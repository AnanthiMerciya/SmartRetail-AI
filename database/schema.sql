-- SmartRetail AI SQLite Database Schema
-- Author: Ananthi Merciya M (Reg No: ASML24005)

CREATE TABLE IF NOT EXISTS uploaded_datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    original_name TEXT NOT NULL,
    row_count INTEGER,
    col_count INTEGER,
    file_size_bytes INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'processed',
    cleaned_path TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS forecast_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    horizon_months INTEGER NOT NULL,
    total_predicted_sales REAL,
    highest_month TEXT,
    highest_sales REAL,
    lowest_month TEXT,
    lowest_sales REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parameters_json TEXT
);

CREATE TABLE IF NOT EXISTS generated_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_type TEXT NOT NULL, -- 'PDF' or 'CSV'
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    records_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

