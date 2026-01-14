import sqlite3
from datetime import datetime

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

# таблица пользователей
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    returns_used INTEGER DEFAULT 0,
    filters_used INTEGER DEFAULT 0,
    gender TEXT DEFAULT 'any',
    geo TEXT DEFAULT 'any'
)
""")

# таблица истории диалогов
cur.execute("""
CREATE TABLE IF NOT EXISTS dialogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_a INTEGER,
    user_b INTEGER,
    ended_at TEXT
)
""")

conn.commit()

# -------- helpers --------

def ensure_user(user_id: int):
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def get_user(user_id: int):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cur.fetchone()

def inc_return(user_id: int):
    cur.execute("UPDATE users SET returns_used = returns_used + 1 WHERE user_id=?", (user_id,))
    conn.commit()

def inc_filter(user_id: int):
    cur.execute("UPDATE users SET filters_used = filters_used + 1 WHERE user_id=?", (user_id,))
    conn.commit()

def save_dialog(a: int, b: int):
    cur.execute(
        "INSERT INTO dialogs (user_a, user_b, ended_at) VALUES (?, ?, ?)",
        (a, b, datetime.utcnow().isoformat())
    )
    conn.commit()
