"""
SmartRetail AI - Machine Learning Sales Forecasting Pipeline
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def prepare_time_series(df):
    """Aggregates transactional retail data into regular monthly sales time series."""
    df_temp = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_temp['Order Date']):
        df_temp['Order Date'] = pd.to_datetime(df_temp['Order Date'])
        
    monthly = df_temp.groupby(df_temp['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly.columns = ['Month', 'Sales']
    monthly['Month_Dt'] = pd.to_datetime(monthly['Month'].astype(str))
    monthly['Year'] = monthly['Month_Dt'].dt.year
    monthly['Month_Number'] = monthly['Month_Dt'].dt.month
    monthly['Month_Str'] = monthly['Month_Dt'].dt.strftime('%Y-%m')
    
    # Feature engineering: Lags & Rolling
    monthly['Lag_1'] = monthly['Sales'].shift(1)
    monthly['Lag_2'] = monthly['Sales'].shift(2)
    monthly['Lag_12'] = monthly['Sales'].shift(12)
    monthly['Rolling_3'] = monthly['Sales'].shift(1).rolling(window=3).mean()
    
    return monthly

def train_and_save_models(data_path, models_dir):
    """
    Trains Linear Regression, Random Forest, and Lag-Engineered models,
    computes evaluation metrics, and serializes models using Joblib.
    """
    os.makedirs(models_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    ts = prepare_time_series(df)
    
    # Split chronologically: Train on years < 2017 (36 months), Test on 2017 (12 months)
    train_data = ts[ts['Year'] < 2017]
    test_data = ts[ts['Year'] == 2017]
    
    X_train = train_data[['Year', 'Month_Number']]
    y_train = train_data['Sales']
    X_test = test_data[['Year', 'Month_Number']]
    y_test = test_data['Sales']
    
    # 1. Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    
    lr_mae = float(mean_absolute_error(y_test, lr_pred))
    lr_rmse = float(np.sqrt(mean_squared_error(y_test, lr_pred)))
    lr_r2 = float(r2_score(y_test, lr_pred))
    
    # 2. Random Forest Regression
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    
    rf_mae = float(mean_absolute_error(y_test, rf_pred))
    rf_rmse = float(np.sqrt(mean_squared_error(y_test, rf_pred)))
    rf_r2 = float(r2_score(y_test, rf_pred))
    
    # 3. Lag-Engineered Linear Regression
    lag_clean = ts.dropna(subset=['Lag_12', 'Rolling_3'])
    train_lag = lag_clean[lag_clean['Year'] < 2017]
    test_lag = lag_clean[lag_clean['Year'] == 2017]
    
    lag_cols = ['Year', 'Month_Number', 'Lag_1', 'Lag_2', 'Lag_12', 'Rolling_3']
    X_train_lag = train_lag[lag_cols]
    y_train_lag = train_lag['Sales']
    X_test_lag = test_lag[lag_cols]
    y_test_lag = test_lag['Sales']
    
    improved_lr = LinearRegression()
    improved_lr.fit(X_train_lag, y_train_lag)
    improved_pred = improved_lr.predict(X_test_lag)
    
    improved_mae = float(mean_absolute_error(y_test_lag, improved_pred))
    improved_rmse = float(np.sqrt(mean_squared_error(y_test_lag, improved_pred)))
    improved_r2 = float(r2_score(y_test_lag, improved_pred))
    
    # Scaler artifact
    scaler = StandardScaler()
    scaler.fit(X_train)
    
    # Serialize Models
    joblib.dump(lr, os.path.join(models_dir, 'linear_regression.pkl'))
    joblib.dump(rf, os.path.join(models_dir, 'random_forest.pkl'))
    joblib.dump(improved_lr, os.path.join(models_dir, 'improved_linear_regression.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    
    metrics = {
        "models": {
            "linear_regression": {
                "name": "Linear Regression",
                "mae": round(lr_mae, 2),
                "rmse": round(lr_rmse, 2),
                "r2_score": round(lr_r2, 4),
                "is_best": True,
                "description": "Ordinary Least Squares regression capturing linear trend and calendar month seasonality."
            },
            "random_forest": {
                "name": "Random Forest Regression",
                "mae": round(rf_mae, 2),
                "rmse": round(rf_rmse, 2),
                "r2_score": round(rf_r2, 4),
                "is_best": False,
                "description": "Ensemble of 100 decision trees. Bounded by training extremes."
            },
            "improved_linear_regression": {
                "name": "Improved Linear Regression (Lags)",
                "mae": round(improved_mae, 2),
                "rmse": round(improved_rmse, 2),
                "r2_score": round(improved_r2, 4),
                "is_best": False,
                "description": "Autoregressive model utilizing Lag_1, Lag_2, Lag_12 and Rolling_3 features."
            }
        },
        "best_model": "linear_regression",
        "training_months": len(train_data),
        "test_months": len(test_data),
        "test_year": 2017
    }
    
    with open(os.path.join(models_dir, 'model_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=4)
        
    return metrics

def ensure_models_ready(data_path, models_dir):
    """Ensures trained model files and metrics exist; if not, triggers training."""
    lr_file = os.path.join(models_dir, 'linear_regression.pkl')
    rf_file = os.path.join(models_dir, 'random_forest.pkl')
    metrics_file = os.path.join(models_dir, 'model_metrics.json')
    
    if not (os.path.exists(lr_file) and os.path.exists(rf_file) and os.path.exists(metrics_file)):
        print("Training models for the first time...")
        return train_and_save_models(data_path, models_dir)
        
    with open(metrics_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_actual_vs_predicted(model_name, data_path, models_dir):
    """
    Returns actual historical test data vs model predictions for Chart.js.
    """
    ensure_models_ready(data_path, models_dir)
    df = pd.read_csv(data_path)
    ts = prepare_time_series(df)
    
    test_data = ts[ts['Year'] == 2017].copy()
    X_test = test_data[['Year', 'Month_Number']]
    y_actual = test_data['Sales'].tolist()
    
    model_file = 'linear_regression.pkl' if model_name != 'random_forest' else 'random_forest.pkl'
    model = joblib.load(os.path.join(models_dir, model_file))
    
    y_pred = model.predict(X_test).tolist()
    
    return {
        "months": test_data['Month_Str'].tolist(),
        "actual": [round(a, 2) for a in y_actual],
        "predicted": [round(p, 2) for p in y_pred]
    }

def generate_forecast(model_name, horizon_months, data_path, models_dir):
    """
    Generates multi-month future sales forecast (3, 6, or 12 months)
    starting from the month immediately following the dataset's latest date.
    """
    ensure_models_ready(data_path, models_dir)
    df = pd.read_csv(data_path)
    ts = prepare_time_series(df)
    
    latest_date = ts['Month_Dt'].max()
    future_start = latest_date + pd.DateOffset(months=1)
    
    future_dates = pd.date_range(start=future_start, periods=horizon_months, freq='MS')
    future_df = pd.DataFrame({"Month_Dt": future_dates})
    future_df['Year'] = future_df['Month_Dt'].dt.year
    future_df['Month_Number'] = future_df['Month_Dt'].dt.month
    future_df['Month_Str'] = future_df['Month_Dt'].dt.strftime('%Y-%m')
    future_df['Month_Name'] = future_df['Month_Dt'].dt.month_name()
    
    model_file = 'linear_regression.pkl' if model_name != 'random_forest' else 'random_forest.pkl'
    model = joblib.load(os.path.join(models_dir, model_file))
    
    X_future = future_df[['Year', 'Month_Number']]
    future_df['Predicted_Sales'] = model.predict(X_future)
    
    # Calculate statistics
    total_sales = float(future_df['Predicted_Sales'].sum())
    avg_sales = float(future_df['Predicted_Sales'].mean())
    
    highest_idx = future_df['Predicted_Sales'].idxmax()
    lowest_idx = future_df['Predicted_Sales'].idxmin()
    
    highest_month = str(future_df.loc[highest_idx, 'Month_Str'])
    highest_val = float(future_df.loc[highest_idx, 'Predicted_Sales'])
    
    lowest_month = str(future_df.loc[lowest_idx, 'Month_Str'])
    lowest_val = float(future_df.loc[lowest_idx, 'Predicted_Sales'])
    
    forecast_table = []
    for _, row in future_df.iterrows():
        forecast_table.append({
            "month": row['Month_Str'],
            "month_name": row['Month_Name'],
            "year": int(row['Year']),
            "predicted_sales": round(float(row['Predicted_Sales']), 2)
        })
        
    return {
        "model_used": model_name,
        "horizon_months": horizon_months,
        "total_predicted_sales": round(total_sales, 2),
        "average_monthly_sales": round(avg_sales, 2),
        "highest_month": highest_month,
        "highest_sales": round(highest_val, 2),
        "lowest_month": lowest_month,
        "lowest_sales": round(lowest_val, 2),
        "table": forecast_table,
        "chart": {
            "labels": future_df['Month_Str'].tolist(),
            "values": [round(float(v), 2) for v in future_df['Predicted_Sales'].tolist()]
        }
    }

get_model_metrics = ensure_models_ready

