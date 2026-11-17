"""
SmartRetail AI - Business Recommendations Routes
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import pandas as pd
from flask import Blueprint, render_template, jsonify
from config import Config
from src.recommendations import generate_business_recommendations

recommendations_bp = Blueprint('recommendations', __name__)

def load_dataset():
    path = Config.DATASET_PROCESSED
    if not os.path.exists(path):
        path = Config.DATASET_RAW
    return pd.read_csv(path)

@recommendations_bp.route('/recommendations')
@recommendations_bp.route('/recommendation')
def recommendations_view():
    return render_template('recommendations.html')

@recommendations_bp.route('/api/recommendations')
def api_recommendations():
    try:
        df = load_dataset()
        recs = generate_business_recommendations(df)
        return jsonify({
            "success": True,
            "recommendations": recs,
            "count": len(recs)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

