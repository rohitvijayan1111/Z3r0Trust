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