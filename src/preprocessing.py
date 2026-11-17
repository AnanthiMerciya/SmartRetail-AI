"""
SmartRetail AI - Preprocessing Module
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = ['Order Date', 'Sales', 'Profit', 'Quantity', 'Discount', 'Category']

def validate_dataset(df):
    """Checks if dataset has the essential required columns."""
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    is_valid = len(missing_cols) == 0
    return is_valid, missing_cols

def inspect_dataset(file_path):
    """Reads dataset, inspects shape, data types, missing values, and duplicates."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(file_path, encoding='latin1')
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
        
    is_valid, missing_cols = validate_dataset(df)
    
    missing_counts = df.isnull().sum().to_dict()
    total_missing = int(df.isnull().sum().sum())
    duplicate_count = int(df.duplicated().sum())
    
    columns_info = []
    for col in df.columns:
        columns_info.append({
            "name": col,
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "unique": int(df[col].nunique())
        })
        
    preview = df.head(10).to_dict(orient='records')
    
    return {
        "is_valid": is_valid,
        "missing_columns": missing_cols,
        "rows": int(df.shape[0]),
        "columns_count": int(df.shape[1]),
        "total_missing": total_missing,
        "duplicate_count": duplicate_count,
        "columns_info": columns_info,
        "preview": preview
    }

def clean_and_process_dataset(input_path, output_path):
    """
    Cleans raw dataset, parses dates, extracts temporal features,
    and saves to output_path.
    """
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(input_path, encoding='latin1')
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(input_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
        
    # Check required columns
    is_valid, missing = validate_dataset(df)
    if not is_valid:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")
        
    # Drop exact duplicate rows if any
    initial_rows = len(df)
    df = df.drop_duplicates()
    dropped_dupes = initial_rows - len(df)
    
    # Parse dates safely
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    if 'Ship Date' in df.columns:
        df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
        
    # Drop rows where Order Date or critical financials are NaN
    df = df.dropna(subset=['Order Date', 'Sales', 'Profit'])
    
    # Numeric sanitization
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0.0)
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0.0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1).astype(int)
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0.0)
    
    # Temporal feature engineering
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Month Name'] = df['Order Date'].dt.month_name()
    df['Quarter'] = df['Order Date'].dt.quarter
    df['Day'] = df['Order Date'].dt.day
    df['Day Name'] = df['Order Date'].dt.day_name()
    
    # Save cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    return {
        "success": True,
        "processed_rows": len(df),
        "columns_count": len(df.columns),
        "dropped_duplicates": dropped_dupes,
        "output_path": output_path
    }

