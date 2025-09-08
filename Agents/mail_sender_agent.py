import os
from fastmcp import Client
from phi.model.groq import Groq
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from phi.agent import Agent
from db_controller_agent import db_controller_agent
mcp = FastMCP("AlertHandler")
import asyncio
from server import send_email
from descope import DescopeClient



descope = DescopeClient(project_id=os.getenv("DESCOPE_PROJECT_ID"))


load_dotenv()

def mail_sender_agent(user_id: str, message: str,access_key: str) -> bool:
    token = descope.exchange_access_key(access_key=access_key).get('sessionToken', {}).get('jwt')
    if not token:
        return False
    """
    This agent decides what action to take
    """
    try:
       
        # For now, just send email directly (no async, no MCP)
        result = send_email(user_id, message=message)
        return bool(result)
    except Exception as e:
        
        print(f"Error in mail_sender_agent: {e}")
        return False

