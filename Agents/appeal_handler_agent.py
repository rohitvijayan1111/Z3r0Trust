import os
import logging
import threading
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
# Optional imports from your project (safe guarded)

from mail_sender_agent import mail_sender_agent


from db_controller_agent import db_controller_agent

from descope import DescopeClient


load_dotenv()
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ------------------ Descope setup (optional) ------------------
DESCOPE_PROJECT_ID = os.getenv("DESCOPE_PROJECT_ID")
DESCOPE_MANAGEMENT_KEY = os.getenv("DESCOPE_MANAGEMENT_KEY")

descope_client = None
if DescopeClient and DESCOPE_PROJECT_ID and DESCOPE_MANAGEMENT_KEY:
    try:
        descope_client =DescopeClient(project_id=DESCOPE_PROJECT_ID,management_key=DESCOPE_MANAGEMENT_KEY)
        log.info("Descope client initialized.")
    except Exception as e:
        log.error(f"Failed to init Descope client: {e}")
        descope_client = None
else:
    log.warning("Descope client not configured (DESCOPE_PROJECT_ID or DESCOPE_MANAGEMENT_KEY missing).")

# ------------------ MCP server ------------------
mcp = FastMCP("AlertHandler")

# ------------------ Helpers ------------------
def _notify_user(user_id: str, message: str) -> None:
    """Notify user via mail_sender_agent if available. Non-fatal on error."""
    if not mail_sender_agent:
        log.warning("mail_sender_agent not available — skipping notification.")
        return
    try:
        # Try common call signatures
        try:
            mail_sender_agent(user_id, message,os.getenv("EMAIL_SENDER_AGENT_ACCESS_KEY"))  # positional
        except TypeError:
            # fallback to named args if the function expects them
            try:
                mail_sender_agent(user_id=user_id, message=message, access_key=os.getenv("EMAIL_SENDER_AGENT_ACCESS_KEY"))
            except Exception:
                mail_sender_agent(user_id=user_id, message=message,access_key=os.getenv("EMAIL_SENDER_AGENT_ACCESS_KEY"))
        log.info(f"Notification sent to {user_id}.")
    except Exception as e:
        log.exception(f"Failed to notify {user_id}: {e}")


def _get_user_from_alert(alert: Dict[str, Any]) -> Optional[str]:
    """Try multiple keys to extract a user identifier from the alert payload."""
    for key in ("user", "user_id", "userid", "email", "email_id", "account"):
        if alert.get(key):
            return str(alert.get(key))
    return None


def _get_confidence(alert: Dict[str, Any]) -> float:
    """
    Extract a confidence score from the alert. Accepts many key names.
    Normalizes percentages (>1) to 0..1 range if needed.
    Returns 0.0 if none found or parse fails.
    """
    for key in ( "confidence_score"):
        val = alert.get(key)
        if val is None:
            continue
        try:
            conf = float(val)
            # normalize if expressed as percentage (0..100)
            if conf > 1.0:
                conf = conf / 100.0
            # clamp
            return max(0.0, min(1.0, conf))
        except Exception:
            continue
    return 0.0

# ------------------ Tools (registered with MCP) ------------------

@mcp.tool()
def permanently_block_user(user_id: str, alert: Optional[Dict[str, Any]] = None) -> str:
    """Permanently block a user (Descope) and notify them."""
    try:
        if not descope_client:
            msg = "Descope not configured — cannot permanently block."
            log.warning(msg)
            return msg

        descope_client.mgmt.user.deactivate(user_id)
        msg = f"User {user_id} permanently blocked."
        log.info(msg)

        # Notify user
        body = (
            f"Dear {user_id},\n\n"
            "We detected high-confidence suspicious activity and have permanently blocked your account.\n"
            "If you believe this is a mistake, please appeal here: http://34.44.88.193/appeal\n\n"
            "Regards,\nZeroTrust Security Team"
        )
        _notify_user(user_id, body)

        # Optionally log to DB
        # if db_controller_agent:
        #     try:
        #         prompt=f"INSERT INTO alerts (user,action,reason) VALUES ('{user_id}','permanent_block','{alert}')"
        #         db_controller_agent(prompt=prompt,access_key=os.getenv("DB_CONTROLLER_AGENT_ACCESS_KEY"))
        #     except Exception:
        #         log.exception("db_controller_agent failed to log permanent block.")

        return msg
    except Exception as e:
        log.exception("Error in permanently_block_user")
        return f"Failed to permanently block {user_id}: {e}"


