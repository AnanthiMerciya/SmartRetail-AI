"""
SmartRetail AI - Dashboard Routes & API
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from config import Config
from src.metrics import (
    calculate_kpis,
    get_monthly_sales_trend,
    get_yearly_breakdown,
    get_category_breakdown,
    get_region_breakdown,
    get_discount_breakdown
)

dashboard_bp = Blueprint('dashboard', __name__)

def load_active_data():
    """Loads current active cleaned dataset."""
    path = Config.DATASET_PROCESSED
    if not os.path.exists(path):
        path = Config.DATASET_RAW
    df = pd.read_csv(path)
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    if 'Year' not in df.columns:
        df['Year'] = df['Order Date'].dt.year
    return df

@dashboard_bp.route('/dashboard')
def dashboard_view():
    df = load_active_data()
    years = sorted(df['Year'].dropna().unique().astype(int).tolist())
    categories = sorted(df['Category'].dropna().unique().tolist()) if 'Category' in df.columns else []
    return render_template('dashboard.html', years=years, categories=categories)

@dashboard_bp.route('/api/dashboard')
def api_dashboard():
    try:
        df = load_active_data()
        
        # Apply optional filters
        year_filter = request.args.get('year')
        category_filter = request.args.get('category')
        
        if year_filter and year_filter != 'all':
            df = df[df['Year'] == int(year_filter)]
            
        if category_filter and category_filter != 'all':
            df = df[df['Category'] == category_filter]
            
        kpis = calculate_kpis(df)
        monthly_trend = get_monthly_sales_trend(df)
        yearly_data = get_yearly_breakdown(df)
        category_data = get_category_breakdown(df)
        region_data = get_region_breakdown(df)
        discount_data = get_discount_breakdown(df)
        
        return jsonify({
            "success": True,
            "kpis": kpis,
            "monthly_trend": monthly_trend,
            "yearly_data": yearly_data,
            "category_data": category_data,
            "region_data": region_data,
            "discount_data": discount_data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@dashboard_bp.route('/api/sales-by-year')
def api_sales_by_year():
    try:
        df = load_active_data()
        yearly = get_yearly_breakdown(df)
        return jsonify({"success": True, "data": yearly})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@dashboard_bp.route('/api/category-analysis')
def api_category_analysis():
    try:
        df = load_active_data()
        category = get_category_breakdown(df)
        return jsonify({"success": True, "data": category})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@dashboard_bp.route('/api/discount-analysis')
def api_discount_analysis():
    try:
        df = load_active_data()
        discount = get_discount_breakdown(df)
        return jsonify({"success": True, "data": discount})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

