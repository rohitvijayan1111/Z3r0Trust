from db import get_db_connection

BASE_PROXY_DOMAIN = "http://127.0.0.1:5000/proxy"  # ✅ adjust

class ProxyRoute:
    @staticmethod
    def insert_proxy(data):
        conn = get_db_connection()
        if not conn:
            return None, None
        try:
            proxy_url = f"{BASE_PROXY_DOMAIN}/{data['client_name'].lower()}"
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO proxy_routes (client_name, proxy_url, client_url) VALUES (%s, %s, %s)",
                (data["client_name"], proxy_url, data["client_url"])
            )
            conn.commit()
            return cursor.lastrowid, proxy_url
        except Exception as e:
            print("Error inserting proxy route:", e)
            return None, None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_proxies():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM proxy_routes ORDER BY id DESC")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error fetching proxies:", e)
            return []
        finally:
            cursor.close()
            conn.close()