@mcp.tool()
def temporarily_block_user(user_id: str, duration: int = 300, alert: Optional[Dict[str, Any]] = None) -> str:
    """Temporarily block a user and schedule re-enable after `duration` seconds."""
    try:
        if not descope_client:
            msg = "Descope not configured — cannot temporarily block."
            log.warning(msg)
            return msg

        descope_client.mgmt.user.deactivate(user_id)
        msg = f"User {user_id} temporarily blocked for {duration} seconds."
        log.info(msg)

        # Schedule unblocking
        def _unblock():
            try:
                descope_client.mgmt.user.activate(user_id)
                log.info(f"User {user_id} re-enabled after temporary block.")
            except Exception:
                log.exception(f"Failed to re-enable {user_id} after temporary block.")

        t = threading.Timer(duration, _unblock)
        t.daemon = True
        t.start()

        # Notify
        body = (
            f"Dear {user_id},\n\n"
            "We detected suspicious activity and temporarily blocked your account.\n"
            f"It will be re-enabled automatically after {duration} seconds.\n"
            "To appeal, visit: http://34.44.88.193/appeal\n\nRegards,\nZeroTrust Security Team"
        )
        _notify_user(user_id, body)

        # try:
        #     db_controller_agent(prompt=f"INSERT INTO alerts (user,action,reason) VALUES ('{user_id}','temporary_block','{alert}')",access_key=os.getenv("DB_CONTROLLER_AGENT_ACCESS_KEY"))
        # except Exception:
        #     log.exception("db_controller_agent failed to log temporary block.")

        return msg
    except Exception as e:
        log.exception("Error in temporarily_block_user")
        return f"Failed to temporarily block {user_id}: {e}"

@mcp.tool()
def log_alert_only(user_id: str, alert: Optional[Dict[str, Any]] = None) -> str:
    """Log the alert in DB or logs and optionally force logout/enforce MFA (non-blocking)."""
    try:
        log_msg = f"Logged alert for {user_id}: {alert}"
        # log.info(log_msg)
        logout_account(user_id)

        # Optionally persist to DB
        
        # Optionally notify the user that we logged and enforced additional checks
        _notify_user(user_id, f"Dear {user_id}, suspicious activity was observed and logged for review. If you did not perform this activity, please appeal: http://34.44.88.193/appeal")

        return f"Alert logged for {user_id}"
    except Exception as e:
        log.exception("Error in log_alert_only")
        return f"Failed to log alert for {user_id}: {e}"

@mcp.tool()
def remove_block(user_id: str) -> str:
    """Remove a block (enable user)."""
    try:
        if not descope_client:
            msg = "Descope not configured — cannot remove block."
            log.warning(msg)
            return msg
        descope_client.mgmt.user.activate(user_id)
        log.info(f"Removed block for user {user_id}")
        _notify_user(user_id, "Your account has been re-enabled by the security team.")
        return f"Block removed for {user_id}"
    except Exception as e:
        log.exception("Error in remove_block")
        return f"Failed to remove block for {user_id}: {e}"

@mcp.tool()
def forward_to_soc(alert: Dict[str, Any]) -> str:
    """Forward alert to SOC — placeholder to push to queue or ticketing system."""
    try:
        # Replace with your SOC integration
        log.info(f"Forwarding to SOC: {alert}")
        # db_controller_agent or queue push could happen here
        return "Forwarded to SOC"
    except Exception as e:
        log.exception("Error in forward_to_soc")
        return f"Failed to forward to SOC: {e}"

@mcp.tool()
def logout_account (user_id: Optional[str] = None, alert: Optional[Dict[str, Any]] = None) -> str:
    """Invalidate a session token (logout)."""
    try:
        if not descope_client:
            msg = "Descope not configured — cannot logout the session."
            log.warning(msg)
            return msg
        descope_client.mgmt.user.logout_user(user_id)
        if user_id:
            _notify_user(user_id, "You have been logged out due to suspicious activity. Please reauthenticate and enable MFA.")
        return "Session invalidated"
    except Exception as e:
        log.exception("Error in logout_account")
        return f"Failed to logout session: {e}"

# ------------------ Decision function (callable directly) ------------------

def alert_handler_agent(alert: Dict[str, Any],access_key:str, temp_duration: int = 3600) -> str:
    """
    Decide action based on confidence score in `alert` and call the proper tool.
    Returns a summary string.
    """
    token = descope_client.exchange_access_key(access_key=access_key).get('sessionToken', {}).get('jwt')
    if not token:
        return "Access Key Not Valid"
    
    if not isinstance(alert, dict):
        return "Invalid alert payload (expected dict)."

    user_id = alert.get("user")
    if not user_id:
        log.warning("No user identifier found in alert payload.")
        return "No user identifier found in alert."

    confidence = int(alert.get("confidence_score"))
    log.info(f"Alert for user={user_id} confidence={confidence:.3f}")

    try:
        if confidence >= 85:
            result = permanently_block_user(user_id, alert)
            action = "permanent_block"
        elif confidence >= 60:
            result = temporarily_block_user(user_id, duration=temp_duration, alert=alert)
            action = "temporary_block"
        else:
            result = log_alert_only(user_id, alert)
            action = "log_only"

        summary = f"Decision: {action}; confidence={confidence:.3f}; result={result}"
        log.info(summary)
        return summary
    except Exception as e:
        log.exception("Error in alert_handler_agent")
        return f"Handler error: {e}"


# # ------------------ Run MCP server (when executed) ------------------
# if __name__ == "__main__":
#     import asyncio

#     log.info("Starting MCP AlertHandler server (stdio transport)...")
#     # This will register tools and run the MCP server on stdio (used when spawned by client)
#     asyncio.run(mcp.run_async(transport="stdio"))
