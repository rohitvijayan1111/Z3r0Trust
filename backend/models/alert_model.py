from db import get_db_connection
from datetime import datetime

class Alert:
    @staticmethod
    def insert_alert(alert_data):
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO alerts 
                (alert_name, confidence_score, timestamp, user_name, email, ip, location, device, action, status, failed_count, blockedIP, blockedUser)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(query, (
                alert_data.get("alert_name"),
                alert_data.get("confidence_score"),
                alert_data.get("timestamp", datetime.utcnow()),
                alert_data.get("user"),
                alert_data.get("ip"),
                alert_data.get("location"),
                alert_data.get("device"),
                alert_data.get("action"),
                alert_data.get("status"),
                alert_data.get("failed_count", 0),
                alert_data.get("blockedIP", False),
                alert_data.get("blockedUser", False)
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error inserting alert:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_alerts():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error fetching alerts:", e)
            return []
        finally:
            cursor.close()
            conn.close()
