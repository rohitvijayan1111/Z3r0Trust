from flask import Blueprint, jsonify, request
from models.alert_model import Alert
from models.response_model import Response
from db import get_db_connection

alerts_bp = Blueprint("alerts", __name__)
responses_bp = Blueprint("responses", __name__)

# Get all alerts
@alerts_bp.route("/alerts", methods=["GET"])
def get_alerts():
    alerts = Alert.get_all_alerts()
    return jsonify(alerts), 200

# Fetch alerts from external API and store in DB
@alerts_bp.route("/alerts/fetch", methods=["POST"])
def fetch_and_store_alerts():
    # import requests
    # external_api_url = "https://external-api.com/alerts"  # replace with actual
    try:
        # resp = requests.get(external_api_url)
        # if resp.status_code == 200:
        #     alerts_data = resp.json()
        #     for alert in alerts_data:
                # Alert.insert_alert(alert)
        #     return jsonify({"message": "Alerts fetched and stored successfully"}), 200
        # return jsonify({"error": "Failed to fetch alerts"}), 400
        print("hellllo")
        data=request.get_json()
        print(data)
        res=Alert.insert_alert(data)
        if(res.get('status')):
            return jsonify({"message": "Alerts stored successfully","new_id":res.get("inserted_id")}), 200
        else:
            return jsonify({'e':str(res.get('e'))}),500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@responses_bp.route("/alerts/fetchbyid", methods=["POST"])
def fetch():
    """
    Fetch a specific alert by its auto-increment ID.
    Input: { "id": <int> }
    Returns: alert row as JSON (key-value pairs).
    """
    try:
        req_data = request.get_json()
        alert_id = req_data.get("id")
        if not alert_id:
            return jsonify({"error": "Missing 'id' in request"}), 400

        res = Alert.fetch_alert(alert_id)
        if res:
            return jsonify({"alert": res}), 200
        else:
            return jsonify({"error": f"No alert found with id={alert_id}"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Block a response and its associated alert
@responses_bp.route("/responses/<int:response_id>/block", methods=["PUT"])
def block_response(response_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Update response status to suspended
        cursor.execute("UPDATE responses SET status='suspended' WHERE id=%s", (response_id,))
        # Fetch associated alert_id
        cursor.execute("SELECT alert_id FROM responses WHERE id=%s", (response_id,))
        result = cursor.fetchone()
        if result and result[0]:
            alert_id = result[0]
            # Block alert IP and user
            cursor.execute(
                "UPDATE alerts SET blockedIP=1, blockedUser=1, status='suspended' WHERE id=%s",
                (alert_id,),
            )
        conn.commit()
        return jsonify({"message": "Response and associated alert blocked successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
