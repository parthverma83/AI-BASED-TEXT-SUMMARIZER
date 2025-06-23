import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    # Create summaries table
    c.execute('''CREATE TABLE IF NOT EXISTS summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        original_text TEXT NOT NULL,
        summary TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[1], password):
        return user[0]  # return user id
    return None

def save_summary(user_id, original_text, summary):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO summaries (user_id, original_text, summary) VALUES (?, ?, ?)',
              (user_id, original_text, summary))
    conn.commit()
    conn.close()

def get_summaries(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, original_text, summary, created_at FROM summaries WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    summaries = c.fetchall()
    conn.close()
    return summaries

def get_db_connection():
    """Return a new connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)
