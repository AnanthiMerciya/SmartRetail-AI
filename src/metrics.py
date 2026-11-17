"""
SmartRetail AI - Metrics & KPI Calculation Engine
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import pandas as pd
import numpy as np

def calculate_kpis(df):
    """Calculates master high-level KPIs from retail DataFrame."""
    total_sales = float(df['Sales'].sum())
    total_profit = float(df['Profit'].sum())
    total_quantity = int(df['Quantity'].sum())
    
    total_orders = int(df['Order ID'].nunique()) if 'Order ID' in df.columns else len(df)
    total_customers = int(df['Customer ID'].nunique()) if 'Customer ID' in df.columns else 0
    
    profit_margin = float((total_profit / total_sales * 100)) if total_sales > 0 else 0.0
    avg_order_value = float(total_sales / total_orders) if total_orders > 0 else 0.0
    
    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_quantity": total_quantity,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "profit_margin": round(profit_margin, 2),
        "avg_order_value": round(avg_order_value, 2)
    }

def get_monthly_sales_trend(df):
    """Returns monthly aggregate sales and profit series formatted for Chart.js."""
    df_temp = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_temp['Order Date']):
        df_temp['Order Date'] = pd.to_datetime(df_temp['Order Date'])
        
    monthly = df_temp.groupby(df_temp['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    monthly['Month_Str'] = monthly['Order Date'].astype(str)
    
    return {
        "labels": monthly['Month_Str'].tolist(),
        "sales": [round(s, 2) for s in monthly['Sales'].tolist()],
        "profit": [round(p, 2) for p in monthly['Profit'].tolist()],
        "quantity": monthly['Quantity'].tolist()
    }

def get_yearly_breakdown(df):
    """Returns year-over-year sales and profit summary."""
    yearly = df.groupby('Year').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values('Year')
    
    yearly['Margin'] = (yearly['Profit'] / yearly['Sales']) * 100
    
    return {
        "years": yearly['Year'].astype(str).tolist(),
        "sales": [round(s, 2) for s in yearly['Sales'].tolist()],
        "profit": [round(p, 2) for p in yearly['Profit'].tolist()],
        "margin": [round(m, 2) for m in yearly['Margin'].tolist()]
    }

def get_category_breakdown(df):
    """Returns category-wise financial and volume breakdown."""
    cat = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values('Sales', ascending=False)
    
    total_sales = cat['Sales'].sum()
    cat['Sales_Share'] = (cat['Sales'] / total_sales) * 100 if total_sales > 0 else 0
    cat['Margin'] = (cat['Profit'] / cat['Sales']) * 100
    
    return {
        "categories": cat['Category'].tolist(),
        "sales": [round(s, 2) for s in cat['Sales'].tolist()],
        "profit": [round(p, 2) for p in cat['Profit'].tolist()],
        "quantity": cat['Quantity'].tolist(),
        "margin": [round(m, 2) for m in cat['Margin'].tolist()],
        "sales_share": [round(sh, 2) for sh in cat['Sales_Share'].tolist()]
    }

def get_region_breakdown(df):
    """Returns regional sales and profit breakdown."""
    if 'Region' not in df.columns:
        return {"regions": [], "sales": [], "profit": []}
        
    reg = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values('Sales', ascending=False)
    
    reg['Margin'] = (reg['Profit'] / reg['Sales']) * 100
    
    return {
        "regions": reg['Region'].tolist(),
        "sales": [round(s, 2) for s in reg['Sales'].tolist()],
        "profit": [round(p, 2) for p in reg['Profit'].tolist()],
        "margin": [round(m, 2) for m in reg['Margin'].tolist()]
    }

def get_discount_breakdown(df):
    """Computes profit and volume across discount brackets."""
    disc = df.groupby('Discount').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values('Discount')
    
    disc['Margin'] = (disc['Profit'] / disc['Sales']) * 100
    disc['Recommendation'] = disc['Profit'].apply(
        lambda p: 'Approved: Profitable' if p >= 0 else 'Review: Loss-Making Discount'
    )
    
    return {
        "discounts": [f"{int(d*100)}%" for d in disc['Discount'].tolist()],
        "discount_values": disc['Discount'].tolist(),
        "sales": [round(s, 2) for s in disc['Sales'].tolist()],
        "profit": [round(p, 2) for p in disc['Profit'].tolist()],
        "quantity": disc['Quantity'].tolist(),
        "margin": [round(m, 2) for m in disc['Margin'].tolist()],
        "recommendations": disc['Recommendation'].tolist()
    }

