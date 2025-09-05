from db import get_db_connection
from datetime import datetime

class Response:
    @staticmethod
    def insert_response(response_data):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO responses 
                (alert_name, confidence_score, timestamp, user_name, email, ip, location, device, action, status, failed_count)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(query, (
    response_data.get("alert_name"),
    response_data.get("confidence_score"),
    response_data.get("timestamp", datetime.utcnow()),
    response_data.get("user_name"),  # ✅ fix here
    response_data.get("email"),
    response_data.get("ip"),
    response_data.get("location"),
    response_data.get("device"),
    response_data.get("action"),
    response_data.get("status"),
    response_data.get("failed_count", 0)
))

            conn.commit()
            return True
        except Exception as e:
            print("Error inserting response:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_responses():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM responses ORDER BY timestamp DESC")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error fetching responses:", e)
            return []
        finally:
            cursor.close()
            conn.close()
