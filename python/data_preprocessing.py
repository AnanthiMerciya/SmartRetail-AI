"""
SmartRetail AI - Data Preprocessing Pipeline
Author: Ananthi Merciya M (Reg No: ASML24005)
Date: 2026-11-05
"""

import os
import pandas as pd
import numpy as np

def clean_retail_data(input_path="../dataset/raw/Superstore.csv", output_path="../dataset/processed/Superstore_Cleaned.csv"):
    print("[1/4] Loading raw retail transactions from:", input_path)
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    df = pd.read_csv(input_path, encoding="latin1")
    print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")

    print("[2/4] Auditing data integrity...")
    missing_vals = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    print(f"Total missing values: {missing_vals}")
    print(f"Total duplicate rows: {duplicate_rows}")

    print("[3/4] Parsing timestamps & feature engineering...")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.month_name()
    df["Quarter"] = df["Order Date"].dt.quarter
    df["Day"] = df["Order Date"].dt.day
    df["Day Name"] = df["Order Date"].dt.day_name()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[4/4] Cleaned dataset saved to: {output_path} ({df.shape[0]} rows, {df.shape[1]} columns)")
    return df

if __name__ == "__main__":
    clean_retail_data()

