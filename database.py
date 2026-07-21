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