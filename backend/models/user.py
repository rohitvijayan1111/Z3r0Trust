from db import get_db_connection

def create_user(first_name, last_name, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
        (first_name, last_name, email, password)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
