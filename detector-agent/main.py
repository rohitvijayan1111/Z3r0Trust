from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from descope import DescopeClient
import requests
import user_agents
import time
import json
import os

app = FastAPI()

# Enable CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DESCOPE_PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

class LoginPayload(BaseModel):
    email: str
    password: str
    request_type: str

def get_location(ip: str) -> str:
    """Get geolocation from IP address."""
    if ip in ("127.0.0.1", "localhost"):
        try:
            ip = requests.get("https://api.ipify.org").text
        except Exception:
            return "Localhost / Private Network"
    try:
        geo_resp = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return f"{geo_resp.get('country','')} / {geo_resp.get('region','')} / {geo_resp.get('city','')}"
    except Exception:
        return "unknown"

def parse_device(user_agent_str: str) -> str:
    """Parse user agent string into readable device info."""
    ua = user_agents.parse(user_agent_str)
    browser = f"{ua.browser.family} {ua.browser.version_string}"
    os = f"{ua.os.family} {ua.os.version_string}"
    device = ua.device.family or "Unknown Device"
    return f"{browser} on {os} ({device})"

def log_attempt(data: dict):
    """Save each login attempt to logs.json"""
    logfile = "logs.json"
    if os.path.exists(logfile):
        with open(logfile, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(data)
    with open(logfile, "w") as f:
        json.dump(logs, f, indent=4)

@app.post("/login-with-email")
async def login_with_email(payload: LoginPayload, request: Request):
    client_ip = request.client.host
    location = get_location(client_ip)
    user_agent_str = request.headers.get("user-agent", "unknown")
    device_info = parse_device(user_agent_str)
    timestamp = int(time.time())

    try:
        login_response = descope_client.password.sign_in(
            login_id=payload.email,
            password=payload.password
        )
        session_token_data = login_response.get("sessionToken", {})
        session_jwt = session_token_data.get("jwt")
        user = login_response.get("user", {})

        status = "success" if session_jwt else "failure"
        attributes = {
            "Timestamp": timestamp,
            "Username": user.get("email") or payload.email,
            "IP Address": client_ip,
            "Geo Location": location,
            "Device": device_info,
            "Request type": payload.request_type,
            "Response": status,
        }

        result = {
            "status": status,
            "attributes": attributes,
            "session_jwt": session_jwt[:40] + "..." if session_jwt else None,
        }

        log_attempt(result)  # save log
        return result

    except Exception as e:
        attributes = {
            "Timestamp": timestamp,
            "Username": payload.email,
            "IP Address": client_ip,
            "Geo Location": location,
            "Device": device_info,
            "Request type": payload.request_type,
            "Response": "failure",
        }
        result = {"status": "failure", "message": str(e), "attributes": attributes}
        log_attempt(result)  # save log
        return result
