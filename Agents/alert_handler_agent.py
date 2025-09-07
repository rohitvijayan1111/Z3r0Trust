
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


from phi.agent import Agent
from phi.tools.sql import SQLTools
from phi.model.groq import Groq
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from descope import DescopeClient
import os
import time
from mail_sender_agent import mail_sender_agent

# ========== MCP Server ==========
mcp = FastMCP("AlertHandler")
alert={}

# ========== Descope Setup ==========
PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"
MANAGEMENT_KEY = os.getenv("DESCOPE_MANAGEMENT_KEY")  # required for user blocking/unblocking
descope = DescopeClient(project_id=PROJECT_ID, management_key=MANAGEMENT_KEY)

# ========== Tools ==========

@mcp.tool()
def logoutaccount(session_token: str,userid: str,alert: dict) -> str:
    """Logout a user by invalidating their session token"""
    try:
        descope.logout(session_token)
        prompt = (
                f"send email to {userid} that Dear {userid} Our monitoring detected suspicious activity and notified already : {alert} Your account is being logged out and enable multi factor autheentication for security reason. Regards, ZeroTrust Security Monitoring Team, here add the button appeal and on cick the button should redirect to http://34.44.88.193/appeal"
            )
        mail_sender_agent(user_id=userid,message=prompt)
        return "✅ User logged out successfully"
    except Exception as e:
        return f"❌ Logout failed: {str(e)}"


@mcp.tool()
def forward_to_soc() -> str:
    """Forward alert to SOC team"""
    # (Here you could push alert into SOC queue or DB)
    return "📨 Alert forwarded to SOC successfully"


@mcp.tool()
def remove_block(userid: str) -> str:
    """Remove block from a user account"""
    try:
        descope.management.user.update_status(userid, "enabled")
        return f"✅ Block removed for user {userid}"
    except Exception as e:
        return f"❌ Failed to remove block: {str(e)}"


@mcp.tool()
def permanently_block_the_user(userid: str) -> str:
    """Block the user account permanently"""
    try:
        descope.management.user.update_status(userid, "disabled")

        prompt = (
                f"send email to {userid} that Dear {userid} Our monitoring detected suspicious activity and notified already : {alert} Your account blocked permanently because of this. Regards, ZeroTrust Security Monitoring Team, here add the button appeal and on cick the button should redirect to http://34.44.88.193/appeal"
            )
        
        mail_sender_agent(user_id=userid,message=prompt)
        return f"🚫 Permanently blocked user {userid}"
    except Exception as e:
        return f"❌ Failed to block user: {str(e)}"

import threading, time

@mcp.tool()
def temporarily_block_the_user(userid: str, duration: int = 600) -> str:
    """Block the user account temporarily for a given duration (seconds)"""
    try:
        descope.management.user.update_status(userid, "disabled")

        # Background task to re-enable after duration
        def unblock_later():
            time.sleep(duration)
            descope.management.user.update_status(userid, "enabled")

        threading.Thread(target=unblock_later, daemon=True).start()

        prompt = (
            f"send email to {userid} that Dear {userid} Our monitoring detected suspicious activity: {alert}. Your account was blocked temporarily. Regards, ZeroTrust Security Monitoring Team. Click here to appeal: http://34.44.88.193/appeal"
        )
        mail_sender_agent(user_id=userid, message=prompt)

        return f"⏳ Temporarily blocked {userid} for {duration} seconds"
    except Exception as e:
        return f"❌ Temporary block failed: {str(e)}"


@mcp.tool()
def log_the_alert_no_block(employee_id: str, session_token: str) -> str:
    """
    Log the alert, log the user out, and enforce MFA on next login.
    """
    try:
        # 1. Log the alert
        log_msg = f"📝 Logged alert for employee {employee_id}, no block applied"

        # 2. Logout (invalidate session token)
        descope.logout(session_token)

        # 3. Enforce MFA for the user on next login
        descope.management.user.update_mfa(
            identifier=employee_id,
            totp=True,   # force TOTP MFA (Google Authenticator, etc.)
            phone=True   # force phone MFA if needed
        )

        return f"{log_msg}. ✅ User {employee_id} logged out and MFA enforced."
    except Exception as e:
        return f"❌ Failed to log alert and enforce MFA: {str(e)}"


# ========== Alert Handler Agent ==========

def alert_handler_agent(alert1: dict):
    global alert
    alert=alert1
    """This agent decides what action to take"""
    model_id = "llama-3.3-70b-versatile"
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    agent = Agent(
        name="Block handler",
        role="Analyse the given alert data and decide what action to take using available tools",
        model=Groq(id=model_id, api_key=groq_api_key),
        tools=[permanently_block_the_user, temporarily_block_the_user, log_the_alert_no_block,remove_block,forward_to_soc,remove_block],
        markdown=True,
    )

    # Debug: ask it what tools it has
    # agent.print_response("List the available tools")

    # Pass the alert to the agent for decision
    agent.print_response(f"Handle this alert: {alert1} proprly, and do the action promptly")

    return "✅ Status from AlertHandler: Successfully executed"


# ========== Run Example ==========
# if __name__ == "__main__":
#     test_alert = {"id": 1, "name": "phishing alert", "user": "bob@example.com"}
#     print(alert_handler(test_alert))
