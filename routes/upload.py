"""
SmartRetail AI - Upload & Data Cleansing Routes
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
from flask import Blueprint, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from config import Config
from src.preprocessing import inspect_dataset, clean_and_process_dataset
from database.db import record_upload, log_event

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@upload_bp.route('/upload')
def upload_view():
    return render_template('upload.html')

@upload_bp.route('/api/upload', methods=['POST'])
def api_upload():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file part in the request"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No selected file"}), 400
            
        if not allowed_file(file.filename):
            return jsonify({
                "success": False, 
                "error": "Invalid file type. Only CSV and Excel (.xlsx, .xls) files are supported."
            }), 400
            
        safe_name = secure_filename(file.filename)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        raw_path = os.path.join(Config.UPLOAD_FOLDER, safe_name)
        file.save(raw_path)
        
        file_size = os.path.getsize(raw_path)
        
        # 1. Inspect dataset
        inspection = inspect_dataset(raw_path)
        if not inspection['is_valid']:
            return jsonify({
                "success": False,
                "error": f"Dataset is missing required columns: {', '.join(inspection['missing_columns'])}",
                "inspection": inspection
            }), 422
            
        # 2. Clean and process dataset
        cleaned_path = Config.DATASET_PROCESSED
        cleaning_result = clean_and_process_dataset(raw_path, cleaned_path)
        
        # 3. Record in SQLite Database
        upload_id = record_upload(
            filename=safe_name,
            original_name=file.filename,
            row_count=cleaning_result['processed_rows'],
            col_count=cleaning_result['columns_count'],
            file_size_bytes=file_size,
            cleaned_path=cleaned_path,
            notes=f"Cleaned and saved successfully. Dropped {cleaning_result['dropped_duplicates']} duplicates."
        )
        log_event('DATASET_UPLOAD', f"Uploaded and cleaned {file.filename} ({cleaning_result['processed_rows']} rows)")
        
        return jsonify({
            "success": True,
            "message": "Dataset uploaded, validated, and processed successfully!",
            "upload_id": upload_id,
            "filename": safe_name,
            "inspection": inspection,
            "cleaning": cleaning_result
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@upload_bp.route('/download/processed')
def download_processed():
    path = Config.DATASET_PROCESSED
    if not os.path.exists(path):
        path = Config.DATASET_RAW
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name="Superstore_Cleaned.csv")
    return jsonify({"error": "Processed dataset not found"}), 404

