
from phi.agent import Agent
from phi.tools.sql import SQLTools
import os
from phi.model.groq import Groq
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from phi.agent import Agent
from db_controller_agent import db_controller_agent
mcp = FastMCP("AlertHandler")

@mcp.tool()
def forward_to_soc() -> str:
    # here have to save in the appeal in db
    
    return "forwared to soc successfully"

@mcp.tool()
def remove_block(userid) -> str:
    """ remove the block """
    prompt=f'{userid}'
    db_controller_agent(prompt=prompt)
    return "block removed successfully"

@mcp.tool()
def permonently_block_the_user(userid) -> str:
    """Execute the block operation permanantly"""
    prompt=f"{userid}"
    db_controller_agent(prompt=prompt)
    return "Blocked account"
   
@mcp.tool()
def temporarily_block_the_user(userid: str) -> str:
    """Execute the block operation temporarily for certain period of time"""
    prompt=f"{userid}"
    db_controller_agent(prompt=prompt)
    return "Blocked account temporarily"


@mcp.tool()
def log_the_alert_no_block(employee_id: str) -> str:
    """ Execute the block operation """
    prompt=f"{userid}"
    db_controller_agent(prompt=prompt)
    return "looged not blocked"


def alert_handler(alert):
    "This agent decides what action to take"
    model_id="llama-3.3-70b-versatile"
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    agent = Agent(
        name="Block handler",
        role="Analyse the given alert data and decide what action to take withint available tools",
        model=Groq(id=model_id, api_key=groq_api_key),
        tools=[permonently_block_the_user,temporarily_block_the_user,log_the_alert_no_block],
        markdown=True
        )

    agent.print_response("list the available tools")
    return "statues from AlertHandler : Successfully executed"


print(alert_handler({"id":1,"name":"phissing alert"}))