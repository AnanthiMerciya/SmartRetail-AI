"""
SmartRetail AI - Sales & Profit Analysis Routes
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import pandas as pd
from flask import Blueprint, render_template, jsonify
from config import Config
from src.analysis import run_full_analysis

analysis_bp = Blueprint('analysis', __name__)

def load_dataset():
    path = Config.DATASET_PROCESSED
    if not os.path.exists(path):
        path = Config.DATASET_RAW
    df = pd.read_csv(path)
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    if 'Year' not in df.columns:
        df['Year'] = df['Order Date'].dt.year
    if 'Month' not in df.columns:
        df['Month'] = df['Order Date'].dt.month
    if 'Month Name' not in df.columns:
        df['Month Name'] = df['Order Date'].dt.month_name()
    return df

@analysis_bp.route('/analysis')
@analysis_bp.route('/analytics')
def analysis_view():
    return render_template('analysis.html')

@analysis_bp.route('/api/analysis')
def api_analysis():
    try:
        df = load_dataset()
        results = run_full_analysis(df)
        return jsonify({
            "success": True,
            "data": results
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

