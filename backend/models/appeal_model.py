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
                "INSERT INTO appeal (subject, content, response_id) VALUES (%s, %s, %s)",
                (data["subject"], data["content"], data["response_id"])
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
                    r.id AS response_id,
                    r.alert_name AS response_alert_name,
                    r.confidence_score AS response_confidence_score,
                    r.alert_id AS alert_id,
                    al.alert_name AS alert_name,
                    al.confidence_score AS alert_confidence_score
                FROM appeal a
                LEFT JOIN responses r ON a.response_id = r.id
                LEFT JOIN alerts al ON r.alert_id = al.id
                ORDER BY a.id DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()  # fetch all rows safely

            appeals = []
            for row in rows:
                appeals.append({
                    "id": row["appeal_id"],
                    "subject": row["appeal_subject"],
                    "content": row["appeal_content"],
                    "response": {
                        "id": row["response_id"],
                        "alert_name": row["response_alert_name"],
                        "confidence_score": row["response_confidence_score"],
                        "alert": {
                            "id": row["alert_id"],
                            "alert_name": row["alert_name"] or "N/A",
                            "confidence_score": row["alert_confidence_score"] or "N/A"
                        } if row["alert_id"] else None
                    } if row["response_id"] else None
                })
            return appeals

        except Exception as e:
            print("Error fetching appeals:", e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

