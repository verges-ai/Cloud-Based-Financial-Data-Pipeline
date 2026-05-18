import sys
import os
import pandas as pd
sys.path.insert(0, '/app/src')

from ingestion.ingest import ingest_market_prices
from transformation.transform import run_full_transformation
from validation.validate import validate_trades
from lineage.lineage import lineage_from_dataframe
from audit.audit import log_audit
from storage.db_handler import init_db, save_validation_errors
from reporting.report_generator import generate_regulatory_report
import sqlite3

DB_PATH = "/data/pipeline.db"

def append_cleaned_trades(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("cleaned_trades", conn, if_exists="append", index=False)
    conn.close()
    log_audit("storage", f"Appended {len(df)} rows to cleaned_trades")

def main():
    print("=== Cloud-Based Financial Data Pipeline (Large Data Mode) ===")
    init_db()

    csv_path = "/data/raw/large_trades.csv"
    
    # Check if large file exists, otherwise fallback to small sample
    if not os.path.exists(csv_path):
        print("Large file not found, using small sample trades.csv")
        csv_path = "/data/raw/trades_2025-03-15.csv"
    
    # Get unique symbols efficiently (read only that column)
    symbols_series = pd.read_csv(csv_path, usecols=['symbol'])
    unique_symbols = symbols_series['symbol'].unique()
    market_prices = ingest_market_prices(unique_symbols)
    
    chunksize = 10000
    total_rows = 0
    all_errors = []
    chunk_num = 0
    
    for chunk_num, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunksize), 1):
        print(f"Processing chunk {chunk_num} ({len(chunk)} rows)...")
        transformed = run_full_transformation(chunk)
        errors = validate_trades(transformed, skip_audit=False)
        all_errors.extend(errors)
        lineage_from_dataframe(transformed, csv_path)
        append_cleaned_trades(transformed)
        total_rows += len(chunk)
    
    save_validation_errors(all_errors)
    generate_regulatory_report()    
    
    print(f"Pipeline finished. Processed {total_rows} rows in {chunk_num} chunks.")
    log_audit("pipeline", f"Large data pipeline completed: {total_rows} rows processed")

if __name__ == "__main__":
    main()