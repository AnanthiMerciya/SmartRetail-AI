"""
SmartRetail AI - Enterprise Web Application Entrypoint
Author: Ananthi Merciya M (Reg No: ASML24005)
Project: B.Sc. Artificial Intelligence & Machine Learning Capstone
"""

import os
from flask import Flask, render_template
from config import Config
from database.db import init_db
from routes.dashboard import dashboard_bp
from routes.upload import upload_bp
from routes.analysis import analysis_bp
from routes.forecast import forecast_bp
from routes.recommendations import recommendations_bp
from routes.reports import reports_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize SQLite database schema
    init_db()
    
    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(forecast_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(reports_bp)
    
    @app.route('/')
    @app.route('/home')
    @app.route('/index')
    def index():
        return render_template('index.html')
        
    @app.route('/about')
    def about():
        return render_template('about.html')
        
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', 5000))
    print(f"================================================================")
    print(f"  SMARTRETAIL AI - ENTERPRISE BUSINESS ANALYTICS DASHBOARD")
    print(f"  Running on: http://127.0.0.1:{port}")
    print(f"  Author: Ananthi Merciya M (Reg No: ASML24005)")
    print(f"================================================================")
    app.run(host='0.0.0.0', port=port, debug=True)

