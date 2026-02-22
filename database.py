import sqlite3
from datetime import datetime

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS force_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT,
    type TEXT,
    value TEXT,
    button_name TEXT,
    required_count INTEGER,
    current_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    created_at TEXT
)
""")

conn.commit()


def add_user(user_id, username, full_name):
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)",
                   (user_id, username, full_name, datetime.now()))
    conn.commit()


def add_force_channel(token, type_, value, button_name, required):
    cursor.execute("""
    INSERT INTO force_channels (token, type, value, button_name, required_count, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (token, type_, value, button_name, required, datetime.now()))
    conn.commit()


def get_channel_by_token(token):
    cursor.execute("SELECT * FROM force_channels WHERE token=? AND status='active'", (token,))
    return cursor.fetchone()


def increase_count(channel_id):
    cursor.execute("""
    UPDATE force_channels
    SET current_count = current_count + 1
    WHERE id=?
    """, (channel_id,))
    conn.commit()
