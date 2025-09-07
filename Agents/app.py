from typing import List, Union
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
import requests
from db_controller_agent import db_controller_agent
from app_helper_functions import apply_policy
from cache import  cache_cleaner, is_duplicate
from alert_handler_agent import alert_handler_agent
from mail_sender_agent import mail_sender_agent
from server import send_email,authenticator,retrieve_unread_emails,tools_list
import google.generativeai as genai
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

nest_asyncio.apply()

PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"
descope = DescopeClient(project_id=PROJECT_ID)

server_params = StdioServerParameters(
    command="python",  
    args=["server.py"],  
)



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
    # async def run():
    #     try:
    #         async with stdio_client(server_params) as (read_stream, write_stream):
    #             async with ClientSession(read_stream, write_stream) as session:
    #                 await session.initialize()
    #                 tools_result = await session.list_tools()
    #                 print("Available tools:")
    #                 for tool in tools_result.tools:
    #                     print(f"  - {tool.name}: {tool.description}")
    #                 return {"tools": [t.dict() for t in tools_result.tools]}
    #     except Exception as e:
    #         print(f"❌ Connection error: {e}")
    #         return {"tools": "connection error"}

    # return asyncio.run(run())
    return {"tools":tools_list()}


# --------- Send email via MCP tool ---------

@app.route("/send-email", methods=["POST"])
def send_email_route():
    data = request.get_json()
    email_id = data.get("email_id")
    message = data.get("message")
    print(email_id, message)

    success = mail_sender_agent(email_id, message)

    return jsonify({"status": "sent" if success else "failed"})


@app.route("/get-email", methods=["GET"])
def get_email():
    async def run():
        # async with Client(MCP_SERVER_URL) as client:
        #     result = await client.call_tool("retrieve_unread_emails")
        #     print(result)
        #     return {"result": result}
        result=retrieve_unread_emails()
    return asyncio.run(run())


# --------- Appeal form ---------
@app.route("/appeal", methods=["GET"])
def get_appeal():
    return render_template("appeal.html")

@app.route("/appealrequest", methods=["POST"])
def handle_appeal():
    emailid  = request.form.get("email")
    subject1 = request.form.get("subject1")
    content1 = request.form.get("content1")
    
    print("Appeals received:")
    print(f"1: {subject1} - {content1}")

    prompt = f"add the entry to the table 'appeal'(id	int,subject	varchar(200), content	varchar(2000), status	tinyint(1)), here the subject {subject1}, content {content1}, status 1"
    db_controller_agent(prompt=prompt)

    prompt = f"mail to {emailid} as appeal recieved successfully, forwarded to our AI agent and SOC, will get back to you within two working days, thank you, ZeroTrust team"
    mail_sender_agent(emailid,prompt)

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



@app.route("/webhook",methods=["post"])
def webhook():
    try:
        alerts=request.get_json().get("result")
        
        print(alerts)
        # if isinstance(alerts, dict):
        #     alerts = [alerts]

        # print(json.dumps(alerts, indent=4))  # pretty print

        # processed, suppressed = [], []

        # for alert in alerts:
        print("reached inside")
        print(alerts)
        # gemini_response = gemini_model.generate_content(f"{alert}, generate this report as a detailed summary")
        # narrative_summary = gemini_response.text.strip()
        # alert['summary']=narrative_summary
        # alert = alert["result"]
        # alert_id = alerts.get("alert_id")
        user=alerts.get("user")
        alert_name = alerts.get("alert_name")
        # if not alert_id or not alert_name:
        #     continue
        # if is_duplicate(alert_id, alert_name):
        #     suppressed.append(alert_id)
        #     print("XXXXXXXXXX Duplicate detected")
        #     continue

        # alert_data = apply_policy(alert)
        # processed.append(alert_data)

        print("reached storage post")
        url = "http://localhost:5000/api/alerts/fetch"

        response = requests.post(url, json=alerts)

        print(response)
        # return {"res": str(response)}
        prompt = (
            f"send email to {user} that Dear {user} Our monitoring detected suspicious activity: {alerts} Your account may be blocked if this continues.Regards, ZeroTrust Security Monitoring Team"
        )
        print("alert reached mail agent")
        mail_sender_agent(alerts.get("user"),prompt)
        print(f"✅ Processed alert: {alert_name} for {alerts.get('user')}")
        print("\nreached alert agent\n")
        alert_handler_agent(alert=alerts)
        return {"result":"success"}
        # return {
        #     "status": "done",
        #     "processed_count": len(processed),
        #     "suppressed_count": len(suppressed),
        #     "processed": processed,
        #     "suppressed": suppressed,
        # }
    except Exception as e:
        print("exception recieved")
        print(e)
        return {'e':str(e)}

# --------- Background tasks ---------
# @app.before_first_request
# def start_background_tasks():
#     asyncio.create_task(cache_cleaner())



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2222, debug=True)

