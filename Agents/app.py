from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastmcp import Client
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
from app_helper_functions import apply_policy 
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from app_helper_functions import apply_policy
import httpx
import requests

load_dotenv()

app = FastAPI()

class AlertRequest(BaseModel):
    alert_name: str
    confidence_score: float
    timestamp: Optional[str]
    user: str
    email: str
    ip: Optional[str] = None
    location: Optional[str] = None
    device: Optional[str] = None
    action: Optional[str] = None
    status: Optional[str] = None

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
    print(request.email_id,request.message)
    async with Client(MCP_SERVER_URL) as client:
        # Authenticate with Descope access key
        # await client.call_tool("authenticator", {"access_key": DESCOPE_ACCESS_KEY})
        
        # Call the MCP tool to send email
        result = await client.call_tool(
            "send_email_to_employees",
            {"email_id": request.email_id, "message": request.message}
        )
        return {"result": result}

@app.get("/get-email")
async def get_email():
    async with Client(MCP_SERVER_URL) as client:
        result=await client.call_tool(
            "retrieve_unread_emails"
        )
        print(result)
        return {"result":result}

templates = Jinja2Templates(directory="templates")

# Serve the appeal form
@app.get("/appeal", response_class=HTMLResponse)
async def get_appeal(request: Request):
    """
    Return HTML page with multiple appeal entries and submit button
    """
    return templates.TemplateResponse("appeal.html", {"request": request})

@app.post("/appealrequest")
async def handle_appeal(
    subject1: str = Form(...),
    content1: str = Form(...),
   
):
    """
    Receive submitted appeal content and close window
    """
    # Here you can process/save the appeals
    print("Appeals received:")
    print(f"1: {subject1} - {content1}")
    # print(f"2: {subject2} - {content2}")

    # Return JS to close the window
    return HTMLResponse(content="""
        <html>
            <body>
                <script>
                    alert("Appeals submitted successfully!");
                    window.close();
                </script>
            </body>
        </html>
    """)

@app.post("/webhook")
async def webhook(alert: dict):
    """
    Process alert JSON and forward it to /responses/add
    """

    #need to write the for look policy

    print(alert)
    alert_data = apply_policy(alert)

    prompt = f"mail this issue to the {alert.get('user')} with the detailed summary of the following details, parapharase these into a passage such that everyone can understand" + str(alert) +"along with this, warn them the account might be blocked, regards ZeroTrust security monitoring team"
    print(prompt)
    async with Client(MCP_SERVER_URL) as client:
        # Authenticate with Descope access key
        # await client.call_tool("authenticator", {"access_key": DESCOPE_ACCESS_KEY})
        
        # Call the MCP tool to send email
        result = await client.call_tool(
            "send_email_to_employees",
            {"email_id": alert.get('user'), "message": prompt}
        )
        print(result)




    print(f"✅ Alert processed locally: {alert_data.get('alert_name')} for user {alert_data.get('user')}")
    return {"status": "processed", "alert": alert_data}




