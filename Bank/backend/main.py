from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from descope import DescopeClient
import requests
import user_agents
import time
import mysql.connector
from decimal import Decimal
from datetime import datetime

# ----------------------------
# Environment / Config
# ----------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=False,  # must be False with "*"
    allow_methods=["*"],
    allow_headers=["*"]
)


# Descope Setup
DESCOPE_PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

# ----------------------------
# DB Connection Function
# ----------------------------
def get_db():
    return mysql.connector.connect(
        host="34.93.101.129",
        user="root",
        password="ZeroTrust@123",
        database="bank"
    )

# ----------------------------
# Helper Functions
# ----------------------------
def get_location(ip: str) -> str:
    if ip in ("127.0.0.1", "localhost"):
        try:
            ip = requests.get("https://api.ipify.org").text
        except:
            return "Localhost / Unknown"
    try:
        geo = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return f"{geo.get('country')}/{geo.get('region')}/{geo.get('city')}"
    except:
        return "Unknown"

def parse_device(user_agent_str: str) -> str:
    ua = user_agents.parse(user_agent_str)
    return f"{ua.browser.family} {ua.browser.version_string} on {ua.os.family} {ua.os.version_string} ({ua.device.family or 'Unknown'})"

# ----------------------------
# Security - Session JWT Verification
# ----------------------------
def get_current_user(
    authorization: str = Header(None),
    x_user_email: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: No token provided")

    token = authorization.split(" ")[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: Empty token")

    if not x_user_email:
        raise HTTPException(status_code=401, detail="Unauthorized: No user email provided")

    # ✅ Return the real user email passed from frontend
    return {"email": x_user_email}

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: No token provided")

    token = authorization.split(" ")[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: Empty token")

    # ✅ If any token exists, allow request
    return {"email": "diva22022.it@rmkec.ac.in"}

    # Just check if Authorization header is present
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # Extract token (but don't validate with Descope)
    token = authorization.split(" ")[1]

    # Allow if token exists
    if token:
        return {"email": "demo_user@example.com"}  # Mock user info
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ----------------------------
# Models
# ----------------------------
class LoginPayload(BaseModel):
    email: str
    password: str
    request_type: str

class FundTransferRequest(BaseModel):
    from_account_number: str
    to_account_number: str
    amount: float

# ----------------------------
# API Routes
# ----------------------------

@app.get("/")
def health():
    return "hello"
@app.post("/api/auth/login")
async def login_with_email(payload: LoginPayload, request: Request):
    try:
        login_response = descope_client.password.sign_in(
            login_id=payload.email,
            password=payload.password
        )

        session_token_data = login_response.get("sessionToken", {})
        session_jwt = session_token_data.get("jwt")

        if not session_jwt:
            return {"status": "failure", "message": "No JWT returned"}

        user = login_response.get("user", {})
        ip = request.client.host
        geo = get_location(ip)
        device = parse_device(request.headers.get("user-agent", "unknown"))

        attributes = {
            "timestamp": int(time.time()),
            "email": user.get("email", payload.email),
            "ip": ip,
            "geo": geo,
            "device": device,
            "request_type": payload.request_type,
            "response": "success"
        }

        return {
            "status": "success",
            "session_jwt": session_jwt,
            "user_id": user.get("email", payload.email),
            "attributes": attributes
        }

    except Exception as e:
        return {"status": "failure", "message": str(e)}

# ----------------------------
# Protected APIs
# ----------------------------
@app.get("/api/balance")
def get_balance(current_user: dict = Depends(get_current_user)):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        email = current_user["email"]

        cursor.execute("""
            SELECT a.balance
            FROM users u
            JOIN accounts a ON a.user_id = u.id
            WHERE u.email = %s
            LIMIT 1
        """, (email,))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return {"balance": float(result["balance"])}

        raise HTTPException(status_code=404, detail="Account not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/transactions")
def get_transactions(current_user: dict = Depends(get_current_user)):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        email = current_user["email"]

        cursor.execute("""
            SELECT t.amount, t.created_at,
                CASE 
                    WHEN t.from_account_id = a.id THEN 'Debit'
                    ELSE 'Credit'
                END AS type
            FROM transactions t
            JOIN accounts a ON (t.from_account_id = a.id OR t.to_account_id = a.id)
            JOIN users u ON a.user_id = u.id
            WHERE u.email = %s
            ORDER BY t.created_at DESC
            LIMIT 10
        """, (email,))
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            {
                "description": row["type"],
                "amount": float(row["amount"]),
                "date": row["created_at"].strftime("%Y-%m-%d")
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/transfer")
def transfer_funds(request: FundTransferRequest, user: dict = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (request.from_account_number,))
        from_account = cursor.fetchone()

        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (request.to_account_number,))
        to_account = cursor.fetchone()

        if not from_account or not to_account:
            raise HTTPException(status_code=404, detail="Invalid account number(s)")

        from_balance = Decimal(from_account["balance"])
        to_balance = Decimal(to_account["balance"])
        transfer_amount = Decimal(str(request.amount))

        if from_balance < transfer_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        new_from_balance = from_balance - transfer_amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_from_balance, from_account["id"]))

        new_to_balance = to_balance + transfer_amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_to_balance, to_account["id"]))

        cursor.execute("""
            INSERT INTO transactions (from_account_id, to_account_id, amount, status, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (from_account["id"], to_account["id"], str(transfer_amount), "success", datetime.now()))

        conn.commit()

        return {
            "status": "success",
            "message": f"Transferred ₹{transfer_amount} from {request.from_account_number} to {request.to_account_number}",
            "transaction_id": cursor.lastrowid
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
