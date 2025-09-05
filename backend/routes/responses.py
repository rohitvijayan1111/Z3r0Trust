from flask import Blueprint, jsonify, request
from models.response_model import Response
import requests

responses_bp = Blueprint('responses', __name__)

# Get all responses from DB
@responses_bp.route('/responses', methods=['GET'])
def get_responses():
    responses = Response.get_all_responses()
    return jsonify(responses), 200

# Fetch from external API and store in DB
@responses_bp.route('/responses/fetch', methods=['POST'])
def fetch_and_store_responses():
    external_api_url = "https://external-api.com/responses"  # replace with actual API
    try:
        resp = requests.get(external_api_url)
        if resp.status_code == 200:
            responses_data = resp.json()
            for item in responses_data:
                Response.insert_response(item)
            return jsonify({"message": "Responses fetched and stored successfully"}), 200
        else:
            return jsonify({"error": "Failed to fetch responses from external API"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
