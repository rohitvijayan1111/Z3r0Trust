import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import threading
# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# -------------------------------
# Database setup
# -------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alerts.db"
db = SQLAlchemy(app)

# Alert Model
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alert_name = db.Column(db.String(120))
    confidence_score = db.Column(db.String(50))
    timestamp = db.Column(db.String(50))
    user = db.Column(db.String(120))
    email = db.Column(db.String(120))
    ip = db.Column(db.String(50))
    location = db.Column(db.String(120))
    device = db.Column(db.String(120))
    action = db.Column(db.String(120))
    status = db.Column(db.String(50))
    failed_count = db.Column(db.Integer, default=0)

# -------------------------------
# Configs from .env
# -------------------------------
HEC_TOKEN = os.getenv("HEC_TOKEN", "changeme")
EMAIL_AGENT_URL = os.getenv("EMAIL_AGENT_URL", "http://127.0.0.1:6001/email")
SOC_API_URL = os.getenv("SOC_API_URL", "http://127.0.0.1:6002/soc")
MAIL_AGENT_TOKEN = os.getenv("MAIL_AGENT_TOKEN", "supersecrettoken")

# -------------------------------
# Policy function
# -------------------------------
def apply_policy(alert):
    try:
        score = int(alert.get("confidence_score", 0))
    except ValueError:
        score = 0

    if 0 <= score <= 30:
        alert["status"] = "logged"
    elif 31 <= score <= 60:
        alert["status"] = "mfa_required"
    elif 61 <= score <= 80:
        alert["status"] = "temporary_block"
    elif 81 <= score <= 100:
        alert["status"] = "permanent_block"
    else:
        alert["status"] = "unknown"

    return alert

# -------------------------------
# Send to Mail Agent
# -------------------------------

def send_email_async(alert):
    thread = threading.Thread(target=send_to_email_agent, args=(alert,))
    thread.start()

def send_to_email_agent(alert):
    payload = {
        "email": alert.get("email", "soc_team@example.com"),
        "user": alert.get("user", "Unknown"),
        "alert_name": alert.get("alert_name", "Unknown Alert"),
        "confidence_score": alert.get("confidence_score", "N/A"),
        "ip": alert.get("ip", "N/A"),
        "timestamp": alert.get("timestamp", "N/A"),
        "location": alert.get("location", "N/A"),
        "device": alert.get("device", "N/A"),
        "action": alert.get("action", "N/A"),
        "status": alert.get("status", "N/A")
    }
    headers = {
        "Authorization": f"Bearer {MAIL_AGENT_TOKEN}"
    }
    try:
        r = requests.post(EMAIL_AGENT_URL, json=payload, headers=headers, timeout=500)
        print(f"📧 Mail Agent Response: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Error sending to Mail Agent: {e}")

# -------------------------------
# Send to SOC Receiver
# -------------------------------
def send_to_soc(alert):
    try:
        r = requests.post(SOC_API_URL, json=alert, timeout=5)
        print(f"📡 SOC Receiver Response: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Error sending to SOC Receiver: {e}")

# -------------------------------
# Webhook endpoint (Splunk alert)
# -------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    auth = request.headers.get("Authorization")
    # Optional HEC token validation
    # if auth != f"Splunk {HEC_TOKEN}":
    #     return jsonify({"error": "Unauthorized"}), 403

    alert = request.json or {}
    if not alert:
        return jsonify({"status": "error", "error": "No alert data received"}), 400

    # Apply policy
    alert = apply_policy(alert)

    # Store in DB
    db_alert = Alert(
        alert_name=alert.get("alert_name"),
        confidence_score=alert.get("confidence_score"),
        timestamp=alert.get("timestamp"),
        user=alert.get("user"),
        email=alert.get("email"),
        ip=alert.get("ip"),
        location=alert.get("location"),
        device=alert.get("device"),
        action=alert.get("action"),
        status=alert.get("status")
    )
    db.session.add(db_alert)
    db.session.commit()

    print(f"✅ Alert stored: {alert.get('alert_name')} for user {alert.get('user')}")

    # Forward to Mail Agent and SOC Receiver
    send_email_async(alert)
    send_to_soc(alert)

    return jsonify({"status": "processed", "alert": alert}), 200

# -------------------------------
# Ping endpoint
# -------------------------------
@app.route("/ping")
def ping():
    return "Responder is running (secure + policy playbook)"

# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=6000)
