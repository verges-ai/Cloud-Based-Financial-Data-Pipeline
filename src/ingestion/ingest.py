import pandas as pd
import requests
import os
from audit.audit import log_audit

def ingest_trades(csv_path: str) -> pd.DataFrame:
    """Read raw trades CSV"""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")
    df = pd.read_csv(csv_path)
    log_audit("ingestion", f"Loaded {len(df)} trades from {os.path.basename(csv_path)}", csv_path)
    return df

def ingest_market_prices(symbols: list) -> dict:
    """
    Get market prices for given symbols.
    If API key available, use real data; otherwise return mock.
    """
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    prices = {}
    for sym in symbols:
        if api_key:
            try:
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={sym}&apikey={api_key}"
                response = requests.get(url, timeout=10)
                data = response.json()
                price = float(data["Global Quote"]["05. price"])
                prices[sym] = price
            except:
                prices[sym] = 150.0  # fallback
        else:
            # Mock prices
            mock = {"AAPL": 175.50, "GOOGL": 140.20, "MSFT": 420.00, "TSLA": 250.00, "AMZN": 130.00, "META": 300.00, "NFLX": 450.00}
            prices[sym] = mock.get(sym, 100.0)
    log_audit("ingestion", f"Fetched prices for {len(prices)} symbols")
    return prices