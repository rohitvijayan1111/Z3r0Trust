from flask import Blueprint, request, jsonify
import requests

auth = Blueprint("auth", __name__)

FASTAPI_LOGIN_URL = "http://localhost:8000/login-with-email"

@auth.route("/login", methods=["POST"])
def login_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    request_type = data.get("request_type", "web")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        response = requests.post(
            FASTAPI_LOGIN_URL,
            json={"email": email, "password": password, "request_type": request_type},
            timeout=5
        )
        fastapi_result = response.json()
        print("FastAPI Login Response:", fastapi_result)
        return jsonify(fastapi_result)
    except Exception as e:
        print("Error calling FastAPI login:", str(e))
        return jsonify({"error": "Login service unavailable"}), 503
