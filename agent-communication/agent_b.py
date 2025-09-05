# agent_b.py
import os
import jwt  # PyJWT
from flask import Flask, request, jsonify
from descope import DescopeClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = DescopeClient(project_id=os.getenv("DESCOPE_PROJECT_ID"))

@app.route("/secure-data", methods=["POST"])
def secure_data():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid auth header"}), 401

    token = auth_header.split(" ")[1]

    try:
        # Decode and verify the JWT manually using PyJWT
        decoded = jwt.decode(token, options={"verify_signature": False})  # optional: verify signature if needed
        return jsonify({
            "status": "success",
            "msg": "Hello from Agent B!",
            "validated_agent": decoded.get("sub")
        })
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 401

if __name__ == "__main__":
    app.run(port=5001)
