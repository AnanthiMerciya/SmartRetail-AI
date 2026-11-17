"""
SmartRetail AI - Comprehensive Sales & Profit Analysis Module
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import pandas as pd
import numpy as np

def run_full_analysis(df):
    """
    Executes the 10 required analysis dimensions on the retail dataset.
    Returns structured results for frontend visualization and tables.
    """
    results = {}
    
    # 1. Year-wise Analysis
    yearly = df.groupby('Year').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).reset_index().sort_values('Year')
    yearly['Margin'] = (yearly['Profit'] / yearly['Sales']) * 100
    results['year_wise'] = yearly.to_dict(orient='records')
    
    # 2. Monthly Trend Analysis (Aggregated over all years by month number)
    monthly_seasonality = df.groupby(['Month', 'Month Name']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values('Month')
    results['monthly_seasonality'] = monthly_seasonality.to_dict(orient='records')
    
    # 3. Category-wise Analysis
    cat = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Discount': 'mean'
    }).reset_index().sort_values('Sales', ascending=False)
    cat['Margin'] = (cat['Profit'] / cat['Sales']) * 100
    results['category_wise'] = cat.to_dict(orient='records')
    
    # 4. Sub-category-wise Analysis
    if 'Sub-Category' in df.columns:
        subcat = df.groupby(['Category', 'Sub-Category']).agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum',
            'Discount': 'mean'
        }).reset_index().sort_values('Sales', ascending=False)
        subcat['Margin'] = (subcat['Profit'] / subcat['Sales']) * 100
        results['subcategory_wise'] = subcat.to_dict(orient='records')
    else:
        results['subcategory_wise'] = []
        
    # 5. Region-wise Performance
    if 'Region' in df.columns:
        reg = df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index().sort_values('Profit', ascending=False)
        reg['Margin'] = (reg['Profit'] / reg['Sales']) * 100
        results['region_wise'] = reg.to_dict(orient='records')
    else:
        results['region_wise'] = []
        
    # 6. State-wise Performance (Top 10 & Bottom 10 states)
    if 'State' in df.columns:
        states = df.groupby('State').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index().sort_values('Sales', ascending=False)
        states['Margin'] = (states['Profit'] / states['Sales']) * 100
        results['top_states'] = states.head(10).to_dict(orient='records')
        results['bottom_states'] = states.sort_values('Profit').head(10).to_dict(orient='records')
    else:
        results['top_states'] = []
        results['bottom_states'] = []
        
    # 7. Product-wise Performance (Top 10 revenue & Top 10 profitable)
    if 'Product Name' in df.columns:
        prods = df.groupby(['Product ID', 'Product Name', 'Category']).agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        prods['Margin'] = (prods['Profit'] / prods['Sales']) * 100
        
        results['top_products_sales'] = prods.sort_values('Sales', ascending=False).head(10).to_dict(orient='records')
        results['top_products_profit'] = prods.sort_values('Profit', ascending=False).head(10).to_dict(orient='records')
        results['bottom_loss_products'] = prods[prods['Profit'] < 0].sort_values('Profit').head(10).to_dict(orient='records')
    else:
        results['top_products_sales'] = []
        results['top_products_profit'] = []
        results['bottom_loss_products'] = []
        
    # 8. Profit & Margin Analysis by Segment & Shipping Mode
    if 'Segment' in df.columns:
        segment = df.groupby('Segment').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index().sort_values('Sales', ascending=False)
        segment['Margin'] = (segment['Profit'] / segment['Sales']) * 100
        results['segment_wise'] = segment.to_dict(orient='records')
    else:
        results['segment_wise'] = []
        
    if 'Ship Mode' in df.columns:
        ship = df.groupby('Ship Mode').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index().sort_values('Sales', ascending=False)
        ship['Margin'] = (ship['Profit'] / ship['Sales']) * 100
        results['ship_wise'] = ship.to_dict(orient='records')
    else:
        results['ship_wise'] = []
        
    # 9. Discount Analysis (Critical finding: 0-20% profitable vs >=30% loss)
    disc = df.groupby('Discount').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values('Discount')
    disc['Margin'] = (disc['Profit'] / disc['Sales']) * 100
    disc['Status'] = disc['Profit'].apply(
        lambda p: 'Profitable' if p >= 0 else 'Loss-Making'
    )
    results['discount_wise'] = disc.to_dict(orient='records')
    
    # 10. Customer Analysis
    if 'Customer Name' in df.columns:
        cust = df.groupby(['Customer ID', 'Customer Name', 'Segment']).agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique'
        }).reset_index().sort_values('Sales', ascending=False)
        results['top_customers_sales'] = cust.head(10).to_dict(orient='records')
        results['top_customers_profit'] = cust.sort_values('Profit', ascending=False).head(10).to_dict(orient='records')
    else:
        results['top_customers_sales'] = []
        results['top_customers_profit'] = []
        
    return results

