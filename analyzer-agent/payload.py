import requests
import json
from datetime import datetime, timedelta, timezone
import random

# --- Timezone: UTC ---
UTC = timezone.utc

# --- Splunk HEC Configuration ---
SPLUNK_URL = "https://127.0.0.1:8088/services/collector"   # Splunk HEC endpoint
HEC_TOKEN = "31459979-84f0-4f36-a09e-83326691c5e5"          # Replace with your HEC token
INDEX = "zerotrust_logs"


def password_bruteforce():
    user = "bob@example.com"
    geo = "UK"
    devices = ["Chrome-Windows", "Firefox-Linux", "Edge-Windows", "Safari-Mac", "Opera-Windows"]

    base_time = datetime.now(UTC)   # UTC base time
    events = []

    for i in range(20):
        event_time = base_time + timedelta(seconds=i)
        payload = {
            "time": int(event_time.timestamp()),   # epoch (UTC)
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),  # human readable UTC
                "username": user,
                "Ip Address": f"192.168.1.{10}",
                "Geo Location": geo,
                "Request type": "login_attempt",
                "Response": "failed",
                "device": random.choice(devices)
            }
        }
        events.append(json.dumps(payload))

    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Password Bruteforce ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))


def credential_stuffing():
    user = "bob@example.com"
    geo = "UK"
    devices = ["Chrome-Windows", "Firefox-Linux", "Edge-Windows", "Safari-Mac", "Opera-Windows"]

    base_time = datetime.now(UTC)
    events = []

    for i in range(20):
        event_time = base_time + timedelta(seconds=i)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": f"192.168.1.{10+i}",
                "Geo Location": geo,
                "Request type": "login_attempt",
                "Response": "failed",
                "device": random.choice(devices)
            }
        }
        events.append(json.dumps(payload))

    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Credential Stuffing ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))


def suspicious_api_usage():
    user = "alice"
    ip = "203.0.113.45"
    endpoint = "/v1/exportData"
    geo = "US"
    device = "laptop"

    base_time = datetime.now(UTC)
    payload_sizes = [5, 8, 250]

    events = []

    for i, size in enumerate(payload_sizes):
        event_time = base_time + timedelta(seconds=i * 5)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": ip,
                "action": "api_call",
                "endpoint": endpoint,
                "size_MB": str(size),
                "location": geo,
                "device": device
            }
        }
        events.append(json.dumps(payload))

    # Add 100+ calls/min to simulate burst
    for j in range(100):
        event_time = base_time + timedelta(seconds=j % 60)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": ip,
                "action": "api_call",
                "endpoint": endpoint,
                "size_MB": str(random.choice([3, 6, 10])),
                "location": geo,
                "device": device
            }
        }
        events.append(json.dumps(payload))

    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Suspicious API Usage ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

def malware_bot_behaviour():
    ip = "10.0.0.50"
    geo = "CN"
    base_time = datetime.now(UTC)
    events = []

    # Case 1: High frequency (1 per second)
    for i in range(60):
        event_time = base_time + timedelta(seconds=i)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": "",
                "Ip Address": ip,
                "location": geo,
                "action": "api_call",
                "endpoint": "/v1/login",
                "Response": "failed",
                "device": ""
            }
        }
        events.append(json.dumps(payload))

    # Case 2: Weird User-Agent
    for j in range(10):
        event_time = base_time + timedelta(seconds=70 + j)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": "",
                "Ip Address": "10.0.0.51",
                "location": "RU",
                "action": "api_call",
                "endpoint": "/v1/admin",
                "Response": "forbidden",
                "device": "Unknown-Agent"
            }
        }
        events.append(json.dumps(payload))

    # Case 3: Many distinct endpoints (scanner)
    for k in range(25):
        event_time = base_time + timedelta(seconds=100 + k)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": "",
                "Ip Address": "10.0.0.52",
                "location": "BR",
                "action": "api_call",
                "endpoint": f"/v1/path{k}",
                "Response": "failed",
                "device": "curl/7.68.0"
            }
        }
        events.append(json.dumps(payload))

    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Malware / Bot Behaviour ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

def simulate_impossible_travel():
    base_time = datetime.now(timezone.utc)
    events = []

    # Case: User logs in from US then UK within 10 minutes
    user = "jdoe"
    locations = [("US", "203.0.113.50"), ("UK", "192.168.1.10")]
    
    for i, (loc, ip) in enumerate(locations):
        event_time = base_time + timedelta(minutes=i*10)  # 0 min, 10 min
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": ip,
                "Geo Location": loc,
                "device": "Laptop-1234",
                "action": "login_success",
                "Response": "success",
                "status": "success"
            }
        }
        print(payload)
        events.append(json.dumps(payload))

    # Optional: Add another user with normal travel (to test false negatives)
    normal_user_time = base_time + timedelta(minutes=5)
    payload_normal = {
        "time": int(normal_user_time.timestamp()),
        "sourcetype": "_json",
        "index": INDEX,
        "event": {
            "timestamp": normal_user_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "username": "asmith",
            "Ip Address": "198.51   .100.25",
            "Geo Location": "US",
            "device": "Desktop-5678",
            "action": "login_success",
            "Response": "success",
            "status": "success"
        }
    }
    events.append(json.dumps(payload_normal))

    # Send to Splunk HEC
    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Impossible Travel Simulation ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))


if __name__ == "__main__":
    password_bruteforce()

