import pandas as pd
from audit.audit import log_audit

def enrich_with_total_value(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total_value = quantity * price"""
    df['total_value'] = df['quantity'] * df['price']
    log_audit("transformation", "Added total_value column")
    return df

def flag_suspicious_trades(df: pd.DataFrame) -> pd.DataFrame:
    """
    Suspicious if:
    - quantity is negative (short sell)
    - total_value > 100,000 (large exposure)
    """
    df['is_suspicious'] = ((df['quantity'] < 0) | (df['total_value'] > 100000)).astype(int)
    log_audit("transformation", f"Flagged {df['is_suspicious'].sum()} suspicious trades")
    return df

def run_full_transformation(df: pd.DataFrame) -> pd.DataFrame:
    df = enrich_with_total_value(df)
    df = flag_suspicious_trades(df)
    return df