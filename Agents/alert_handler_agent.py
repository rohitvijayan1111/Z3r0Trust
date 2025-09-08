
# from phi.agent import Agent
# from phi.tools.sql import SQLTools
# import os
# from phi.model.groq import Groq
# from dotenv import load_dotenv
# from mcp.server.fastmcp import FastMCP
# from phi.agent import Agent
# from db_controller_agent import db_controller_agent
# from descope import DescopeClient

# mcp = FastMCP("AlertHandler")

# PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
# descope = DescopeClient(project_id=PROJECT_ID)


# @mcp.tool()
# def logoutaccount(session_token):
#     descope.logout(session_token)

# @mcp.tool()
# def forward_to_soc() -> str:
#     # here have to save in the appeal in db
    
#     return "forwared to soc successfully"

# @mcp.tool()
# def remove_block(userid) -> str:
#     """ remove the block """
#     prompt=f'{userid}'
#     db_controller_agent(prompt=prompt)
#     return "block removed successfully"

# @mcp.tool()
# def permonently_block_the_user(userid) -> str:
#     """Execute the block operation permanantly"""
#     prompt=f"{userid}"
#     db_controller_agent(prompt=prompt)
#     return "Blocked account"
   
# @mcp.tool()
# def temporarily_block_the_user(userid: str) -> str:
#     """Execute the block operation temporarily for certain period of time"""
#     prompt=f"{userid}"
#     db_controller_agent(prompt=prompt)
#     return "Blocked account temporarily"


# @mcp.tool()
# def log_the_alert_no_block(employee_id: str) -> str:
#     """ Execute the block operation """
#     prompt=f"{userid}"
#     db_controller_agent(prompt=prompt)
#     return "looged not blocked"


# def alert_handler(alert):
#     "This agent decides what action to take"
#     model_id="llama-3.3-70b-versatile"
#     load_dotenv()
#     groq_api_key = os.getenv("GROQ_API_KEY")
#     agent = Agent(
#         name="Block handler",
#         role="Analyse the given alert data and decide what action to take withint available tools",
#         model=Groq(id=model_id, api_key=groq_api_key),
#         tools=[permonently_block_the_user,temporarily_block_the_user,log_the_alert_no_block],
#         markdown=True
#         )

#     agent.print_response("list the available tools")
#     return "statues from AlertHandler : Successfully executed"


# print(alert_handler({"id":1,"name":"phissing alert"}))


# from phi.agent import Agent
# from phi.tools.sql import SQLTools
# from phi.model.groq import Groq
# from dotenv import load_dotenv
# from mcp.server.fastmcp import FastMCP
# from descope import DescopeClient
# import os
# import time
# from mail_sender_agent import mail_sender_agent

# # ========== MCP Server ==========
# mcp = FastMCP("AlertHandler")
# alert={}

# # ========== Descope Setup ==========
# PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"
# MANAGEMENT_KEY = os.getenv("DESCOPE_MANAGEMENT_KEY")  # required for user blocking/unblocking
# descope = DescopeClient(project_id=PROJECT_ID, management_key=MANAGEMENT_KEY)

# # ========== Tools ==========

# @mcp.tool()
# def logoutaccount(session_token: str,userid: str,alert: dict) -> str:
#     """Logout a user by invalidating their session token"""
#     try:
#         descope.logout(session_token)
#         prompt = (
#                 f"send email to {userid} that Dear {userid} Our monitoring detected suspicious activity and notified already : {alert} Your account is being logged out and enable multi factor autheentication for security reason. Regards, ZeroTrust Security Monitoring Team, here add the button appeal and on cick the button should redirect to http://34.44.88.193/appeal"
#             )
#         mail_sender_agent(user_id=userid,message=prompt)
#         return "✅ User logged out successfully"
#     except Exception as e:
#         return f"❌ Logout failed: {str(e)}"


# @mcp.tool()
# def forward_to_soc() -> str:
#     """Forward alert to SOC team"""
#     # (Here you could push alert into SOC queue or DB)
#     return "📨 Alert forwarded to SOC successfully"


# @mcp.tool()
# def remove_block(userid: str) -> str:
#     """Remove block from a user account"""
#     try:
#         descope.management.user.update_status(userid, "enabled")
#         return f"✅ Block removed for user {userid}"
#     except Exception as e:
#         return f"❌ Failed to remove block: {str(e)}"


# @mcp.tool()
# def permanently_block_the_user(userid: str) -> str:
#     """Block the user account permanently"""
#     try:
#         descope.management.user.update_status(userid, "disabled")

#         prompt = (
#                 f"send email to {userid} that Dear {userid} Our monitoring detected suspicious activity and notified already : {alert} Your account blocked permanently because of this. Regards, ZeroTrust Security Monitoring Team, here add the button appeal and on cick the button should redirect to http://34.44.88.193/appeal"
#             )
        
#         mail_sender_agent(user_id=userid,message=prompt)
#         return f"🚫 Permanently blocked user {userid}"
#     except Exception as e:
#         return f"❌ Failed to block user: {str(e)}"

# import threading, time

# @mcp.tool()
# def temporarily_block_the_user(userid: str, duration: int = 600) -> str:
#     """Block the user account temporarily for a given duration (seconds)"""
#     try:
#         descope.management.user.update_status(userid, "disabled")

#         # Background task to re-enable after duration
#         def unblock_later():
#             time.sleep(duration)
#             descope.management.user.update_status(userid, "enabled")

#         threading.Thread(target=unblock_later, daemon=True).start()

