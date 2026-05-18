FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY src/ ./src/
COPY sql/ ./sql/
COPY dashboard/ ./dashboard/
COPY tests/ ./tests/

# Create directories for data persistence
RUN mkdir -p /data/raw /data/staging /data/curated

# Copy sample data (optional – you can also mount it)
COPY data/raw/trades_2025-03-15.csv /data/raw/

# Set PYTHONPATH to find modules
ENV PYTHONPATH=/app

CMD ["python", "-m", "src.main"]