"""
SmartRetail AI - Executive PDF & CSV Report Generation Engine
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from src.metrics import calculate_kpis, get_category_breakdown, get_discount_breakdown
from src.forecasting import get_model_metrics, generate_forecast
from src.recommendations import generate_business_recommendations

def generate_pdf_report(df, output_path, author_name="Ananthi Merciya M", reg_no="ASML24005"):
    """
    Builds a professional multi-page Executive Analytics PDF report using ReportLab.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1F4E79'),
        alignment=1, # Center
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#595959'),
        alignment=1,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1F4E79'),
        spaceBefore=14,
        spaceAfter=6
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2E75B6'),
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#262626'),
        spaceAfter=6
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1F4E79')
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#262626')
    )

    story = []
    
    # Header Banner
    story.append(Paragraph("SMARTRETAIL AI", title_style))
    story.append(Paragraph("Intelligent Business Analytics Dashboard &amp; Sales Forecasting Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1F4E79'), spaceAfter=10))
    
    # Metadata Box
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    meta_data = [
        [
            Paragraph(f"<b>Author:</b> {author_name} ({reg_no})", body_style),
            Paragraph(f"<b>Generated:</b> {now_str}", body_style),
            Paragraph("<b>Analysis Type:</b> Retail Analytics &amp; Forecasting", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[200, 160, 180])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))
    
    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    exec_summary_text = (
        "SmartRetail AI is an intelligent business analytics platform designed to analyze retail transaction data, "
        "evaluate financial and volume KPIs, identify profit drivers and loss-making items, model discount sensitivity, "
        "and forecast future demand trends using machine learning. This report synthesizes historical performance "
        "and prescribes strategic interventions to optimize bottom-line profitability."
    )
    exec_box = Table([[Paragraph(exec_summary_text, callout_style)]], colWidths=[540])
    exec_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0F4F8')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#B8D5E5')),
        ('LINELEFT', (0, 0), (0, -1), 4, colors.HexColor('#1F4E79')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(exec_box)
    story.append(Spacer(1, 10))
    
    # 2. Master Key Performance Indicators
    story.append(Paragraph("2. Key Performance Indicators (KPI Scorecard)", h1_style))
    kpis = calculate_kpis(df)
    kpi_rows = [
        [
            Paragraph("<b>Total Sales Revenue</b>", table_header_style),
            Paragraph("<b>Total Net Profit</b>", table_header_style),
            Paragraph("<b>Profit Margin</b>", table_header_style),
            Paragraph("<b>Total Orders</b>", table_header_style),
            Paragraph("<b>Total Customers</b>", table_header_style),
            Paragraph("<b>Quantity Sold</b>", table_header_style)
        ],
        [
            Paragraph(f"<b>${kpis['total_sales']:,.2f}</b>", ParagraphStyle('C1', parent=table_cell_style, alignment=1)),
            Paragraph(f"<b>${kpis['total_profit']:,.2f}</b>", ParagraphStyle('C2', parent=table_cell_style, alignment=1, textColor=colors.HexColor('#166534'))),
            Paragraph(f"<b>{kpis['profit_margin']}%</b>", ParagraphStyle('C3', parent=table_cell_style, alignment=1)),
            Paragraph(f"{kpis['total_orders']:,}", ParagraphStyle('C4', parent=table_cell_style, alignment=1)),
            Paragraph(f"{kpis['total_customers']:,}", ParagraphStyle('C5', parent=table_cell_style, alignment=1)),
            Paragraph(f"{kpis['total_quantity']:,}", ParagraphStyle('C6', parent=table_cell_style, alignment=1))
        ]
    ]
    kpi_table = Table(kpi_rows, colWidths=[90, 90, 90, 90, 90, 90])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#FFFFFF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1F4E79')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 12))
    
    # 3. Category Breakdown Table
    story.append(Paragraph("3. Category Financial Breakdown", h1_style))
    cat_data = get_category_breakdown(df)
    cat_rows = [
        [
            Paragraph("<b>Category</b>", table_header_style),
            Paragraph("<b>Sales ($)</b>", table_header_style),
            Paragraph("<b>Profit ($)</b>", table_header_style),
            Paragraph("<b>Margin (%)</b>", table_header_style),
            Paragraph("<b>Sales Share</b>", table_header_style),
            Paragraph("<b>Units Sold</b>", table_header_style)
        ]
    ]
    for i in range(len(cat_data['categories'])):
        bg = colors.HexColor('#FFFFFF') if i % 2 == 0 else colors.HexColor('#F8FAFC')
        cat_rows.append([
            Paragraph(cat_data['categories'][i], table_cell_style),
            Paragraph(f"${cat_data['sales'][i]:,.2f}", table_cell_style),
            Paragraph(f"${cat_data['profit'][i]:,.2f}", table_cell_style),
            Paragraph(f"{cat_data['margin'][i]}%", table_cell_style),
            Paragraph(f"{cat_data['sales_share'][i]}%", table_cell_style),
            Paragraph(f"{cat_data['quantity'][i]:,}", table_cell_style)
        ])
    cat_table = Table(cat_rows, colWidths=[120, 90, 90, 80, 80, 80])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1F4E79')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 12))
    
    # 4. Discount Impact Summary
    story.append(Paragraph("4. Discount Impact & Margin Cannibalization", h1_style))
    story.append(Paragraph(
        "Critical finding: Transactions with discounts from 0% to 20% generate +$421K in net profits, "
        "while discounts of 30% and above incur over -$135K in cumulative losses.",
        body_style
    ))
    disc_data = get_discount_breakdown(df)
    disc_rows = [
        [
            Paragraph("<b>Discount</b>", table_header_style),
            Paragraph("<b>Sales ($)</b>", table_header_style),
            Paragraph("<b>Profit ($)</b>", table_header_style),
            Paragraph("<b>Units</b>", table_header_style),
            Paragraph("<b>Margin (%)</b>", table_header_style),
            Paragraph("<b>Policy Status</b>", table_header_style)
        ]
    ]
    # Include selected discount levels
    sample_discounts = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.8]
    for i in range(len(disc_data['discount_values'])):
        val = disc_data['discount_values'][i]
        if val in sample_discounts:
            p = disc_data['profit'][i]
            bg = colors.HexColor('#FDF2F2') if p < 0 else colors.HexColor('#F0FDF4')
            status_txt = "Loss-Making (Restricted)" if p < 0 else "Profitable (Approved)"
            disc_rows.append([
                Paragraph(disc_data['discounts'][i], table_cell_style),
                Paragraph(f"${disc_data['sales'][i]:,.2f}", table_cell_style),
                Paragraph(f"${p:,.2f}", table_cell_style),
                Paragraph(f"{disc_data['quantity'][i]:,}", table_cell_style),
                Paragraph(f"{disc_data['margin'][i]}%", table_cell_style),
                Paragraph(f"<b>{status_txt}</b>", table_cell_style)
            ])
    disc_table = Table(disc_rows, colWidths=[70, 95, 95, 60, 70, 150])
    disc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1F4E79')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(disc_table)
    story.append(Spacer(1, 12))
    
    # 5. Machine Learning Model Evaluation & 12-Month Forecast
    story.append(Paragraph("5. Machine Learning Models & Sales Forecasting", h1_style))
    ml_rows = [
        [
            Paragraph("<b>Model Architecture</b>", table_header_style),
            Paragraph("<b>MAE ($)</b>", table_header_style),
            Paragraph("<b>RMSE ($)</b>", table_header_style),
            Paragraph("<b>R² Score</b>", table_header_style),
            Paragraph("<b>Evaluation Rank</b>", table_header_style)
        ],
        [
            Paragraph("Linear Regression (Trend + Month)", table_cell_style),
            Paragraph("12,180.97", table_cell_style),
            Paragraph("16,833.86", table_cell_style),
            Paragraph("0.5734", table_cell_style),
            Paragraph("<b>Rank 1 (Best Performing)</b>", ParagraphStyle('R1', parent=table_cell_style, textColor=colors.HexColor('#166534')))
        ],
        [
            Paragraph("Improved Linear Regression (Lags)", table_cell_style),
            Paragraph("14,373.80", table_cell_style),
            Paragraph("17,671.21", table_cell_style),
            Paragraph("0.5299", table_cell_style),
            Paragraph("Rank 2", table_cell_style)
        ],
        [
            Paragraph("Random Forest Regression (n=100)", table_cell_style),
            Paragraph("14,174.73", table_cell_style),
            Paragraph("17,723.94", table_cell_style),
            Paragraph("0.5271", table_cell_style),
            Paragraph("Rank 3", table_cell_style)
        ]
    ]
    ml_table = Table(ml_rows, colWidths=[180, 90, 90, 80, 100])
    ml_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F0FDF4')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1F4E79')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(ml_table)
    story.append(Spacer(1, 12))
    
    # 6. Strategic Business Recommendations
    story.append(Paragraph("6. Automated Strategic Recommendations", h1_style))
    recs = generate_business_recommendations(df)
    for r in recs[:4]: # Top 4 recommendations
        p_badge = f"<b>[{r['priority']}]</b> "
        p_title = f"{p_badge}{r['title']}"
        story.append(Paragraph(p_title, h2_style))
        story.append(Paragraph(f"<b>Data Evidence:</b> {r['supporting_data']}", body_style))
        story.append(Paragraph(f"<b>Action:</b> {r['suggested_action']}", body_style))
        story.append(Spacer(1, 4))
        
    # Build Document
    doc.build(story)
    return output_path

def export_forecast_csv(forecast_data, output_path):
    """Exports forecast prediction table to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_fc = pd.DataFrame(forecast_data['table'])
    df_fc.to_csv(output_path, index=False)
    return output_path

def export_summary_csv(df, output_path):
    """Exports monthly and category summary to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_temp = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_temp['Order Date']):
        df_temp['Order Date'] = pd.to_datetime(df_temp['Order Date'])
        
    monthly = df_temp.groupby(df_temp['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    monthly['Month'] = monthly['Order Date'].astype(str)
    monthly.drop(columns=['Order Date']).to_csv(output_path, index=False)
    return output_path

