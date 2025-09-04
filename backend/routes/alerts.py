from flask import Blueprint, jsonify, request
from models.alert_model import Alert
import requests

alerts_bp = Blueprint('alerts', __name__)

# Route to fetch alerts from DB
@alerts_bp.route('/alerts', methods=['GET'])
def get_alerts():
    alerts = Alert.get_all_alerts()
    return jsonify(alerts), 200

# Route to fetch from external API and store in DB
@alerts_bp.route('/alerts/fetch', methods=['POST'])
def fetch_and_store_alerts():
    external_api_url = "https://external-api.com/alerts"  # replace with actual
    try:
        resp = requests.get(external_api_url)
        if resp.status_code == 200:
            alerts_data = resp.json()
            for alert in alerts_data:
                Alert.insert_alert(alert)
            return jsonify({"message": "Alerts fetched and stored successfully"}), 200
        else:
            return jsonify({"error": "Failed to fetch alerts from external API"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
