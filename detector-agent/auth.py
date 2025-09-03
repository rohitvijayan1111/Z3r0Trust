import os
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from descope import DescopeClient
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("DESCOPE_PROJECT_ID")

client = DescopeClient(project_id=PROJECT_ID)

# FastAPI security
bearer_scheme = HTTPBearer()

def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    try:
        jwt = client.validate_jwt(token)  
        return jwt["sub"]  
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {e}")
