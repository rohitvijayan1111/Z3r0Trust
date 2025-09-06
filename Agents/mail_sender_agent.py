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


async def mail_sender_agent(user_id,message):
    "This agent decides what action to take"
    
    DESCOPE_ACCESS_KEY = os.getenv("DESCOPE_ACCESS_KEY")

    # async with Client(MCP_SERVER_URL) as client:

    #     # Authenticate with Descope access key
    #     # await client.call_tool("authenticator", {"access_key": DESCOPE_ACCESS_KEY})
    #     # Call the MCP tool to send email


    #     result = await client.call_tool(
    #         "send_email_to_employees",
    #         {"email_id": user_id, "message": message}
    #     )
    result=send_email(user_id,message=message)

    return {"result": result}
    return "statues from AlertHandler : Successfully executed"

