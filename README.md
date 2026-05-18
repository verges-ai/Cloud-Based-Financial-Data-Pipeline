# 📊 Cloud-Based Financial Data Pipeline

**A production‑ready ETL pipeline that ingests, cleans, validates, and reports on financial trade data – with full audit trails, data lineage, and an interactive dashboard.**  
Built with Python, SQL, Docker, and Streamlit.

---

## 🧭 Business Context (For Everyone)

Imagine a small investment firm that buys and sells stocks for its clients. Every day they receive thousands of trade records (who bought what, how many shares, at what price). The data comes from different sources: CSV files, a market price API, and a risk database.

**The old way**  
An employee spends 4 hours manually copy‑pasting data, checking for missing prices, and creating an Excel report. Mistakes happen, and when the regulator asks *“Where did this number come from?”* – nobody knows.

**Our solution**  
An automated pipeline that:
- Reads trades from a CSV file (100,000+ rows).
- Fetches live market prices from an API (or uses mock data).
- Merges risk scores from a SQLite database.
- Calculates total value and flags suspicious trades (negative quantity or large exposure).
- Writes every step into an **audit log** (a diary of actions).
- Records **data lineage** (where each number originated).
- Produces a clean dataset and a regulatory report.
- Visualises everything in a **dashboard** with filters and charts.

The pipeline runs inside **Docker** containers – it works the same on a laptop, a server, or in the cloud.

---

## 💼 Business Case – Why This Project Matters

| Metric | Without Pipeline | With Pipeline | Saving |
|--------|----------------|---------------|--------|
| Time per daily report | 4 hours | 15 minutes | 3.75 hours/day |
| Data errors (missing/wrong) | ~8% | <0.5% | fewer fines & rework |
| Audit readiness | impossible | full traceability | pass regulator inspections |
| Monthly cost (staff + cloud) | €3,200 | €50 | ~€3,150 |

**Payback period:** less than 1 month.

From a job perspective: this project proves you can design **modular, production‑grade data pipelines** with monitoring, error handling, and real business value.

---

## 🧩 Architecture Overview
# Cloud-Based-Financial-Data-Pipeline

```bash
Cloud-Based-Financial-Data-Pipeline/
│
├── data/
│   ├── raw/           ← Raw input files (e.g. trades_2025-03-15.csv)
│   ├── staging/       ← Intermediate processed data
│   └── curated/       ← Final cleaned & enriched data + reports
│
├── src/
│   ├── ingestion/     ← Reading CSV, APIs, external sources
│   ├── transformation/← Data cleaning, calculations (total_value, etc.)
│   ├── validation/    ← Quality checks (missing fields, negative quantity...)
│   ├── lineage/       ← Data lineage tracking
│   ├── audit/         ← Audit logging for every step
│   ├── storage/       ← Database operations (SQLite / PostgreSQL)
│   ├── reporting/     ← Generate regulatory & business reports
│   └── utils/         ← Helper functions
│
├── dashboard/         ← Streamlit web application
├── sql/               ← SQL scripts (table creation, views, etc.)
├── tests/             ← Unit & integration tests (pytest)
├── scripts/           ← Utility scripts (generate fake data, etc.)
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```




**How data flows:**
1. **Ingestion** – read trades CSV, fetch market prices (real or mock), load risk scores.
2. **Transformation** – calculate `total_value = quantity * price`, flag suspicious trades.
3. **Validation** – find missing prices, missing clients, negative quantities, future dates.
4. **Storage** – save cleaned data, validation errors, audit log, lineage into SQLite.
5. **Reporting** – create aggregated report (`regulatory_report.csv`).
6. **Dashboard** – visualise tables, charts, filters, and lineage.

All steps are logged in the `audit_log` table. Every value’s origin is stored in the `lineage` table.

---

## 🚀 Quick Start (Run the pipeline in 5 minutes)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows, Mac, or Linux)
- [Python 3.10+](https://www.python.org/downloads/) (only if you want to run the dashboard locally)
- Git (optional)

### 1. Clone or download this repository
```bash
git clone https://github.com/yourusername/Cloud-Based-Financial-Data-Pipeline.git
cd Cloud-Based-Financial-Data-Pipeline
```
---
### 2. Generate large sample data (100,000 trades)

pip install pandas numpy
python scripts/generate_large_data.py

This creates data/raw/large_trades.csv.

### 3. Build and run the pipeline (inside Docker)

docker-compose build pipeline
docker-compose run --rm pipeline python -m src.main

The pipeline will process the CSV in chunks (10,000 rows at a time), log everything, and produce a database and a report.

### 4. Copy the database to your local folder (for the dashboard)

docker-compose run --rm pipeline cat /data/pipeline.db > pipeline.db

### 5. Launch the dashboard (locally)

pip install streamlit pandas plotly
streamlit run dashboard/app.py

### 6. Dashboard – What You’ll See
The dashboard has a sidebar with navigation and filters.

Pages
📊 Overview – Key metrics (total trades, suspicious %, validation errors), charts (trades per symbol, daily value, suspicious vs normal), and recent audit log.

📋 Cleaned Trades – Table of all cleaned data (supports filtering by date, symbol, client, suspicious flag). Download as CSV.

⚠️ Validation Errors – List of mistakes found in raw data, plus a bar chart of error types.

📜 Audit Log – Complete diary of every pipeline step (ingestion, transformation, validation, storage, reporting).

🔗 Data Lineage – Trace where each value came from (source file, row, transformation rule).

Filters (apply to Overview and Cleaned Trades)
Date range

Symbol (e.g., AAPL, GOOGL)

Client ID

Suspicious only / normal / all

Example KPI cards
Total Trades (e.g., 100,000)

Suspicious Trades (e.g., 7,650)

Validation Errors (e.g., 3,200)

Total Value (e.g., €12.4 million)

### 7. Customisation – Use Your Own Data

Replace the input CSV

trade_id, date, symbol, quantity, price, client_id

### 8. Add a real market price API (Alpha Vantage)

1. Get a free API key from Alpha Vantage.

2. Run the pipeline with your key:
docker-compose run --rm -e ALPHA_VANTAGE_API_KEY=YOUR_KEY_HERE pipeline python -m src.main
