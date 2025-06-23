import psycopg2

# connects to PostgreSQL DB
def get_db_connection():
    conn = psycopg2.connect(
        dbname="word_reader",
        user="kevin4383",
        password="password123",
        host="localhost",
        port="5432"  
    )
    return conn
