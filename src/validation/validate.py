import pandas as pd
import datetime
from audit.audit import log_audit

def validate_trades(df: pd.DataFrame, skip_audit: bool = False) -> list:
    """
    Returns list of tuples (trade_id, error_type, error_message)
    If skip_audit=True, does not write to audit log (useful for testing)
    """
    errors = []
    today = datetime.date.today().isoformat()

    for _, row in df.iterrows():
        trade_id = row['trade_id']

        if pd.isna(row['price']):
            errors.append((trade_id, "missing_price", f"Trade {trade_id} has no price"))
        if pd.isna(row['client_id']):
            errors.append((trade_id, "missing_client", f"Trade {trade_id} has no client"))
        if row['quantity'] < 0:
            errors.append((trade_id, "negative_quantity", f"Trade {trade_id} quantity {row['quantity']} < 0"))
        if row['date'] > today:
            errors.append((trade_id, "future_date", f"Trade {trade_id} date {row['date']} is in the future"))

    if not skip_audit:
        log_audit("validation", f"Found {len(errors)} validation issues")
    return errors