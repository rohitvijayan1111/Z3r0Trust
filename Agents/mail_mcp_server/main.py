from mcp.server.fastmcp import FastMCP
from phi.agent import Agent
from phi.tools.email import EmailTools
import os
from phi.model.groq import Groq
from dotenv import load_dotenv
import imaplib
import email
# from email.header import decode_header

# Load environment variables
load_dotenv()
GMAIL_PASSKEY = os.getenv("GMAIL_PASSKEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


mcp = FastMCP("LeaveManager")

# --- Email Tools ---
@mcp.tool()
def send_email_to_employees(email_id: str, message: str) -> str:
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
    return "mail sent successfully"

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
