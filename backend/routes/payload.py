from flask import Blueprint,Flask, jsonify
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

payload_bp = Blueprint("payload_bp", __name__)

app = Flask(__name__)

def send_to_splunk(events):
    body = "\n".join(events)
    headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}
    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        return {"status_code": response.status_code, "response": response.text}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
@payload_bp.route("/password_bruteforce", methods=["POST"])
def password_bruteforce_endpoint():
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
                "Ip Address": f"192.168.1.{10}",
                "Geo Location": geo,
                "Request type": "login_attempt",
                "Response": "failed",
                "device": random.choice(devices)
            }
        }
        events.append(json.dumps(payload))

    result = send_to_splunk(events)
    return jsonify(result)


@payload_bp.route("/credential_stuffing", methods=["POST"])
def credential_stuffing_endpoint():
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

    result = send_to_splunk(events)
    return jsonify(result)

@payload_bp.route("/suspicious_api_usage", methods=["POST"])
def suspicious_api_usage_endpoint():
    user = "alice"
    ip = "203.0.113.45"
    endpoint = "/v1/exportData"
    geo = "US"
    device = "laptop"

    base_time = datetime.now(UTC)
    payload_sizes = [5, 8, 250]

    events = []

    for i, size in enumerate(payload_sizes):
        event_time = base_time + timedelta(seconds=i*5)
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

    result = send_to_splunk(events)
    return jsonify(result)



@payload_bp.route("/malware_bot_behaviour", methods=["POST"])
def malware_bot_behaviour_endpoint():
    ip = "10.0.0.50"
    geo = "CN"
    base_time = datetime.now(UTC)
    events = []

    # High frequency
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

    result = send_to_splunk(events)
    return jsonify(result)


@payload_bp.route("/simulate_impossible_travel", methods=["POST"])
def simulate_impossible_travel_endpoint():
    base_time = datetime.now(UTC)
    events = []

    user = "jdoe"
    locations = [("US", "203.0.113.50"), ("UK", "192.168.1.10")]

    for i, (loc, ip) in enumerate(locations):
        event_time = base_time + timedelta(minutes=i*10)
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
        events.append(json.dumps(payload))

    result = send_to_splunk(events)
    return jsonify(result)



@payload_bp.route("/privilege_escalation", methods=["POST"])
def privilege_escalation_endpoint():
    user = "broh22012.it@rmkec.ac.in"
    base_time = datetime.now(UTC)
    events = []

    endpoints = ["/admin/delete", "/admin/update", "/admin/users/123"]

    for i, ep in enumerate(endpoints):
        event_time = base_time + timedelta(seconds=i*10)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": "192.168.1.50",
                "Geo Location": "US",
                "endpoint": ep,
                "Response": "success",
                "device": "Chrome-Windows"
            }
        }
        events.append(json.dumps(payload))

    result = send_to_splunk(events)
    return jsonify(result)



@payload_bp.route("/account_takeover", methods=["POST"])
def account_takeover_endpoint():
    user = "broh22012.it@rmkec.ac.in"
    base_time = datetime.now(UTC)
    events = []

    # 5+ failed logins
    for i in range(5):
        event_time = base_time + timedelta(seconds=i*5)
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

    # Success from new IP/device/geo
    event_time = base_time + timedelta(seconds=40)
    payload = {
        "time": int(event_time.timestamp()),
        "sourcetype": "_json",
        "index": INDEX,
        "event": {
            "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "username": user,
            "Ip Address": "203.0.113.55",
            "Geo Location": "US",
            "Request type": "login_attempt",
            "Response": "success",
            "device": "Safari-Mac"
        }
    }
    events.append(json.dumps(payload))

    # Another ATO case (failed logins)
    for i in range(6):
        event_time = base_time + timedelta(minutes=1, seconds=i*5)
        payload = {
            "time": int(event_time.timestamp()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": {
                "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "username": user,
                "Ip Address": "198.51.100.77",
                "Geo Location": "IN",
                "Request type": "login_attempt",
                "Response": "failed",
                "device": "Edge-Windows"
            }
        }
        events.append(json.dumps(payload))

    # Success from another new IP/device/geo
    event_time = base_time + timedelta(minutes=2)
    payload = {
        "time": int(event_time.timestamp()),
        "sourcetype": "_json",
        "index": INDEX,
        "event": {
            "timestamp": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "username": user,
            "Ip Address": "192.0.2.44",
            "Geo Location": "SG",
            "Request type": "login_attempt",
            "Response": "success",
            "device": "Firefox-Android"
        }
    }
    events.append(json.dumps(payload))

    result = send_to_splunk(events)
    return jsonify(result)


@payload_bp.route("/network_anomalies", methods=["POST"])
def network_anomalies_endpoint():
    base_time = datetime.now(UTC) - timedelta(hours=1)
    events = []

    ip_address = "203.0.113.10"
    for port in range(1000, 1060):
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

    result = send_to_splunk(events)
    return jsonify(result)


@payload_bp.route("/data_exfiltration", methods=["POST"])
def data_exfiltration_endpoint():
    base_time = datetime.now(UTC)
    events = []

    users = [
        {"username": "broh22012.it@rmkec.ac.in", "ip": "192.168.1.10", "device": "Chrome-Windows", "geo": "UK"},
        {"username": "diva22022.it@rmkec.ac.in", "ip": "192.168.1.20", "device": "Firefox-Linux", "geo": "US"}
    ]
    download_sizes = [600, 200, 350, 1200]

    for user in users:
        for i, size in enumerate(download_sizes):
            event_time = base_time + timedelta(minutes=i*5)
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

    result = send_to_splunk(events)
    return jsonify(result)
