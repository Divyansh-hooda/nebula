import sqlite3
import os
import config

def initialize():
    os.makedirs(config.DATABASE_DIR, exist_ok=True)
    conn = sqlite3.connect(config.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                filepath TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS favorites(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT UNIQUE
    )
    """)

def log(action, path):
    conn = sqlite3.connect(config.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (action, filepath) VALUES (?, ?)",
        (action, path)
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(config.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM history ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_favorite(path):
    conn=sqlite3.connect(config.DATABASE_FILE)
    cur=conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO favorites(filepath) VALUES (?)",
        (path,)
    )
    conn.commit()
    conn.close()

def get_favorites():
    conn=sqlite3.connect(config.DATABASE_FILE)
    cur=conn.cursor()
    cur.execute("SELECT * FROM favorites")
    rows=cur.fetchall()
    conn.close()
    return [x[0] for x in rows]