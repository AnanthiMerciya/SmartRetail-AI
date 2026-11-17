"""
SmartRetail AI - Sales Forecasting & Machine Learning Pipeline
Author: Ananthi Merciya M (Reg No: ASML24005)
Date: 2026-11-05
"""

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_forecast(data_path="../dataset/processed/Superstore_Cleaned.csv"):
    print("[1/5] Loading cleaned dataset from:", data_path)
    df = pd.read_csv(data_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    print("[2/5] Aggregating monthly sales time series...")
    monthly_sales = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    monthly_sales.columns = ["Month", "Sales"]
    monthly_sales["Month"] = pd.to_datetime(monthly_sales["Month"].astype(str))
    monthly_sales["Year"] = monthly_sales["Month"].dt.year
    monthly_sales["Month_Number"] = monthly_sales["Month"].dt.month

    # Train-test split (2014-2016 Train, 2017 Test)
    train_data = monthly_sales[monthly_sales["Year"] < 2017]
    test_data = monthly_sales[monthly_sales["Year"] == 2017]
    print(f"Training months: {len(train_data)} | Testing months: {len(test_data)}")

    X_train = train_data[["Year", "Month_Number"]]
    y_train = train_data["Sales"]
    X_test = test_data[["Year", "Month_Number"]]
    y_test = test_data["Sales"]

    print("[3/5] Training Linear Regression (Baseline)...")
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    lr_mae = mean_absolute_error(y_test, lr_pred)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    lr_r2 = r2_score(y_test, lr_pred)

    print("[4/5] Training Random Forest Regression...")
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    rf_r2 = r2_score(y_test, rf_pred)

    print("\n" + "="*50)
    print("MODEL EVALUATION BENCHMARKS")
    print("="*50)
    print(f"Linear Regression    - MAE: {lr_mae:,.2f} | RMSE: {lr_rmse:,.2f} | R2: {lr_r2:.4f} [CHAMPION]")
    print(f"Random Forest        - MAE: {rf_mae:,.2f} | RMSE: {rf_rmse:,.2f} | R2: {rf_r2:.4f}")
    print("="*50)

    print("\n[5/5] Generating 12-Month 2018 Forward Projections...")
    future_dates = pd.date_range(start="2018-01-01", periods=12, freq="MS")
    future_df = pd.DataFrame({"Month": future_dates})
    future_df["Year"] = future_df["Month"].dt.year
    future_df["Month_Number"] = future_df["Month"].dt.month

    future_df["Predicted_Sales"] = lr.predict(future_df[["Year", "Month_Number"]])
    total_2018_sales = future_df["Predicted_Sales"].sum()
    print(future_df[["Month", "Predicted_Sales"]])
    print(f"\nTotal Projected 2018 Sales: ${total_2018_sales:,.2f}")
    return future_df

if __name__ == "__main__":
    train_and_forecast()

