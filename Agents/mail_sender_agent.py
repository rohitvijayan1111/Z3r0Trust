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

load_dotenv()

def mail_sender_agent(user_id: str, message: str) -> bool:
    """
    This agent decides what action to take
    """
    try:
        descope_access_key = os.getenv("DESCOPE_ACCESS_KEY")
        # For now, just send email directly (no async, no MCP)
        result = send_email(user_id, message=message)
        return bool(result)
    except Exception as e:
        
        print(f"Error in mail_sender_agent: {e}")
        return False