#         prompt = (
#             f"send email to {userid} that Dear {userid} Our monitoring detected suspicious activity: {alert}. Your account was blocked temporarily. Regards, ZeroTrust Security Monitoring Team. Click here to appeal: http://34.44.88.193/appeal"
#         )
#         mail_sender_agent(user_id=userid, message=prompt)

#         return f"⏳ Temporarily blocked {userid} for {duration} seconds"
#     except Exception as e:
#         return f"❌ Temporary block failed: {str(e)}"

# @mcp.tool()
# def log_the_alert_no_block(employee_id: str) -> str:
#     """
#     Log the alert, log the user out, and enforce MFA on next login.
#     """
#     try:
#         # 1. Log the alert
#         log_msg = f"📝 Logged alert for user{employee_id}, no block applied"

#         # 2. Logout (invalidate session token)
#         # descope.logout(session_token)

#         # # 3. Enforce MFA for the user on next login
#         # descope.management.user.update_mfa(
#         #     identifier=employee_id,
#         #     totp=True,   # force TOTP MFA (Google Authenticator, etc.)
#         #     phone=True   # force phone MFA if needed
#         # )

#         return f"{log_msg}. ✅ User {employee_id} logged out and MFA enforced."
#     except Exception as e:
#         return f"❌ Failed to log alert and enforce MFA: {str(e)}"


# # ========== Alert Handler Agent ==========

# def alert_handler_agent(alert1: dict):
#     global alert
#     alert=alert1
#     """This agent decides what action to take"""
#     model_id = "llama-3.3-70b-versatile"
#     load_dotenv()
#     groq_api_key = os.getenv("GROQ_API_KEY")

#     agent = Agent(
#         name="Block handler",
#         role="Analyse the given alert data and decide what action to take using available tools",
#         model=Groq(id=model_id, api_key=groq_api_key),
#         tools=[permanently_block_the_user, temporarily_block_the_user, log_the_alert_no_block,remove_block,forward_to_soc,remove_block],
#         markdown=True,
#     )

#     # Debug: ask it what tools it has
#     # agent.print_response("List the available tools")

#     # Pass the alert to the agent for decision
#     agent.print_response(f"Handle this alert: {alert1} proprly, and do the action promptly")

#     return "✅ Status from AlertHandler: Successfully executed"

# alert_handler_agent.py
import os
import logging
import threading
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import requests

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
       

        # Optionally log to DB
        # if db_controller_agent:
        try:
            r_id=alert["id"]
            prompt = f"set blockedUser column to 1 where the id is {r_id} in the alerts table "
            db_controller_agent(prompt=prompt,access_key=os.getenv("DB_CONTROLLER_AGENT_ACCESS_KEY"))
        except Exception:
            log.exception("db_controller_agent failed to log permanent block.")

        # try:
        #     new_id=alert.get("id")
        #     prompt = f"add the entry to the table 'appeal'(id	int,subject	varchar(200), content	varchar(2000), status	tinyint(1),ref_id (int), created_at(timestamp)), here the subject null, content null, ref_id is {new_id}, created_at is default value"
        #     db_controller_agent(prompt=prompt,access_key=os.getenv("DB_CONTROLLER_AGENT_ACCESS_KEY"))
        # except Exception:
        #     log.exception("db_controller_agent failed to log temporary block.")
        new_id=alert.get("id")
        url = "http://localhost:5000/api/appeals/add/init"
        data={"new_id":new_id}
        response = requests.post(url, json=data)

        body = f"send mail detially as Dear {user_id} We detected high-confidence suspicious activity and have permanently blocked your account.If you believe this is a mistake, please appeal here: http://localhost:2222/appeal\n\n , notify the user that he has to enter the appeal ref id {r_id} for further follow up Regards,\nZeroTrust Security Team"
        
        _notify_user(user_id, body)

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
        # def _unblock():
        #     try:
        #         descope_client.mgmt.user.activate(user_id)
        #         log.info(f"User {user_id} re-enabled after temporary block.")
        #     except Exception:
        #         log.exception(f"Failed to re-enable {user_id} after temporary block.")

        # t = threading.Timer(duration, _unblock)
        # t.daemon = True
        # t.start()
        new_id=alert.get("id")
        # Notify
        body =   f"send mail detially as Dear {user_id} We detected high-confidence suspicious activity and have Temporarily blocked your account.If you believe this is a mistake, please appeal here: http://34.44.88.193/appeal\n\n , notify the user that he has to enter the appeal ref id {new_id} for further follow up Regards,\nZeroTrust Security Team"
        _notify_user(user_id, body)

        try:
            prompt = f"set blockedUser column to 1 where the id is {new_id} in the alerts table "
            db_controller_agent(prompt=prompt,access_key=os.getenv("DB_CONTROLLER_AGENT_ACCESS_KEY"))

        except Exception:
            log.exception("db_controller_agent failed to log permanent block.")
            
        # try:
        #     new_id=alert.get("new_id")
        #     prompt = f"add the entry to the table 'appeal'(id int autoincrement,subject	varchar(200), content	varchar(2000), status	tinyint(1),ref_id (int), created_at(timestamp) Default CURRENT_TIMESTAMP), here the subject null, content null, ref_id is {new_id}"
        #     db_controller_agent(prompt=prompt,access_key=os.getenv("DB_CONTROLLER_AGENT_ACCESS_KEY"))
        # except Exception:
        #     log.exception("db_controller_agent failed to log temporary block.")
        url = "http://localhost:5000/api/appeals/add/init"
        data={"new_id":alert.get("id")}
        response = requests.post(url, json=data)
        
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
        if confidence >= 80:
            result = permanently_block_user(user_id, alert)
            action = "permanent_block"
        elif confidence >= 50:
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
