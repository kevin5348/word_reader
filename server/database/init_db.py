from dp import get_db_connection

conn = get_db_connection()
print("connected")
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    level FLOAT DEFAULT 0.5
)
""")
print("users table created")

# Create click_logs table
cur.execute("""
CREATE TABLE IF NOT EXISTS click_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    word TEXT NOT NULL,
    difficulty_score FLOAT NOT NULL,
    clicked BOOLEAN DEFAULT TRUE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
cur.close()
conn.close()

print("Tables created successfully.")