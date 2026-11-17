"""
SmartRetail AI - SQLite Database Utility
"""

import sqlite3
import os
from config import Config

def get_db_connection():
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    schema_path = os.path.join(Config.BASE_DIR, 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn = get_db_connection()
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()
        print("Database schema initialized successfully.")

def log_event(event_type, message):
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO system_logs (event_type, message) VALUES (?, ?)', (event_type, message))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging event: {e}")

def record_upload(filename, original_name, row_count, col_count, file_size_bytes, cleaned_path, notes=''):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO uploaded_datasets 
            (filename, original_name, row_count, col_count, file_size_bytes, cleaned_path, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (filename, original_name, row_count, col_count, file_size_bytes, cleaned_path, notes))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except Exception as e:
        print(f"Error recording upload: {e}")
        return None

def record_forecast(model_name, horizon_months, total_predicted, highest_m='', highest_s=0, lowest_m='', lowest_s=0, params=''):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO forecast_history 
            (model_name, horizon_months, total_predicted_sales, highest_month, highest_sales, lowest_month, lowest_sales, parameters_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (model_name, horizon_months, total_predicted, highest_m, highest_s, lowest_m, lowest_s, params))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except Exception as e:
        print(f"Error recording forecast: {e}")
        return None

def record_report(report_type, filename, file_path, records_count):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO generated_reports (report_type, filename, file_path, records_count)
            VALUES (?, ?, ?, ?)
        ''', (report_type, filename, file_path, records_count))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except Exception as e:
        print(f"Error recording report: {e}")
        return None

