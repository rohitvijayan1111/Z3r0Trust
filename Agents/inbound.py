import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

APP_ID = os.getenv("DESCOPE_PROJECT_ID")
CLIENT_ID = os.getenv("DESCOPE_CLIENT_ID")
CLIENT_SECRET = os.getenv("DESCOPE_CLIENT_SECRET")

print(f"APP_ID: {APP_ID}")
print(f"CLIENT_ID: {CLIENT_ID[:6]}***")  # mask for safety
print(f"CLIENT_SECRET: {CLIENT_SECRET[:4]}***")

# ✅ Descope OAuth2 token endpoint
url = "https://api.descope.com/oauth2/v1/token"

# Put credentials in headers (Basic Auth)
resp = requests.post(
    url,
    data={"grant_type": "client_credentials"},
    auth=(CLIENT_ID, CLIENT_SECRET),  # <-- this is the key fix
    timeout=10
)

print("Status:", resp.status_code)
print("Response text:", resp.text)

try:
    print("As JSON:", resp.json())
except Exception:
    print("⚠️ Response is not JSON")
