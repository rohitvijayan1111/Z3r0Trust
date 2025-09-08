from flask import Blueprint, jsonify, request
from models.proxy_routes_model import ProxyRoute
import requests   # ✅ Needed for forwarding
import user_agents
import time
import json

proxy_bp = Blueprint("proxy_routes", __name__)

# --- Splunk HEC Configuration ---
SPLUNK_URL = "https://127.0.0.1:8088/services/collector"   # Splunk HEC endpoint
HEC_TOKEN = "31459979-84f0-4f36-a09e-83326691c5e5"          # Replace with your HEC token
INDEX = "zerotrust_logs"

payload_bp = Blueprint("payload_bp", __name__)

def get_location(ip: str) -> str:
    if ip in ("127.0.0.1", "localhost"):
        try:
            my_ip = requests.get("https://api.ipify.org").text
            ip = my_ip
        except Exception:
            return "Localhost / Private Network"
    try:
        geo_resp = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return f"{geo_resp.get('country','')}/{geo_resp.get('region','')}/{geo_resp.get('city','')}".strip("/")
    except Exception:
        return "unknown"

def parse_device(user_agent_str: str) -> str:
    ua = user_agents.parse(user_agent_str)
    return f"{ua.browser.family} {ua.browser.version_string} on {ua.os.family} {ua.os.version_string} ({ua.device.family or 'Unknown Device'})"


def send_to_splunk(events):
    headers = {
        "Authorization": f"Splunk {HEC_TOKEN}",
        "Content-Type": "application/json"
    }

    body = "\n".join(events)

    try:
        response = requests.post(SPLUNK_URL, headers=headers, data=body, verify=False)
        print("🔎 Splunk HEC response:", response.status_code, response.text)  # <-- log it!
        return {"status_code": response.status_code, "response": response.text}
    except requests.exceptions.RequestException as e:
        print("❌ Splunk HEC error:", str(e))
        return {"error": str(e)}

@proxy_bp.route("/proxies", methods=["GET"])
def get_proxies():
    try:
        proxies = ProxyRoute.get_all_proxies()
        return jsonify(proxies), 200
    except Exception as e:
        print("Error fetching proxies:", e)
        return jsonify([]), 500


@proxy_bp.route("/proxies/add", methods=["POST"])
def add_proxy():
    try:
        data = request.get_json()
        required_fields = ["client_name", "client_url"]
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        proxy_id, proxy_url = ProxyRoute.insert_proxy(data)
        if not proxy_id:
            return jsonify({"error": "Failed to insert proxy route"}), 500

        return jsonify({
            "message": "Proxy route added successfully",
            "id": proxy_id,
            "proxy_url": proxy_url
        }), 201

    except Exception as e:
        print("Error adding proxy route:", e)
        return jsonify({"error": str(e)}), 500



@proxy_bp.route("/proxy/<client_name>/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy_request(client_name, path):
    # 1. Get client mapping from DB
    proxies = ProxyRoute.get_all_proxies()
    client = next((c for c in proxies if c["client_name"].lower() == client_name.lower()), None)

    if not client:
        return jsonify({"error": "Client not registered"}), 404

    target_url = f"{client['client_url'].rstrip('/')}/{path}"

    # --- Collect request metadata ---
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    location = get_location(client_ip)
    user_agent_str = request.headers.get("User-Agent", "unknown")
    device_info = parse_device(user_agent_str)

    attributes = {
        "Timestamp": int(time.time()),
        "IP Address": client_ip,
        "Geo Location": location,
        "Device": device_info,
        "Request type": request.method,
        "Target URL": target_url,
        "Response": "pending"
    }

    try:
        # 2. Forward request to client_url
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k.lower() != "host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        attributes["Response"] = f"success ({resp.status_code})"

        # 3. Send to Splunk
        event = json.dumps({
            "time": int(time.time()),
            "sourcetype": "_json",
            "index": INDEX,
            "event": attributes
        })
        send_to_splunk([event])

        
        # 4. Also log locally
        print("📌 Proxy attributes sent to Splunk:", attributes)

        # 5. Return response back to caller
        if "application/json" in resp.headers.get("Content-Type", ""):
            return jsonify(resp.json()), resp.status_code
        else:
            return resp.text, resp.status_code

    except Exception as e:
        attributes["Response"] = f"failure ({str(e)})"

        # Send failure log to Splunk
        event = json.dumps({"event": attributes})
        send_to_splunk([event])

        print("❌ Proxy error attributes sent to Splunk:", attributes)
        return jsonify({
            "error": "Failed to forward request",
            "attributes": attributes
        }), 500