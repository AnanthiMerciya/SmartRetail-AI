"""
SmartRetail AI - Report Export & Download Routes
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import pandas as pd
from flask import Blueprint, render_template, request, jsonify, send_file
from config import Config
from src.reports_generator import generate_pdf_report, export_summary_csv
from database.db import record_report, log_event

reports_bp = Blueprint('reports', __name__)

def load_dataset():
    path = Config.DATASET_PROCESSED
    if not os.path.exists(path):
        path = Config.DATASET_RAW
    return pd.read_csv(path)

@reports_bp.route('/reports')
@reports_bp.route('/report')
def reports_view():
    return render_template('reports.html')

@reports_bp.route('/api/export-report', methods=['POST'])
def api_export_report():
    try:
        data = request.get_json() or {}
        report_type = data.get('type', 'pdf').lower()
        df = load_dataset()
        
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        
        if report_type == 'pdf':
            pdf_path = os.path.join(Config.REPORTS_DIR, 'SmartRetail_AI_Analytics_Report.pdf')
            generate_pdf_report(df, pdf_path)
            record_report('PDF', 'SmartRetail_AI_Analytics_Report.pdf', pdf_path, len(df))
            log_event('REPORT_EXPORT', 'Generated Executive PDF Report')
            return jsonify({
                "success": True,
                "message": "PDF Report generated successfully.",
                "download_url": "/download/report-pdf"
            })
            
        elif report_type == 'csv':
            csv_path = os.path.join(Config.REPORTS_DIR, 'SmartRetail_AI_Monthly_Summary.csv')
            export_summary_csv(df, csv_path)
            record_report('CSV', 'SmartRetail_AI_Monthly_Summary.csv', csv_path, len(df))
            log_event('REPORT_EXPORT', 'Generated Monthly Summary CSV')
            return jsonify({
                "success": True,
                "message": "CSV Report generated successfully.",
                "download_url": "/download/report-csv"
            })
        else:
            return jsonify({"success": False, "error": "Invalid report type"}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@reports_bp.route('/download/report-pdf')
def download_pdf():
    pdf_path = os.path.join(Config.REPORTS_DIR, 'SmartRetail_AI_Analytics_Report.pdf')
    if not os.path.exists(pdf_path):
        # Generate on the fly
        df = load_dataset()
        generate_pdf_report(df, pdf_path)
    return send_file(pdf_path, as_attachment=True, download_name="SmartRetail_AI_Analytics_Report.pdf")

@reports_bp.route('/download/report-csv')
def download_csv():
    csv_path = os.path.join(Config.REPORTS_DIR, 'SmartRetail_AI_Monthly_Summary.csv')
    if not os.path.exists(csv_path):
        df = load_dataset()
        export_summary_csv(df, csv_path)
    return send_file(csv_path, as_attachment=True, download_name="SmartRetail_AI_Monthly_Summary.csv")

@reports_bp.route('/download/project-doc')
def download_project_doc():
    doc_path = os.path.join(Config.REPORTS_DIR, 'SmartRetail_AI_Project_Documentation.docx')
    if not os.path.exists(doc_path):
        doc_path = os.path.join(Config.BASE_DIR, '..', 'SmartRetail_AI_Project_Documentation.docx')
    if os.path.exists(doc_path):
        return send_file(doc_path, as_attachment=True, download_name="SmartRetail_AI_Project_Documentation.docx")
    return jsonify({"error": "Project documentation file not found"}), 404

