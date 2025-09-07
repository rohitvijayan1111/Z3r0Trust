from flask import Blueprint, jsonify, request
from models.proxy_routes_model import ProxyRoute
import requests   # ✅ Needed for forwarding

proxy_bp = Blueprint("proxy_routes", __name__)

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

        # 3. Log request/response
        print(f"📌 Proxy log: {request.method} {request.url} → {target_url} [{resp.status_code}]")

        # 4. Return response back to caller
        if "application/json" in resp.headers.get("Content-Type", ""):
            return jsonify(resp.json()), resp.status_code
        else:
            return resp.text, resp.status_code

    except Exception as e:
        print("Proxy error:", e)
        return jsonify({"error": "Failed to forward request"}), 500
