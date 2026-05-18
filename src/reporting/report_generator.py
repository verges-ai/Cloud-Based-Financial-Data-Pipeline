import pandas as pd
import sqlite3
from audit.audit import log_audit

def generate_regulatory_report(output_path: str = "/data/curated/regulatory_report.csv"):
    conn = sqlite3.connect("/data/pipeline.db")
    query = """
    SELECT 
        symbol,
        COUNT(trade_id) as num_trades,
        SUM(quantity) as total_quantity,
        SUM(total_value) as total_value,
        SUM(is_suspicious) as suspicious_trades
    FROM cleaned_trades
    GROUP BY symbol
    ORDER BY symbol
    """
    summary = pd.read_sql_query(query, conn)
    summary.to_csv(output_path, index=False)
    conn.close()
    log_audit("reporting", f"Generated regulatory report at {output_path}")
    return summary