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
                (alert_id, alert_name, confidence_score, last_time, user, ip, location, device, action, status, failed_count, blockedIP, blockedUser)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(query, (
                alert_data.get('alert_id'),
                alert_data.get("alert_name"),
                int(alert_data.get("confidence_score")),
                alert_data.get("last_time", datetime.utcnow()),
                alert_data.get("user"),
                alert_data.get("ip"),
                alert_data.get("locations"),
                str(alert_data.get("devices")),
                alert_data.get("actions"),
                'suspended' if alert_data.get("statuses")=='failed' else 'active',
                int(alert_data.get("failed_count", '0')),
                alert_data.get("blockedIP", 0),
                alert_data.get("blockedUser", 0)
            ))
            conn.commit()

            new_id = cursor.lastrowid   # <-- auto increment ID
            return {'status': True, 'inserted_id': new_id}

        except Exception as e:
            print("Error inserting alert:", e)
            return {'status': False, 'e': str(e)}
        finally:
            cursor.close()
            conn.close()

    # def insert_alert(alert_data):
    #     conn = get_db_connection()
    #     if not conn:
    #         return False
        
    #     try:
    #         cursor = conn.cursor()
    #         query = """
    #             INSERT INTO alerts 
    #             (alert_id, alert_name, confidence_score, last_time, user, ip, location, device, action, status, failed_count, blockedIP, blockedUser)
    #             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    #         """
    #         cursor.execute(query, (
    #             alert_data.get('alert_id'),
    #             alert_data.get("alert_name"),
    #             int(alert_data.get("confidence_score")),
    #             alert_data.get("last_time", datetime.utcnow()),
    #             alert_data.get("user"),
    #             alert_data.get("ip"),
    #             alert_data.get("locations"),
    #             str(alert_data.get("devices")),
    #             alert_data.get("actions"),
    #             'suspended' if alert_data.get("statuses")=='failed' else 'active',
    #             int(alert_data.get("failed_count", '0')),
    #             alert_data.get("blockedIP", 0),
    #             alert_data.get("blockedUser", 0)
    #         ))
    #         conn.commit()
    #         return {'status':True}
    #     except Exception as e:
    #         print("Error inserting alert:", e)
    #         return {'status':False,'e':str(e)}
    #     finally:

    #         cursor.close()
    #         conn.close()

    @staticmethod
    def get_all_alerts():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alerts")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error fetching alerts:", e)
            return []
        finally:
            cursor.close()
            conn.close()

    
