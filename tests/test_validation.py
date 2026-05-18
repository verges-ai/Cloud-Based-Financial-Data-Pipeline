import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pandas as pd
from validation.validate import validate_trades

def test_validate_missing_price():
    df = pd.DataFrame({
        'trade_id': ['T1'],
        'date': ['2025-03-15'],
        'symbol': ['AAPL'],
        'quantity': [100],
        'price': [None],
        'client_id': ['C1']
    })
    errors = validate_trades(df, skip_audit=True)
    assert any('missing_price' in str(err) for err in errors)

def test_validate_negative_quantity():
    df = pd.DataFrame({
        'trade_id': ['T2'],
        'date': ['2025-03-15'],
        'symbol': ['GOOGL'],
        'quantity': [-10],
        'price': [150.0],
        'client_id': ['C2']
    })
    errors = validate_trades(df, skip_audit=True)
    assert any('negative_quantity' in str(err) for err in errors)