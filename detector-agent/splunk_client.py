import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPLUNK_HEC_URL = os.getenv("SPLUNK_HEC_URL")
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")

def send_to_splunk(event, anomalies):
    headers = {"Authorization": f"Splunk {SPLUNK_HEC_TOKEN}"}
    payload = {
        "event": {
            "log": event,
            "anomalies": anomalies
        }
    }
    try:
        r = requests.post(SPLUNK_HEC_URL, json=payload, headers=headers, verify=False)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send to Splunk: {e}")
        return False
