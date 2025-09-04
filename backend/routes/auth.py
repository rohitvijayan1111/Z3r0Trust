from flask import Blueprint, request, jsonify
from descope import DescopeClient
import os

# Create Blueprint
auth = Blueprint("auth", __name__)

# Initialize Descope client
descope_client = DescopeClient(project_id="P32DvqStnvlzxBbYFSmAYq74fsPQ")

# Session validation helper
def validate_descope_session(session_token):
    try:
        jwt_response = descope_client.validate_session(session_token=session_token)
        return jwt_response.user
    except Exception as e:
        return None

# Example route
@auth.route("/validate-session", methods=["POST"])
def validate_session_route():
    data = request.json
    token = data.get("sessionToken")
    
    if not token:
        return jsonify({"error": "No session token provided"}), 400

    user = validate_descope_session(token)
    
    if not user:
        return jsonify({"error": "Invalid session"}), 401

    return jsonify({"user": user})
