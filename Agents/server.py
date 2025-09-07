# import asyncio
# import logging
# import os
# from fastmcp import FastMCP
# from phi.agent import Agent
# from phi.tools.email import EmailTools
# from phi.model.groq import Groq
# from dotenv import load_dotenv
# from descope import DescopeClient
# from fastapi import HTTPException
# import imaplib
# import email
# from email.header import decode_header
# from typing import List

# model_id="llama-3.3-70b-versatile"
# load_dotenv()

# logger = logging.getLogger(__name__)
# logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# mcp = FastMCP("MCP Server on Cloud Run")

# descope_client = DescopeClient(project_id=os.getenv("DESCOPE_PROJECT_ID"))

# def validate_token(access_key: str):
   
#     """Helper to validate a JWT with Descope"""
#     try:
#         jwt_response = descope_client.exchange_access_key(access_key=access_key)
#         token = jwt_response.get('sessionToken', {}).get('jwt')
#         if not token:
#             return False
#         return True
#     except Exception as e:
#         raise HTTPException(status_code=403, detail=f"Invalid token: {e}")

# # ✅ Authenticator tool
# @mcp.tool()
# def authenticator(access_key: str) -> bool:
#     """
#     Validate a Descope session token.
    
#     Args:
#         token: JWT session token
    
#     Returns:
#         True if authenticated, False otherwise
#     """
#     return validate_token(access_key=access_key)

# @mcp.tool()
# def send_email_to_employees(email_id:str, message:str) -> str: 
#     """
#     The function send mail to the given email_id and with the given message 
#     """ 
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
#     agent.print_response(f"{message} send mail only once")
#     return "mail sent successfully"


# @mcp.tool()
# def retrieve_unread_emails() -> List[str]:
#     """
#     Retrieve last 5 unread emails from the sender Gmail inbox.

#     Returns:
#         List of last 5 unread email subjects and snippets
#     """
#     sender_email = "kavirajmetech@gmail.com"
#     sender_passkey = os.getenv("GMAIL_PASSKEY")

#     # Connect to Gmail IMAP
#     imap = imaplib.IMAP4_SSL("imap.gmail.com")
#     try:
#         imap.login(sender_email, sender_passkey)
#     except imaplib.IMAP4.error as e:
#         return [f"Failed to login: {e}"]

#     # Select INBOX
#     imap.select("INBOX")

#     # Search for unread emails
#     status, messages = imap.search(None, "UNSEEN")
#     if status != "OK" or not messages[0]:
#         imap.logout()
#         return ["No unread emails found."]

#     mail_ids = messages[0].split()
#     last_ids = mail_ids[-5:]  # Last 5 unread emails

#     result_emails = []
#     for mail_id in reversed(last_ids):
#         status, msg_data = imap.fetch(mail_id, "(RFC822)")
#         if status != "OK":
#             continue
#         for response_part in msg_data:
#             if isinstance(response_part, tuple):
#                 msg = email.message_from_bytes(response_part[1])
#                 # Decode subject
#                 subject, encoding = decode_header(msg["Subject"])[0]
#                 if isinstance(subject, bytes):
#                     subject = subject.decode(encoding or "utf-8", errors="ignore")
#                 # Get body snippet
#                 body = ""
#                 if msg.is_multipart():
#                     for part in msg.walk():
#                         if part.get_content_type() == "text/plain":
#                             body = part.get_payload(decode=True).decode(errors="ignore")
#                             break
#                 else:
#                     body = msg.get_payload(decode=True).decode(errors="ignore")
#                 snippet = body[:100]  # first 100 chars
#                 result_emails.append(f"Subject: {subject} | Snippet: {snippet}")

#     imap.logout()
#     return result_emails

# # ✅ Run MCP server
# if __name__ == "__main__":
#     # port = int(os.getenv("PORT", 8080))
#     # logger.info(f"🚀 MCP server started on port {port}")
#     asyncio.run(
#         mcp.run_async(
#             transport="stdio"
#         )
#     )



import asyncio
import logging
import os
from fastmcp import FastMCP
from phi.agent import Agent
from phi.tools.email import EmailTools
from phi.model.groq import Groq
from dotenv import load_dotenv
from descope import DescopeClient
from fastapi import HTTPException
import imaplib
import email
from email.header import decode_header
from typing import List

model_id="llama-3.3-70b-versatile"
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# mcp = FastMCP("MCP Server on Cloud Run")

descope_client = DescopeClient(project_id=os.getenv("DESCOPE_PROJECT_ID"))
def tools_list():
    return ["validate_token","authenticator", "send_email","retrieve_unread_email"]

def validate_token(access_key: str):
   
    """Helper to validate a JWT with Descope"""
    try:
        jwt_response = descope_client.exchange_access_key(access_key=access_key)
        token = jwt_response.get('sessionToken', {}).get('jwt')
        if not token:
            return False
        return True
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Invalid token: {e}")

def authenticator(access_key: str) -> bool:
    """
    Validate a Descope session token.
    
    Args:
        token: JWT session token
    
    Returns:
        True if authenticated, False otherwise
    """
    return validate_token(access_key=access_key)

def send_email(email_id: str, message: str) -> bool: 
    """
    Send mail to the given email_id with the given message 
    """ 
    try:
        model_id = "llama-3.3-70b-versatile"
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")

        sender_email = "kavirajmetech@gmail.com"
        sender_name = "kaviyarasu"
        sender_passkey = os.getenv("GMAIL_PASSKEY")

        agent = Agent(
            name="Email Agent",
            role="Send email",
            model=Groq(id=model_id, api_key=groq_api_key),
            tools=[
                EmailTools(
                    receiver_email=email_id,
                    sender_email=sender_email,
                    sender_name=sender_name,
                    sender_passkey=sender_passkey,
                )
            ],
            markdown=True
        )
        agent.print_response(f"{message} send mail only once")
        return True
    except Exception as e:
        return False
    
def retrieve_unread_emails() -> List[str]:
    """
    Retrieve last 5 unread emails from the sender Gmail inbox.

    Returns:
        List of last 5 unread email subjects and snippets
    """
    sender_email = "kavirajmetech@gmail.com"
    sender_passkey = os.getenv("GMAIL_PASSKEY")

    # Connect to Gmail IMAP
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        imap.login(sender_email, sender_passkey)
    except imaplib.IMAP4.error as e:
        return [f"Failed to login: {e}"]

    # Select INBOX
    imap.select("INBOX")

    # Search for unread emails
    status, messages = imap.search(None, "UNSEEN")
    if status != "OK" or not messages[0]:
        imap.logout()
        return ["No unread emails found."]

    mail_ids = messages[0].split()
    last_ids = mail_ids[-5:]  # Last 5 unread emails

    result_emails = []
    for mail_id in reversed(last_ids):
        status, msg_data = imap.fetch(mail_id, "(RFC822)")
        if status != "OK":
            continue
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # Decode subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")
                # Get body snippet
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                snippet = body[:100]  # first 100 chars
                result_emails.append(f"Subject: {subject} | Snippet: {snippet}")

    imap.logout()
    return result_emails

# # ✅ Run MCP server
# if __name__ == "__main__":
#     # port = int(os.getenv("PORT", 8080))
#     # logger.info(f"🚀 MCP server started on port {port}")
#     asyncio.run(
#         mcp.run_async(
#             transport="stdio"
#         )
#     )
