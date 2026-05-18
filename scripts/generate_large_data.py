import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_trades(n_rows=100000):
    np.random.seed(42)
    trade_ids = [f"T{i:06d}" for i in range(1, n_rows+1)]
    dates = [datetime(2025,1,1) + timedelta(days=np.random.randint(0, 90)) for _ in range(n_rows)]
    symbols = np.random.choice(['AAPL','GOOGL','MSFT','TSLA','AMZN','META','NFLX'], n_rows)
    quantities = np.random.randint(-500, 1000, n_rows)  # negative = short sells
    prices = np.round(np.random.uniform(50, 800, n_rows), 2)
    client_ids = [f"C{np.random.randint(1,5000):04d}" for _ in range(n_rows)]
    
    df = pd.DataFrame({
        'trade_id': trade_ids,
        'date': dates,
        'symbol': symbols,
        'quantity': quantities,
        'price': prices,
        'client_id': client_ids
    })
    return df

if __name__ == "__main__":
    df = generate_trades(100000)
    df.to_csv("data/raw/large_trades.csv", index=False)
    print("Generated 100,000 trades in data/raw/large_trades.csv")