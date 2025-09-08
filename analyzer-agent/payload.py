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
    user = "broh22012.it@rmkec.ac.in"
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
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),  
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
    user = "broh22012.it@rmkec.ac.in"
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



def privilege_escalation():
    user = "broh22012.it@rmkec.ac.in"   # Normal user (not admin)
    base_time = datetime.now(UTC)
    events = []

    # --- Suspicious admin actions by a normal user ---
    endpoints = ["/admin/delete", "/admin/update", "/admin/users/123"]

    for i, ep in enumerate(endpoints):
        event_time = base_time + timedelta(seconds=i * 10)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": "192.168.1.50",
                "Geo Location": "US",
                "endpoint": ep,               # <-- matches your SPL
                "Response": "success",        # <-- maps to 'status'
                "device": "Chrome-Windows"
            }
        }
        events.append(json.dumps(payload))

    # --- Send to Splunk HEC ---
    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Privilege Escalation ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

def account_takeover():
    user = "broh22012.it@rmkec.ac.in"
    base_time = datetime.now(UTC)
    events = []

    # 5+ failed logins from same IP/device/geo
    for i in range(5):
        event_time = base_time + timedelta(seconds=i * 5)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": "192.168.1.10",
                "Geo Location": "UK",
                "Request type": "login_attempt",
                "Response": "failed",
                "device": "Chrome-Windows"
            }
        }
        events.append(json.dumps(payload))

    # Success from NEW IP + NEW device + NEW geo (ATO trigger)
    event_time = base_time + timedelta(seconds=40)
    payload = {
        "time": int(event_time.timestamp()),
        "sourcetype": "_json",
        "index": INDEX,
        "event": {
            "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "username": user,
            "Ip Address": "203.0.113.55",       # new IP
            "Geo Location": "US",               # new Geo
            "Request type": "login_attempt",
            "Response": "success",              # sudden success
            "device": "Safari-Mac"              # new Device
        }
    }
    events.append(json.dumps(payload))

    # Optional: another ATO case (different user)
    for i in range(6):
        event_time = base_time + timedelta(minutes=1, seconds=i * 5)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": "broh22012.it@rmkec.ac.in",
                "Ip Address": "198.51.100.77",
                "Geo Location": "IN",
                "Request type": "login_attempt",
                "Response": "failed",
                "device": "Edge-Windows"
            }
        }
        events.append(json.dumps(payload))

    event_time = base_time + timedelta(minutes=2)
    payload = {
        "time": int(event_time.timestamp()),
        "sourcetype": "_json",
        "index": INDEX,
        "event": {
            "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "username": "broh22012.it@rmkec.ac.in",
            "Ip Address": "192.0.2.44",         # new IP
            "Geo Location": "SG",               # new Geo
            "Request type": "login_attempt",
            "Response": "success",
            "device": "Firefox-Android"         # new Device
        }
    }
    events.append(json.dumps(payload))

    # Send to Splunk HEC
    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Account Takeover (ATO) ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))


def privilege_escalation():
    user = "broh22012.it@rmkec.ac.in"   
    base_time = datetime.now(UTC)
    events = []

    # --- Suspicious admin actions by a normal user ---
    endpoints = ["/admin/delete", "/admin/update", "/admin/users/123"]

    for i, ep in enumerate(endpoints):
        event_time = base_time + timedelta(seconds=i * 10)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": "192.168.1.50",
                "Geo Location": "US",
                "endpoint": ep,               # <-- matches your SPL
                "Response": "success",        # <-- maps to 'status'
                "device": "Chrome-Windows"
            }
        }
        events.append(json.dumps(payload))

    # --- Send to Splunk HEC ---
    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Privilege Escalation ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

def network_anomalies():
    base_time = datetime.now(UTC) - timedelta(hours=1)  # 1 hour ago
    events = []

    # Simulate one IP scanning 60 unique ports
    ip_address = "203.0.113.10"
    for port in range(1000, 1060):  # 60 ports
        event_time = base_time + timedelta(seconds=random.randint(0, 300))
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "ip": ip_address,
                "port": port,
                "endpoint": f"/service/{port}",
                "action": "network_probe",
                "status": "blocked",
                "device": "N/A",
                "username": "N/A",
                "Geo Location": "US"
            }
        }
        events.append(json.dumps(payload))

    # Send all events to Splunk HEC
    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Network Anomalies ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

def data_exfiltration():
    base_time = datetime.now(UTC)
    events = []

    users = [
        {"username": "broh22012.it@rmkec.ac.in", "ip": "192.168.1.10", "device": "Chrome-Windows", "geo": "UK"},
        {"username": "diva22022.it@rmkec.ac.in", "ip": "192.168.1.20", "device": "Firefox-Linux", "geo": "US"}
    ]

    # Each user downloads multiple files
    download_sizes = [600, 200, 350, 1200]  # in MB

    for user in users:
        for i, size in enumerate(download_sizes):
            event_time = base_time + timedelta(minutes=i * 5)
            payload = {
                "time": int(event_time.timestamp()),
                "sourcetype": "_json",
                "index": INDEX,
                "event": {
                    "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "username": user["username"],
                    "Ip Address": user["ip"],
                    "Geo Location": user["geo"],
                    "Request type": "download",
                    "Response": "success",
                    "device": user["device"],
                    "size_MB": size
                }
            }
            events.append(json.dumps(payload))

    # --- Send all events to Splunk HEC ---
    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("Data Exfiltration ->", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))


if __name__ == "__main__":
    data_exfiltration()

