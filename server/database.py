import sqlite3
from datetime import datetime

DB_PATH = "server/chat.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ✅ CREATE TABLE ON IMPORT (CRITICAL)
conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    date TEXT NOT NULL,
    edited INTEGER DEFAULT 0
)
""")


conn.commit()
conn.close()


def save_message(username: str, message: str):
    conn = get_connection()
    cur = conn.cursor()

    timestamp = datetime.now().strftime("%H:%M")
    date = datetime.now().strftime("%Y-%m-%d")

    cur.execute("""
        INSERT INTO messages (username, message, timestamp, date)
        VALUES (?, ?, ?, ?)
    """, (username, message, timestamp, date))

    conn.commit()
    msg_id = cur.lastrowid
    conn.close()
    return msg_id, timestamp, date


def get_chat_history(limit: int = 50):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, message, timestamp, date, edited
        FROM messages
        ORDER BY id ASC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return rows
def update_message(msg_id: int, new_text: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE messages
        SET message = ?, edited = 1
        WHERE id = ?
    """, (new_text, msg_id))

    conn.commit()
    conn.close()


def delete_message(msg_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE messages
        SET message = 'This message was deleted', edited = 1
        WHERE id = ?
    """, (msg_id,))

    conn.commit()
    conn.close()
