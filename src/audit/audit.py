import sqlite3
import datetime
import os

DB_PATH = "/data/pipeline.db"  # inside container

def log_audit(step: str, description: str, source_file: str = "unknown"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO audit_log (step, description, timestamp, source_file) VALUES (?, ?, ?, ?)",
        (step, description, timestamp, source_file)
    )
    conn.commit()
    conn.close()
    print(f"[AUDIT] {step} - {description}")