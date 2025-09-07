from flask import Blueprint, jsonify, request
from models.appeal_model import Appeal

appeals_bp = Blueprint("appeals", __name__)

@appeals_bp.route("/appeals", methods=["GET"])
def get_appeals():
    try:
        appeals = Appeal.get_all_appeals()
        if not isinstance(appeals, list):
            appeals = []
        return jsonify(appeals), 200
    except Exception as e:
        print("Error fetching appeals:", e)
        return jsonify([]), 500

@appeals_bp.route("/appeals/add", methods=["POST"])
def add_appeal():
    try:
        data = request.get_json()
        required_fields = ["subject", "content", "response_id"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        appeal_id = Appeal.insert_appeal(data)
        if not appeal_id:
            return jsonify({"error": "Failed to insert appeal"}), 500

        return jsonify({"message": "Appeal added successfully", "id": appeal_id}), 201

    except Exception as e:
        print("Error adding appeal:", e)
        return jsonify({"error": str(e)}), 500
