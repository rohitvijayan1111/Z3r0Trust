import os, requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("DESCOPE_PROJECT_ID")
CLIENT_ID = os.getenv("DESCOPE_CLIENT_ID")
CLIENT_SECRET = os.getenv("DESCOPE_CLIENT_SECRET")

url = f"https://api.descope.com/v1/apps/{APP_ID}/token"
data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

resp = requests.post(url, data=data)
print(resp.json())
