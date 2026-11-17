"""
SmartRetail AI - Configuration Module
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smartretail-ai-secret-key-capstone-2026')
    DEBUG = True
    
    # Dataset Paths
    DATASET_RAW = os.path.join(BASE_DIR, 'dataset', 'raw', 'Superstore.csv')
    DATASET_PROCESSED = os.path.join(BASE_DIR, 'dataset', 'processed', 'Superstore_Cleaned.csv')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'dataset', 'uploads')
    
    # Models & Artifacts
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    CHARTS_DIR = os.path.join(REPORTS_DIR, 'charts')
    
    # Database
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'smartretail.db')
    
    # File Upload Security
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB max upload
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # Benchmark KPIs (Superstore Reference)
    BENCHMARK_KPIS = {
        "records": 9994,
        "columns": 21,
        "total_sales": 2297200.86,
        "total_profit": 286397.02,
        "total_orders": 5009,
        "total_customers": 793,
        "total_quantity": 37873,
        "profit_margin": 12.47
    }

