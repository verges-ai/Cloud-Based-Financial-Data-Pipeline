import sqlite3
import pandas as pd
import os
import datetime
from audit.audit import log_audit

DB_PATH = "/data/pipeline.db"

def init_db():
    """Create all tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    with open("/app/sql/schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def save_cleaned_trades(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("cleaned_trades", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

def save_validation_errors(errors: list):

    """errors is list of (trade_id, error_type, error_message)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    for trade_id, err_type, msg in errors:
        cursor.execute(
            "INSERT INTO validation_errors (trade_id, error_type, error_message, timestamp) VALUES (?, ?, ?, ?)",
            (trade_id, err_type, msg, timestamp)
        )
    conn.commit()
    conn.close()

def append_cleaned_trades(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("cleaned_trades", conn, if_exists="append", index=False)
    conn.close()
    log_audit("storage", f"Appended {len(df)} rows to cleaned_trades")    