import asyncio
import logging
import os
from fastmcp import FastMCP
from phi.agent import Agent
from phi.tools.email import EmailTools
from phi.model.groq import Groq
from dotenv import load_dotenv
from descope import DescopeClient
from fastapi import HTTPException

model_id="llama-3.3-70b-versatile"
load_dotenv()
# jwt_response = descope_client.validate_session(session_token=session_token)

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("MCP Server on Cloud Run")

# ✅ Descope validator

descope_client = DescopeClient(project_id=os.getenv("DESCOPE_PROJECT_ID"))

def validate_token(access_key: str):
   
    """Helper to validate a JWT with Descope"""
    try:
        jwt_response = descope_client.exchange_access_key(access_key=access_key)
        token = jwt_response.get('sessionToken', {}).get('jwt')
        if not token:
            return False
        return True
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Invalid token: {e}")

# ✅ Authenticator tool
@mcp.tool()
def authenticator(access_key: str) -> bool:
    """
    Validate a Descope session token.
    
    Args:
        token: JWT session token
    
    Returns:
        True if authenticated, False otherwise
    """
    return validate_token(access_key=access_key)

# ✅ Add tool
@mcp.tool()
def add(a: int, b: int) -> int:
    
    logger.info(f">>> Tool: 'add' called with {a} + {b}")
    return a + b

# ✅ Subtract tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    
    logger.info(f">>> Tool: 'subtract' called with {a} - {b}")
    return a - b


@mcp.tool()
def send_email_to_employees(email_id:str, message:str) -> str:  
    model_id="llama-3.3-70b-versatile"
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    sender_email = "kavirajmetech@gmail.com"
    sender_name = "kaviyarasu"
    sender_passkey = os.getenv("GMAIL_PASSKEY")

    agent = Agent(
        name="Web Search Agent",
        role="Send email",
        model=Groq(id=model_id, api_key=groq_api_key),
        tools=[
            EmailTools(
                receiver_email=email_id,
                sender_email=sender_email,
                sender_name=sender_name,
                sender_passkey=sender_passkey,
            )
        ],
        markdown=True
    )
    agent.print_response(f"{message} send mail only once")
    return "mail sent successfully"

# ✅ Run MCP server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f"🚀 MCP server started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=port,
        )
    )
