# Updated working example for secure communication between Agent A and Agent B using Descope
# This version handles the latest SDK response for Access Keys

# agent_a.py
import os
import requests
from flask import Flask, jsonify
from descope import DescopeClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = DescopeClient(project_id=os.getenv("DESCOPE_PROJECT_ID"))

# Updated function to extract JWT correctly
def get_service_jwt():
    jwt_response = client.exchange_access_key(os.getenv("DESCOPE_ACCESS_KEY"))
    print("JWT Response:", jwt_response)  # Debug
    # Extract the JWT from nested 'sessionToken' object
    token = jwt_response.get('sessionToken', {}).get('jwt')
    if not token:
        raise Exception("JWT not found in exchange_access_key response")
    return token

@app.route("/call-agent-b")
def call_agent_b():
    token = get_service_jwt()
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.post("http://localhost:5001/secure-data", headers=headers)

    return jsonify({
        "agent_a_status": "called agent b",
        "agent_b_response": resp.json()
    })

if __name__ == "__main__":
    app.run(port=5000)


# agent_b.py
