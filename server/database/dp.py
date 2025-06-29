import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # This is important to load the .env when called directly

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432")
    )
    return conn

