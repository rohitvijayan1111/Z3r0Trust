from fastapi import FastAPI, Request
from pydantic import BaseModel
from descope import DescopeClient
import requests
import user_agents
import time
import json
app = FastAPI()

DESCOPE_PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

class LoginPayload(BaseModel):
    email: str
    password: str
    request_type: str

def get_location(ip: str) -> str:
    if ip in ("127.0.0.1", "localhost"):
        try:
            my_ip = requests.get("https://api.ipify.org").text
            ip = my_ip
        except Exception:
            return "Localhost / Private Network"
    try:
        geo_resp = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return f"{geo_resp.get('country','')}/{geo_resp.get('region','')}/{geo_resp.get('city','')}".strip("/")
    except Exception:
        return "unknown"

def parse_device(user_agent_str: str) -> str:
    ua = user_agents.parse(user_agent_str)
    return f"{ua.browser.family} {ua.browser.version_string} on {ua.os.family} {ua.os.version_string} ({ua.device.family or 'Unknown Device'})"

SPLUNK_URL = "https://127.0.0.1:8088/services/collector"   # Splunk HEC endpoint
HEC_TOKEN = "31459979-84f0-4f36-a09e-83326691c5e5"          # Replace with your HEC token
INDEX = "zerotrust_logs"

def send_to_splunk(events):
    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}
    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        return {"status_code": response.status_code, "response": response.text}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@app.post("/login-with-email")
async def login_with_email(payload: LoginPayload, request: Request):
    try:
        login_response = descope_client.password.sign_in(
            login_id=payload.email,
            password=payload.password
        )

        print("Descope login response:", login_response)

        session_token_data = login_response.get("sessionToken", {})
        session_jwt = session_token_data.get("jwt")

        if not session_jwt:
            return {"status": "failure", "message": "No JWT returned", "response": login_response}

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

        # --- Send log to Splunk ---
        event = json.dumps({"event": attributes})
        send_to_splunk([event])

        return {"status": "success", "attributes": attributes, "session_jwt": session_jwt}

    except Exception as e:
        client_ip = request.client.host
        location = get_location(client_ip)
        user_agent_str = request.headers.get("user-agent", "unknown")
        device_info = parse_device(user_agent_str)

        attributes = {
            "Timestamp": int(time.time()),
            "IP Address": client_ip,
            "Geo Location": location,
            "Device": device_info,
            "Request type": payload.request_type,
            "Response": "failure"
        }

        # --- Send failure log to Splunk ---
        event = json.dumps({"event": attributes})
        send_to_splunk([event])

        return {
            "status": "failure",
            "message": str(e),
            "attributes": attributes
        }
