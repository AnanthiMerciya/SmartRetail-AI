"""
SmartRetail AI - Machine Learning Forecasting Routes
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
from flask import Blueprint, render_template, request, jsonify, send_file
from config import Config
from src.forecasting import (
    ensure_models_ready,
    generate_forecast,
    get_actual_vs_predicted,
    get_model_metrics
)
from src.reports_generator import export_forecast_csv
from database.db import record_forecast, log_event

forecast_bp = Blueprint('forecast', __name__)

def get_data_path():
    path = Config.DATASET_PROCESSED
    if not os.path.exists(path):
        path = Config.DATASET_RAW
    return path

@forecast_bp.route('/forecast')
@forecast_bp.route('/forecasting')
def forecast_view():
    return render_template('forecast.html')

@forecast_bp.route('/api/model-metrics')
def api_model_metrics():
    try:
        data_path = get_data_path()
        metrics = ensure_models_ready(data_path, Config.MODELS_DIR)
        return jsonify({"success": True, "metrics": metrics})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@forecast_bp.route('/api/actual-vs-predicted')
def api_actual_vs_predicted():
    try:
        model_name = request.args.get('model', 'linear_regression')
        data_path = get_data_path()
        results = get_actual_vs_predicted(model_name, data_path, Config.MODELS_DIR)
        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@forecast_bp.route('/api/forecast', methods=['POST'])
def api_forecast():
    try:
        data = request.get_json() or {}
        model_name = data.get('model', 'linear_regression')
        horizon = int(data.get('horizon', 12))
        
        if horizon not in [3, 6, 12]:
            horizon = 12
            
        data_path = get_data_path()
        forecast_res = generate_forecast(model_name, horizon, data_path, Config.MODELS_DIR)
        
        # Record forecast in DB
        record_forecast(
            model_name=model_name,
            horizon_months=horizon,
            total_predicted=forecast_res['total_predicted_sales'],
            highest_m=forecast_res['highest_month'],
            highest_s=forecast_res['highest_sales'],
            lowest_m=forecast_res['lowest_month'],
            lowest_s=forecast_res['lowest_sales'],
            params=f"Model: {model_name}, Horizon: {horizon}m"
        )
        log_event('FORECAST_GENERATED', f"Generated {horizon}-month forecast using {model_name}")
        
        return jsonify({
            "success": True,
            "forecast": forecast_res
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@forecast_bp.route('/download/forecast-csv')
def download_forecast_csv():
    try:
        model_name = request.args.get('model', 'linear_regression')
        horizon = int(request.args.get('horizon', 12))
        data_path = get_data_path()
        
        forecast_res = generate_forecast(model_name, horizon, data_path, Config.MODELS_DIR)
        csv_path = os.path.join(Config.REPORTS_DIR, f"forecast_{model_name}_{horizon}m.csv")
        export_forecast_csv(forecast_res, csv_path)
        
        return send_file(csv_path, as_attachment=True, download_name=f"SmartRetail_Forecast_{horizon}M.csv")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

