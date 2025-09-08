import requests
from requests.auth import HTTPBasicAuth

# From Descope Inbound App B
CLIENT_ID = "UDMyRGoxU0ZhT3hod3o0djBpOUQ2anNlRUpueTpUUEEzMlBYZzBlQ1RoSzVWcm5GSDByQUlDVjltZEs="
CLIENT_SECRET = "Rw6KJE3gLGuwjq10cGF79ztCmtFl9tCPDBIRnZHTb78"

TOKEN_URL = "https://api.descope.com/oauth2/v1/apps/token"
SCOPE = "full_access"

# Step 1: Get Access Token via Client Credentials Flow
data = {
    "grant_type": "client_credentials",
    "scope": SCOPE,
}
response = requests.post(
    TOKEN_URL,
    data=data,
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
)

if response.status_code != 200:
    raise Exception(f"Failed to get token: {response.text}")

access_token = response.json()["access_token"]
print("Access Token:", access_token)
print("✅ Got Access Token")

# Step 2: Call Agent A API with token
headers = {"Authorization": f"Bearer {access_token}"}
print(headers)
resp = requests.get("http://localhost:5000/data", headers=headers)


print("Response from Agent A:")
print("📡 Status Code:", resp.status_code)
print("📩 Raw Response:", resp.text)

try:
    print("📑 JSON Parsed:", resp.json())
except Exception:
    print("⚠️ Response was not JSON")
