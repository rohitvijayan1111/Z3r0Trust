from flask import Blueprint, jsonify, request
from db import get_db_connection  # your DB connection function

responses_bp = Blueprint("responses", __name__)

# ------------------------------
# Get all responses
# ------------------------------
@responses_bp.route("/responses", methods=["GET"])
def get_responses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM responses ORDER BY timestamp DESC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching responses:", e)
        return jsonify([]), 200


# ------------------------------
# Undo response
# ------------------------------
@responses_bp.route("/responses/<int:response_id>/undo", methods=["PUT"])
def undo_response(response_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Reactivate response
        cursor.execute("UPDATE responses SET status='active' WHERE id=%s", (response_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Response not found"}), 404

        # Get associated alert
        cursor.execute("SELECT alert_id FROM responses WHERE id=%s", (response_id,))
        result = cursor.fetchone()
        if result and result[0]:
            alert_id = result[0]
            cursor.execute(
                "UPDATE alerts SET blockedIP=0, blockedUser=0, status='active' WHERE id=%s",
                (alert_id,),
            )

        conn.commit()
        return jsonify({"message": "Response and associated alert unblocked successfully"}), 200
    except Exception as e:
        print("Error undoing response:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# ------------------------------
# Add a new response
# ------------------------------
@responses_bp.route("/responses/add", methods=["POST"])
def add_response():
    try:
        data = request.get_json()

        required_fields = ["alert_name", "confidence_score", "timestamp", "user_name",
                           "email", "ip", "location", "device", "action", "status",
                           "failed_count", "alert_id"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO responses 
            (alert_name, confidence_score, timestamp, user_name, email, ip, location, device, action, status, failed_count, alert_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(query, (
            data["alert_name"],
            data["confidence_score"],
            data["timestamp"],
            data["user_name"],
            data["email"],
            data["ip"],
            data["location"],
            data["device"],
            data["action"],
            data["status"],
            data["failed_count"],
            data["alert_id"]
        ))

        conn.commit()
        response_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Response added successfully", "id": response_id}), 201

    except Exception as e:
        print("Error adding response:", e)
        return jsonify({"error": str(e)}), 500

@responses_bp.route("/responses/<int:response_id>/block", methods=["PUT"])
def block_response(response_id):
    """
    Block a response: set status to 'suspended' and block associated alert IP/User
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1️⃣ Update response status
        cursor.execute(
            "UPDATE responses SET status = 'suspended' WHERE id = %s",
            (response_id,),
        )

        # 2️⃣ Get associated alert_id
        cursor.execute(
            "SELECT alert_id FROM responses WHERE id = %s", (response_id,)
        )
        row = cursor.fetchone()
        if row:
            alert_id = row[0]
            # 3️⃣ Update alert: blockedIP and blockedUser to true
            cursor.execute(
                "UPDATE alerts SET blockedIP = 1, blockedUser = 1 WHERE id = %s",
                (alert_id,),
            )

        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        print("Error blocking response:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
