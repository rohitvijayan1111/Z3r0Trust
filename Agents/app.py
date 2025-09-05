# from fastapi import FastAPI
# import asyncio
# from fastmcp import Client
# import os
# from dotenv import load_dotenv

# load_dotenv()
# app = FastAPI()

# @app.get("/")
# def hello():
#     return {"message": "Hello MCP!"}

# @app.post("/send-email")
# async def send_email(email_id: str, message: str):
#     async with Client("http://localhost:8080/mcp") as client:
#         await client.call_tool("authenticator", {"access_key": os.getenv("DESCOPE_ACCESS_KEY")})
#         result = await client.call_tool("send_email_to_employees", {"email_id": email_id, "message": message})
#         print(result)
#         return {"result": result[0].text}


from fastapi import FastAPI
from pydantic import BaseModel
import os
import asyncio
from fastmcp import Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
DESCOPE_ACCESS_KEY = os.getenv("DESCOPE_ACCESS_KEY")


# --------- Request model ---------
class EmailRequest(BaseModel):
    email_id: str
    message: str


# --------- Health check ---------
@app.get("/")
def hello():
    return {"message": "Hello MCP!"}


# --------- List available tools ---------
@app.get("/tools")
async def list_tools():
    async with Client(MCP_SERVER_URL) as client:
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        return {"tools": tool_names}


# --------- Send email via MCP tool ---------
@app.post("/send-email")
async def send_email(request: EmailRequest):
    async with Client(MCP_SERVER_URL) as client:
        # Authenticate with Descope access key
        await client.call_tool("authenticator", {"access_key": DESCOPE_ACCESS_KEY})
        
        # Call the MCP tool to send email
        result = await client.call_tool(
            "send_email_to_employees",
            {"email_id": request.email_id, "message": request.message}
        )
        return {"result": result[0].text}
