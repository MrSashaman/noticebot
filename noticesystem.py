import sqlite3

DB_NAME = "notices.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            notice_date TEXT
        )
    """)
  conn.commit()
  conn.close()

def deletenotice(user_id: int, title: str):

  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  cursor.execute(
      "SELECT id FROM user_notices WHERE user_id = ? AND LOWER(title) = LOWER(?)",
      (user_id, title),
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
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute(
      "INSERT INTO user_notices (user_id, title, notice_date) VALUES (?, ?, ?)",
      (user_id, title, notice_date),
  )
  conn.commit()
  conn.close()
  print(f"Notice saved for user {user_id}: {title} at {notice_date}")


def getnotices(user_id: int):
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT title, notice_date FROM user_notices WHERE user_id = ?",
      (user_id,),
  )
  rows = cursor.fetchall()
  conn.close()
  return rows  


init_db()
