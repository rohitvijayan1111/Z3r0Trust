import os
import logging
import threading
from typing import Any, Dict, Optional
from groq import Groq
from phi.agent import Agent
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
mcp = FastMCP("AppealHandler")

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

@mcp.tool()
def remove_block(user_id: str,ref_id) -> str:
    """Remove a block (enable user)."""
    try:
        if not descope_client:
            msg = "Descope not configured — cannot remove block."
            log.warning(msg)
            return msg
        descope_client.mgmt.user.activate(user_id)
        log.info(f"Removed block for user {user_id}")
        prompt = f"set blockedUser column to 0 where the id is {ref_id} in the alerts table "
        db_controller_agent(prompt=prompt,access_key=os.getenv("DB_CONTROLLER_AGENT_ACCESS_KEY"))
        _notify_user(user_id, "Your account has been re-enabled by the security team. mail detailly")

        prompt = f"set status column to 0 where the ref_id is {ref_id} in the appeal table "
        db_controller_agent(prompt=prompt,access_key=os.getenv("DB_CONTROLLER_AGENT_ACCESS_KEY"))

        return f"Block removed for {user_id}"
    except Exception as e:
        log.exception("Error in remove_block")
        return f"Failed to remove block for {user_id}: {e}"

@mcp.tool()
def forward_to_soc(user_id: Dict[str, Any]) -> str:
    """Forward alert to SOC — placeholder to push to queue or ticketing system."""
    try:
        # Replace with your SOC integration
        log.info(f"Forwarding to SOC: {alert}")
        prompt = f"mail to {user_id} as appeal recieved successfully, forwarded to our SOC, will get back to you within two working days, thank you, ZeroTrust team"
        mail_sender_agent(user_id,prompt,os.getenv("EMAIL_SENDER_AGENT_ACCESS_KEY"))

        # db_controller_agent or queue push could happen here
        return "Forwarded to SOC"
    except Exception as e:
        log.exception("Error in forward_to_soc")
        return f"Failed to forward to SOC: {e}"


# ------------------ Decision function (callable directly) ------------------

def appeal_handler_agent(appeal: Dict[str, Any],access_key:str):
    """
    Decide action based on  `alert`, subject, content of the appeal then take decision.
    Returns a summary string.
    """
    token = descope_client.exchange_access_key(access_key=access_key).get('sessionToken', {}).get('jwt')
    if not token:
        return "Access Key Not Valid"
    
    if not isinstance(appeal, dict):
        return "Invalid alert payload (expected dict)."

    user_id=appeal.get("email")
    ref_id=appeal.get('ref_id')
    path=os.getenv('IP_AND_PORT_2')
    url = f"{path}/api/alerts/fetchbyid"
    alert = requests.post(url, json={"id":ref_id})
    try:
        if not user_id or not ref_id:
            log.warning("No user identifier found in alert payload.")
            return "No sufficient data found in alert ."
        agent = Agent(
            name="Appeal handler",
            role="Analyse the given appeal and alert data and decide what action to take using available tools",
            model=Groq(id=os.getenv(), api_key=os.getenv()),
            tools=[remove_block,forward_to_soc],
            messages=[
                {"role": "system", "content": "alert_data={alert}, appeal_data={appeal}"}
            ],
            memory={
                "alert": alert,
                "appeal": appeal,
                "user_id":user_id,
                "ref_id":ref_id
            },
            markdown=True,
        )    
        
        print("alert from appeal handler agent")
        print(alert)
        # prompt=f"{alert}, {appeal} if the volnurability of the alert is less, appeal is reasonable enough to remove the block call remove block, if it is not certain forward to soc"
        # agent.print_response(prompt)

        result = agent.run(
            f"""
            Appeal data:
            {appeal_dict}

            Alert data:
            {alert_dict}

            Decide whether to remove block or forward to SOC.
            """
        )
        print(result)

    except Exception as e:
        log.exception("Error in alert_handler_agent")
        return f"Handler error: {e}"


# # ------------------ Run MCP server (when executed) ------------------
# if __name__ == "__main__":
#     import asyncio

#     log.info("Starting MCP AlertHandler server (stdio transport)...")
#     # This will register tools and run the MCP server on stdio (used when spawned by client)
#     asyncio.run(mcp.run_async(transport="stdio"))
