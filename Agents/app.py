from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastmcp import Client
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import asyncio
from app_helper_functions import apply_policy 
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from app_helper_functions import apply_policy
from cache import is_duplicate,cache_cleaner
import httpx
import requests
from typing import Optional, Union, List


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
async def webhook(alerts: Union[dict, List[dict]]):
    print(alerts)
    if isinstance(alerts, dict):
        alerts = [alerts]

    import json
    print(json.dumps(alerts, indent=4))  # pretty print

    processed, suppressed = [], []

    for alert in alerts:
        alert=alert = alert["result"]
        alert_id = alert.get("alert_id")
        alert_name = alert.get("alert_name")
        if not alert_id or not alert_name:
            continue
        if is_duplicate(alert_id, alert_name):
            suppressed.append(alert_id)
            print("XXXXXXXXXX Duplicate detected")
            continue

        alert_data = apply_policy(alert)
        processed.append(alert_data)

        prompt = (
            f"Dear {alert.get('user')},\n\n"
            f"Our monitoring detected suspicious activity:\n\n"
            f"{alert}\n\n"
            "Your account may be blocked if this continues.\n"
            "Regards,\nZeroTrust Security Monitoring Team"
        )

        # async with Client(MCP_SERVER_URL) as client:
        #     await client.call_tool(
        #         "send_email_to_employees",
        #         {"email_id": alert.get("user"), "message": prompt}
        #     )

        print(f"✅ Processed alert: {alert_name} for {alert.get('user')}")

    return {
        "status": "done",
        "processed_count": len(processed),
        "suppressed_count": len(suppressed),
        "processed": processed,
        "suppressed": suppressed,
    }

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(cache_cleaner())