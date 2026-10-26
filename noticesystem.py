import sqlite3
import hashlib
import hmac
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "notices.db"
SECRET_PEPPER = os.getenv("SECRET_PEPPER", "default_fallback_pepper_key").encode('utf-8')

def anonymize_user_id(user_id: int) -> str:
    return hmac.new(
        SECRET_PEPPER, 
        str(user_id).encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            title TEXT,
            notice_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def deletenotice(user_id: int, title: str) -> bool:
    hashed_user_id = anonymize_user_id(user_id)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM user_notices WHERE user_id = ? AND LOWER(title) = LOWER(?)",
        (hashed_user_id, title),
    )
    row = cursor.fetchone()

    if row:
        cursor.execute("DELETE FROM user_notices WHERE id = ?", (row[0],))
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False

def createnotice(user_id: int, title: str, notice_date: str):
    hashed_user_id = anonymize_user_id(user_id)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_notices (user_id, title, notice_date) VALUES (?, ?, ?)",
        (hashed_user_id, title, notice_date),
    )
    conn.commit()
    conn.close()
    print(f"Notice saved for anonymized user {hashed_user_id[:10]}...: {title} at {notice_date}")

def getnotices(user_id: int):
    hashed_user_id = anonymize_user_id(user_id)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title, notice_date FROM user_notices WHERE user_id = ?",
        (hashed_user_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows  

init_db()
