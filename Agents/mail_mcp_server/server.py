from flask import Flask, request, jsonify
from phi.agent import Agent
from phi.tools.email import EmailTools
from phi.model.groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

def send_email_with_groq(recipient: str, alert_context: str) -> str:
    """
    Compose a professional SOC alert email using Groq + EmailTools and send it.
    Returns a descriptive status message.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    sender_email = os.getenv("GMAIL_SENDER_EMAIL")
    sender_name = os.getenv("GMAIL_SENDER_NAME", "Z3r0Trust Alerting System")
    sender_passkey = os.getenv("GMAIL_PASSKEY")

    if not groq_api_key or not sender_email or not sender_passkey:
        raise ValueError("Missing required environment variables for Groq/Gmail integration")

    # Initialize agent
    agent = Agent(
        name="Email Agent",
        role="Compose and send professional SOC alert emails with clarity",
        model=Groq(id="llama-3.3-70b-versatile", api_key=groq_api_key),
        tools=[
            EmailTools(
                receiver_email=recipient,
                sender_email=sender_email,
                sender_name=sender_name,
                sender_passkey=sender_passkey,
            )
        ],
        markdown=True,
    )

    # Compose professional email
    prompt = f"""
You are a SOC email assistant. Compose a concise, professional security alert email using the information below.
Include a clear subject, actionable description, and context for SOC analysts.

Alert details:
{alert_context}

Rules:
- Use professional tone.
- Summarize key points in bullet format if needed.
- Include action recommendation at the end.
- Do not send multiple emails; send only once.
- Return confirmation of content after sending.
"""

    agent.print_response(prompt)

    # Return confirmation message
    return f"✅ Email successfully composed and sent to {recipient} with alert context."


@app.route("/email", methods=["POST"])
def email_endpoint():
    try:
        data = request.get_json(force=True)

        # Extract alert data
        user = data.get("user", "Unknown")
        alert_name = data.get("alert_name", "Unknown Alert")
        confidence = data.get("confidence_score", "N/A")
        ip = data.get("ip", "N/A")
        timestamp = data.get("timestamp", "N/A")
        recipient = data.get("email", "soc_team@example.com")

        # Prepare raw alert context for Groq
        alert_context = f"""
User: {user}
Alert: {alert_name}
Confidence Score: {confidence}
IP Address: {ip}
Time: {timestamp}
"""

        result = send_email_with_groq(recipient, alert_context)

        return jsonify({
            "status": "success",
            "message": result,
            "alert_details": {
                "user": user,
                "alert_name": alert_name,
                "confidence_score": confidence,
                "ip": ip,
                "timestamp": timestamp,
                "recipient": recipient
            }
        }), 200

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route("/ping", methods=["GET"])
def ping():
    return "Mail Agent is running!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6001, debug=True)
