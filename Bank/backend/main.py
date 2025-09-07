from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from descope import DescopeClient
import requests
import user_agents
import time
import mysql.connector
from decimal import Decimal   # ✅ Fix 1
from datetime import datetime  # ✅ Fix 2

import os

# ----------------------------
# Environment / Config
# ----------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Descope Setup
DESCOPE_PROJECT_ID = "P32Dj1SFaOxhwz4v0i9D6jseEJny"
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)
resp = descope_client.password.sign_in(login_id="diva22022.it@rmkec.ac.in", password="123qwe!@#QWE")
print(resp)

# ----------------------------
# DB Connection Function
# ----------------------------
def get_db():
    return mysql.connector.connect(
        host="34.93.101.129",     # Replace if hosted
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
# Models
# ----------------------------
class LoginPayload(BaseModel):
    email: str
    password: str
    request_type: str

# ----------------------------
# API Routes
# ----------------------------

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

@app.get("/api/balance")
def get_balance(user_id: str):
    try:
        print(f"Getting balance for user_id: '{user_id}'")

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # TEMP: Print all emails for debugging
        cursor.execute("SELECT email FROM users")
        all_users = cursor.fetchall()
        print("All emails in DB:")
        for u in all_users:
            print(f"-> '{u['email']}'")

        # Clean input email
        clean_email = user_id.strip()

        cursor.execute("""
            SELECT a.balance
            FROM users u
            JOIN accounts a ON a.user_id = u.id
            WHERE u.id = 1
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            print(f"Balance found: {result['balance']}")
            return {"balance": float(result["balance"])}

        print("No account found")
        raise HTTPException(status_code=404, detail="Account not found")

    except Exception as e:
        print(f"Error in /api/balance: {e}")
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/api/transactions")
def get_transactions(user_id: str):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
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
        """, (user_id,))
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
    
class FundTransferRequest(BaseModel):
    from_account_number: str
    to_account_number: str
    amount: float

# --- API Route ---
@app.post("/api/transfer")
def transfer_funds(request: FundTransferRequest):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Get accounts
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (request.from_account_number,))
        from_account = cursor.fetchone()

        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (request.to_account_number,))
        to_account = cursor.fetchone()

        if not from_account or not to_account:
            raise HTTPException(status_code=404, detail="Invalid account number(s)")

        # 2. Convert balances safely
        from_balance = Decimal(from_account["balance"])
        to_balance = Decimal(to_account["balance"])
        transfer_amount = Decimal(str(request.amount))

        # 3. Check balance
        if from_balance < transfer_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # 4. Update balances
        new_from_balance = from_balance - transfer_amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_from_balance, from_account["id"]))

        new_to_balance = to_balance + transfer_amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_to_balance, to_account["id"]))

        # 5. Insert transaction log
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