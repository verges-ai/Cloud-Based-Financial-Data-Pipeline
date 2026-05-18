import sqlite3
import pandas as pd
import datetime
import os

DB_PATH = "/data/pipeline.db"

def record_lineage(target_table: str, target_field: str, target_value: str, 
                   source_file: str, source_line: int, transformation_rule: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.datetime.now().isoformat()
    cursor.execute(
        """INSERT INTO lineage 
        (target_table, target_field, target_value, source_file, source_line, transformation_rule, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (target_table, target_field, str(target_value), source_file, source_line, transformation_rule, created_at)
    )
    conn.commit()
    conn.close()

def lineage_from_dataframe(df: pd.DataFrame, source_file: str):
    """Simple example: record that each trade came from a specific CSV row"""
    for idx, row in df.iterrows():
        record_lineage(
            target_table="cleaned_trades",
            target_field="trade_id",
            target_value=row['trade_id'],
            source_file=source_file,
            source_line=idx+2,   # +2 for header row
            transformation_rule="direct copy from CSV"
        )