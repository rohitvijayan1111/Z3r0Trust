from db import get_db_connection

class Appeal:
    @staticmethod
    def insert_appeal(data):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO appeal (subject, content, status,ref_id) VALUES (%s, %s, %s,%s )",
                (data["subject"], data["content"], 1)  # default active
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error inserting appeal:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_appeal_init(data):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO appeal (subject, content, status,ref_id) VALUES (%s, %s, %s,%s )",
                (None,None,1,data.get("new_id"))  # default active
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error inserting appeal:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_appeals():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    a.id AS appeal_id,
                    a.subject AS appeal_subject,
                    a.content AS appeal_content,
                    a.status AS appeal_status,
                    al.id AS alert_id,
                    al.alert_name,
                    al.confidence_score,
                    al.user,
                    al.ip,
                    al.device,
                    al.status AS alert_status,
                    al.blockedIP,
                    al.blockedUser
                FROM appeal a
                LEFT JOIN alerts al ON a.ref_id = al.id
                WHERE a.status = 1
                ORDER BY a.id DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            appeals = []
            for row in rows:
                appeals.append({
                    "id": row["appeal_id"],
                    "subject": row["appeal_subject"],
                    "content": row["appeal_content"],
                    "status": row["appeal_status"],
                    "alert": {
                        "id": row["alert_id"],
                        "alert_name": row["alert_name"],
                        "confidence_score": row["confidence_score"],
                        "user": row["user"],
                        "ip": row["ip"],
                        "device": row["device"],
                        "status": row["alert_status"],
                        "blockedIP": row["blockedIP"],
                        "blockedUser": row["blockedUser"],
                    } if row["alert_id"] else None
                })
            return appeals
        except Exception as e:
            print("Error fetching appeals:", e)
            return []
        finally:
            cursor.close()
            conn.close()
