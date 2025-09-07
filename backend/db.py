from flask import Flask
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MySQL connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
