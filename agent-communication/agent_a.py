from flask import Flask, request, jsonify
from descope import DescopeClient

app = Flask(__name__)

# Use your Project ID from Descope
PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"

client = DescopeClient(project_id=PROJECT_ID)

@app.route("/data", methods=["GET"])
def get_data():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing Bearer token"}), 401

    try:
        jwt_response = client.validate_jwt(token)
        return jsonify({
            "message": "✅ Access granted",
            "claims": jwt_response
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(port=5000, debug=True)
