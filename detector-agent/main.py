from fastapi import FastAPI, Request
from pydantic import BaseModel
from descope import DescopeClient
import requests
import user_agents
import time

app = FastAPI()

DESCOPE_PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

class LoginPayload(BaseModel):
    email: str
    password: str
    request_type: str

def get_location(ip: str) -> str:
    """Get geolocation from IP address."""
    if ip in ("127.0.0.1", "localhost"):
        # fallback: fetch own public IP
        try:
            my_ip = requests.get("https://api.ipify.org").text
            ip = my_ip
        except Exception:
            return "Localhost / Private Network"

    try:
        geo_resp = requests.get(f"https://ipinfo.io/{ip}/json").json()
        country = geo_resp.get("country", "")
        region = geo_resp.get("region", "")
        city = geo_resp.get("city", "")
        return f"{country} / {region} / {city}".strip(" /")
    except Exception:
        return "unknown"

def parse_device(user_agent_str: str) -> str:
    """Parse user agent string into readable device info."""
    ua = user_agents.parse(user_agent_str)
    browser = f"{ua.browser.family} {ua.browser.version_string}"
    os = f"{ua.os.family} {ua.os.version_string}"
    device = ua.device.family or "Unknown Device"
    return f"{browser} on {os} ({device})"

@app.post("/login-with-email")
async def login_with_email(payload: LoginPayload, request: Request):
    try:
        login_response = descope_client.password.sign_in(
            login_id=payload.email,
            password=payload.password
        )

        session_token_data = login_response.get("sessionToken", {})
        session_jwt = session_token_data.get("jwt")

        if not session_jwt:
            return {
                "status": "failure",
                "message": "No JWT returned",
                "response": login_response
            }

        user = login_response.get("user", {})
        client_ip = request.client.host
        location = get_location(client_ip)
        user_agent_str = request.headers.get("user-agent", "unknown")
        device_info = parse_device(user_agent_str)

        attributes = {
            "Timestamp": int(time.time()),
            "Username": user.get("email") or payload.email,
            "IP Address": client_ip,
            "Geo Location": location,
            "Device": device_info,
            "Request type": payload.request_type,
            "Response": "success"
        }

        return {
            "status": "success",
            "attributes": attributes,
            "session_jwt": session_jwt[:40] + "..."  
        }

    except Exception as e:
        client_ip = request.client.host
        location = get_location(client_ip)
        user_agent_str = request.headers.get("user-agent", "unknown")
        device_info = parse_device(user_agent_str)

        return {
            "status": "failure",
            "message": str(e),
            "attributes": {
                "Timestamp": int(time.time()),
                "IP Address": client_ip,
                "Geo Location": location,
                "Device": device_info,
                "Request type": payload.request_type,
                "Response": "failure"
            }
        }
