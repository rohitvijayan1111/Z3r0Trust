from flask import Flask, request, jsonify, render_template, Response
from pydantic import BaseModel
import os
from fastmcp import Client
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from datetime import datetime
from descope import DescopeClient
import asyncio
import nest_asyncio
from db_controller_agent import db_controller_agent
from app_helper_functions import apply_policy
from cache import  cache_cleaner
from alert_handler_agent import alert_handler_agent
from mail_sender_agent import mail_sender_agent


nest_asyncio.apply()

PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
descope = DescopeClient(project_id=PROJECT_ID)

server_params = StdioServerParameters(
    command="python",  # The command to run your server
    args=["server.py"],  # Arguments to the command
)

load_dotenv()

app = Flask(__name__)

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
DESCOPE_ACCESS_KEY = os.getenv("DESCOPE_ACCESS_KEY")

# --------- Health check ---------
@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Hello MCP!"})


@app.route("/hi", methods=["GET"])
def hi():
    return jsonify({"message": " hi Hello MCP!"})


# --------- List available tools ---------
@app.route("/tools", methods=["GET"])
def list_tools():
    async def run():
        try:
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()
                    print("Available tools:")
                    for tool in tools_result.tools:
                        print(f"  - {tool.name}: {tool.description}")
                    return {"tools": [t.dict() for t in tools_result.tools]}
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return {"tools": "connection error"}

    return asyncio.run(run())


# --------- Send email via MCP tool ---------
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    email_id = data.get("email_id")
    message = data.get("message")
    print(email_id, message)
    mail_sender_agent(email_id, message)
    return jsonify({"status": "sent"})


@app.route("/get-email", methods=["GET"])
def get_email():
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("retrieve_unread_emails")
            print(result)
            return {"result": result}
    return asyncio.run(run())


# --------- Appeal form ---------
@app.route("/appeal", methods=["GET"])
def get_appeal():
    return render_template("appeal.html")


@app.route("/appealrequest", methods=["POST"])
def handle_appeal():
    subject1 = request.form.get("subject1")
    content1 = request.form.get("content1")

    print("Appeals received:")
    print(f"1: {subject1} - {content1}")

    prompt = "add the entry to the table 'appeal'(id, subject, content, response_id, status) "
    db_controller_agent(prompt=prompt)

    # Returning JS alert to close window
    return Response("""
        <html>
            <body>
                <script>
                    alert("Appeals submitted successfully!");
                    window.close();
                </script>
            </body>
        </html>
    """, mimetype="text/html")


# --------- Webhook ---------
@app.route("/webhook", methods=["POST"])
def webhook():
    alerts = request.get_json()
    print(alerts)

    processed, suppressed = [], []

    # (original suppression & processing logic is kept commented in your code)

    return jsonify({
        "status": "done",
        "processed_count": len(processed),
        "suppressed_count": len(suppressed),
        "processed": processed,
        "suppressed": suppressed,
    })


# --------- Background tasks ---------
@app.before_first_request
def start_background_tasks():
    asyncio.create_task(cache_cleaner())



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)