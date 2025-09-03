import os
from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from anomaly_rules import detect_anomalies
from splunk_client import send_to_splunk
from auth import verify_jwt 

load_dotenv()

app = FastAPI(title="Detector Agent")

@app.get("/")
async def root():
    return {"message": "Detector Agent is running"}

@app.post("/detect")
async def detect(event: dict, user_id: str = Depends(verify_jwt)):
    """
    Only authenticated users (via Descope JWT) can send events.
    """
    try:
        anomalies = detect_anomalies(event)
        if anomalies:
            send_to_splunk(event, anomalies)
            return {"status": "suspicious", "user": user_id, "anomalies": anomalies}
        return {"status": "normal", "user": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid event format: {e}")
