# from mcp.server.fastmcp import FastMCP
# from typing import List
# from phi.agent import Agent
# from phi.tools.email import EmailTools

# import os
# from phi.model.groq import Groq
# from dotenv import load_dotenv


# # In-memory mock database with 20 leave days to start
# employee_leaves = {
#     "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
#     "E002": {"balance": 20, "history": []}
# }

# # Create MCP server
# mcp = FastMCP("LeaveManager")

# # Tool: Check Leave Balance
# @mcp.tool()
# def get_leave_balance(employee_id: str) -> str:
#     """Check how many leave days are left for the employee"""
#     data = employee_leaves.get(employee_id)
#     if data:
#         return f"{employee_id} has {data['balance']} leave days remaining."
#     return "Employee ID not found."

# # Tool: Apply for Leave with specific dates
# @mcp.tool()
# def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
#     """
#     Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
#     """
#     if employee_id not in employee_leaves:
#         return "Employee ID not found."

#     requested_days = len(leave_dates)
#     available_balance = employee_leaves[employee_id]["balance"]

#     if available_balance < requested_days:
#         return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."

#     # Deduct balance and add to history
#     employee_leaves[employee_id]["balance"] -= requested_days
#     employee_leaves[employee_id]["history"].extend(leave_dates)

#     return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."


# # Resource: Leave history
# @mcp.tool()
# def get_leave_history(employee_id: str) -> str:
#     """Get leave history for the employee"""
#     data = employee_leaves.get(employee_id)
#     if data:
#         history = ', '.join(data['history']) if data['history'] else "No leaves taken."
#         return f"Leave history for {employee_id}: {history}"
#     return "Employee ID not found."

# # Resource: Greeting
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}! How can I assist you with leave management today?"



# @mcp.tool()
# def send_email_to_employees(email_id:str, message:str) -> str:  
#     model_id="llama-3.3-70b-versatile"
#     load_dotenv()
#     groq_api_key = os.getenv("GROQ_API_KEY")

#     sender_email = "kavirajmetech@gmail.com"
#     sender_name = "kaviyarasu"
#     sender_passkey = os.getenv("GMAIL_PASSKEY")

#     agent = Agent(
#         name="Web Search Agent",
#         role="Send email",
#         model=Groq(id=model_id, api_key=groq_api_key),
#         tools=[
#             EmailTools(
#                 receiver_email=email_id,
#                 sender_email=sender_email,
#                 sender_name=sender_name,
#                 sender_passkey=sender_passkey,
#             )
#         ],
#         markdown=True
#     )
#     agent.print_response(f"{message} send mail only once and retun the control")
#     return "mail sent successfully"

# if __name__ == "__main__":
#     mcp.run()
from mcp.server.fastmcp import FastMCP
from typing import List
from phi.agent import Agent
from phi.tools.email import EmailTools

import os
from phi.model.groq import Groq
from dotenv import load_dotenv
import imaplib
import email
from email.header import decode_header

# Load environment variables
load_dotenv()
GMAIL_PASSKEY = os.getenv("GMAIL_PASSKEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


mcp = FastMCP("LeaveManager")

# --- Email Tools ---
@mcp.tool()
def send_email_to_employees(email_id: str, message: str) -> str:
    """Send email using the agent."""
    model_id = "llama-3.3-70b-versatile"
    agent = Agent(
        name="Email Agent",
        role="Send and categorize emails",
        model=Groq(id=model_id, api_key=GROQ_API_KEY),
        tools=[
            EmailTools(
                receiver_email=email_id,
                sender_email="kavirajmetech@gmail.com",
                sender_name="kaviyarasu",
                sender_passkey=GMAIL_PASSKEY,
            )
        ],
        markdown=True
    )
    agent.print_response(f"{message} send mail only once and return control")
    return "Mail sent successfully"


@mcp.tool()
def fetch_and_categorize_emails() -> str:
    """Connects to Gmail, fetches new emails, and categorizes them"""
    imap_host = "imap.gmail.com"
    email_user = "kavirajmetech@gmail.com"
    email_pass = GMAIL_PASSKEY

    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    if not email_ids:
        return "No new emails."

    categorized_emails = {"Work": [], "Personal": [], "Other": []}

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")

                # Simple categorization based on keywords
                if any(k in subject.lower() for k in ["leave", "meeting", "project"]):
                    categorized_emails["Work"].append((from_, subject))
                elif any(k in subject.lower() for k in ["friend", "party", "personal"]):
                    categorized_emails["Personal"].append((from_, subject))
                else:
                    categorized_emails["Other"].append((from_, subject))

    return f"Categorized new emails: {categorized_emails}"


if __name__ == "__main__":
    mcp.run()
