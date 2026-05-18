-- Main cleaned trades table
CREATE TABLE IF NOT EXISTS cleaned_trades (
    trade_id TEXT PRIMARY KEY,
    date TEXT,
    symbol TEXT,
    quantity REAL,
    price REAL,
    client_id TEXT,
    total_value REAL,
    is_suspicious INTEGER
);

-- Validation errors
CREATE TABLE IF NOT EXISTS validation_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id TEXT,
    error_type TEXT,
    error_message TEXT,
    timestamp TEXT
);

-- Audit log
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    step TEXT,
    description TEXT,
    timestamp TEXT,
    source_file TEXT
);

-- Data lineage (tracks field-level origin)
CREATE TABLE IF NOT EXISTS lineage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_table TEXT,
    target_field TEXT,
    target_value TEXT,
    source_file TEXT,
    source_line INTEGER,
    transformation_rule TEXT,
    created_at TEXT
);