# SmartRetail AI
## Intelligent Business Analytics Dashboard with Sales Forecasting and Decision Support Using Machine Learning

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.9-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)

---

### Academic Credentials
- **Student Name:** Ananthi Merciya M
- **Register Number:** ASML24005
- **Degree:** B.Sc. Artificial Intelligence and Machine Learning (AIML)
- **Course:** Final Year Capstone Project
- **Date of Completion:** November 2026

---

## 1. Project Overview

**SmartRetail AI** is a production-grade, full-stack business analytics and sales forecasting web application engineered to transform retail transaction records into strategic executive intelligence. The platform combines dynamic descriptive KPIs, multi-dimensional diagnostic analytics, time-series machine learning forecasting, and automated prescriptive decision directives.

### Key Capabilities
- **Executive BI Dashboard:** Live interactive KPI cards and 5 dynamic Chart.js visualizations with instant year and category filtering.
- **Dataset Ingestion Pipeline:** Drag-and-drop CSV and Excel (.xlsx, .xls) upload with schema validation, missing cell detection, automated deduplication, and cleaned CSV export.
- **10-Dimensional Deep Analysis:** Dedicated analytical matrices for Yearly trends, Monthly seasonality, Categories, 17 Sub-categories, 4 Geographic Regions, Top & Bottom 10 States, Top & Loss-making Products, Customer Segments, Shipping modes, and Discount elasticity.
- **Machine Learning Sales Forecasting:** Serialized Scikit-learn regression models (Linear Regression and Random Forest Regression) with 3, 6, and 12-month horizon projections, avoiding training latency on user requests.
- **Automated Prescriptive Directives:** Rule-based decision heuristics identifying the critical 20% discount profit threshold, chronic product loss bleeders, and Q4 inventory planning.
- **Multi-Format Export Suite:** Automated compilation of formal multi-page ReportLab PDF reports, raw financial summary CSVs, forecast prediction CSVs, and complete academic project Word documentation (.docx).

---

## 2. Dataset Reference Benchmarks

The application is benchmarked against the canonical **Superstore** retail transaction dataset:

| Metric | Reference Value |
| :--- | :--- |
| **Total Transaction Records** | 9,994 |
| **Dataset Columns** | 21 |
| **Gross Sales Revenue** | $2,297,200.86 |
| **Net Operating Profit** | $286,397.02 |
| **Net Profit Margin** | 12.47% |
| **Unique Customer Accounts** | 793 |
| **Unique Fulfilled Orders** | 5,009 |
| **Total Physical Units Sold** | 37,873 |
| **Operating Period** | Jan 03, 2014 &ndash; Dec 30, 2017 (48 Months) |

---

## 3. Machine Learning Model Evaluation

Models were evaluated using chronological out-of-time validation (Train: 2014&ndash;2016, 36 months; Test: 2017, 12 months) to strictly prevent future data leakage.

| Model Algorithm | MAE ($) | RMSE ($) | R² Score | Evaluation Status |
| :--- | :---: | :---: | :---: | :--- |
| **Linear Regression** | **12,180.97** | **16,833.86** | **0.5734** | **Best Performing Model** |
| **Random Forest Regression** | 14,174.73 | 17,723.94 | 0.5271 | Baseline Ensemble Model |
| **Improved LR (Lags + Rolling)** | 14,373.80 | 17,671.21 | 0.5299 | Autoregressive Features |

> **Why Linear Regression Outperformed Random Forest:**  
> Decision tree ensembles cannot extrapolate outside their historical training range. The training period had an all-time peak of $96,999 in December 2016; when the test set peaked at $118,447 in November 2017, Random Forest clipped its projection at the training maximum. In contrast, Linear Regression effectively captured the underlying secular trend and calendar month seasonality.

---

## 4. Project Folder Structure

```text
SmartRetail-AI/
├── app.py                          # Flask application factory and server entrypoint
├── config.py                       # Application configuration and path mappings
├── requirements.txt                # Python package dependencies
├── README.md                       # Project documentation and setup guide
│
├── dataset/
│   ├── raw/
│   │   └── Superstore.csv          # Canonical raw retail dataset (9,994 rows)
│   ├── processed/
│   │   └── Superstore_Cleaned.csv  # Feature-engineered cleaned dataset
│   └── uploads/                    # User uploaded CSV/Excel files
│
├── models/
│   ├── linear_regression.pkl       # Serialized best model (Joblib)
│   ├── random_forest.pkl           # Serialized ensemble model (Joblib)
│   ├── improved_linear_regression.pkl # Serialized lag-based model
│   ├── scaler.pkl                  # Feature scaler artifact
│   └── model_metrics.json          # Benchmark metrics and validation statistics
│
├── notebooks/
│   ├── 01_data_inspection.ipynb    # Data exploration and quality audit
│   ├── 02_data_cleaning.ipynb      # Deduplication and type standardization
│   ├── 03_exploratory_analysis.ipynb # Statistical EDA and correlation analysis
│   ├── 04_feature_engineering.ipynb # Resampling, lags, and rolling windows
│   └── 05_sales_forecasting.ipynb  # ML training and residual diagnostics
│
├── src/
│   ├── preprocessing.py            # Ingestion, validation, and feature engineering
│   ├── metrics.py                  # Dynamic KPI calculations and aggregations
│   ├── analysis.py                 # 10-dimensional diagnostic analytics processor
│   ├── forecasting.py              # Time-series ML pipeline and horizon projection
│   ├── recommendations.py          # Automated prescriptive decision engine
│   └── reports_generator.py        # ReportLab PDF compiler and CSV exporter
│
├── routes/
│   ├── dashboard.py                # Dashboard views and /api/dashboard
│   ├── upload.py                   # File upload pipeline and validation APIs
│   ├── analysis.py                 # Analytical dimensions and /api/analysis
│   ├── forecast.py                 # Forecast projection and /api/forecast
│   ├── recommendations.py          # Prescriptive directives and /api/recommendations
│   └── reports.py                  # Report download and export endpoints
│
├── templates/
│   ├── base.html                   # Dark navy & teal layout, sidebar, topbar
│   ├── index.html                  # Landing page with architecture and metrics
│   ├── dashboard.html              # KPI cards, filters, and 5 Chart.js panels
│   ├── upload.html                 # Drag-and-drop upload and schema inspector
│   ├── analysis.html               # 10-dimensional deep analysis tabbed interface
│   ├── forecast.html               # ML model selector, horizon controls, charts
│   ├── recommendations.html        # Filterable strategic recommendation cards
│   ├── reports.html                # PDF, CSV, and DOCX generation hub
│   └── about.html                  # Student profile and technical specifications
│
├── static/
│   ├── css/
│   │   └── style.css               # Professional dark navy and teal design system
│   └── js/
│       ├── charts.js               # Dark-themed Chart.js rendering factory
│       ├── dashboard.js            # Dashboard async fetch and filter bindings
│       ├── upload.js               # Drag-and-drop file upload and table preview
│       └── forecast.js             # Forecast execution, charts, and table bindings
│
├── database/
│   ├── db.py                       # SQLite database manager and audit logger
│   ├── schema.sql                  # Database schema definitions
│   └── smartretail.db              # Active SQLite database file
│
├── reports/
│   ├── SmartRetail_AI_Analytics_Report.pdf  # Compiled Executive PDF report
│   ├── SmartRetail_AI_Project_Documentation.docx # Academic documentation
│   └── charts/                     # Rendered charts cache
│
└── tests/
    ├── test_upload.py              # Unit tests for upload and validation pipeline
    ├── test_analysis.py            # Unit tests for KPIs and 10 analysis dimensions
    └── test_forecast.py            # Unit tests for ML models and projections
```

---

## 5. Installation and Setup

### Prerequisites
- Python 3.10 or 3.11 installed.
- Git (optional, for cloning).

### Step 1: Navigate to Project Directory
```bash
cd SmartRetail-AI
```

### Step 2: Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```
Open your browser and navigate to:  
**`http://127.0.0.1:5000`**

---

## 6. Running Automated Unit Tests

The test suite validates dataset validation, mathematical KPI accuracy against Superstore benchmarks, 10-dimensional analytical integrity, and machine learning forecast calculations:

```bash
# Run all unit tests
python -m unittest discover -s tests
```

Expected output:
```text
Ran 17 tests in 1.55s

OK
```

---

## 7. API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/dashboard` | Returns dynamic KPIs, monthly trends, yearly YoY, category, region, and discount breakdown. Supports `?year=` and `?category=` query parameters. |
| `POST` | `/api/upload` | Ingests CSV or Excel file via multipart/form-data. Validates required columns, cleans data, records upload in database, and returns schema audit. |
| `GET` | `/download/processed` | Downloads the active cleaned and feature-engineered dataset (`Superstore_Cleaned.csv`). |
| `GET` | `/api/analysis` | Computes all 10 analytical dimensions across sales, margins, states, products, and customer segments. |
| `GET` | `/api/sales-by-year` | Returns year-over-year revenue, profit, units, and margins. |
| `GET` | `/api/category-analysis`| Returns category sales distribution and margin health. |
| `GET` | `/api/discount-analysis`| Returns discount depth elasticity and profit impact curves. |
| `GET` | `/api/model-metrics` | Returns evaluation benchmarks (MAE, RMSE, R²) for Linear Regression, Random Forest, and Lag-based models. |
| `GET` | `/api/actual-vs-predicted` | Returns 2017 test set actual vs. model predicted sales. |
| `POST` | `/api/forecast` | Generates future multi-month sales forecast. Accepts JSON `{"model": "linear_regression", "horizon": 12}`. |
| `GET` | `/download/forecast-csv` | Exports future forecast projections as a downloadable CSV. |
| `GET` | `/api/recommendations` | Returns prioritized, data-driven prescriptive decision directives. |
| `POST` | `/api/export-report` | Compiles executive report. Accepts JSON `{"type": "pdf"}` or `{"type": "csv"}`. |
| `GET` | `/download/report-pdf` | Downloads the compiled multi-page ReportLab PDF analytics report. |
| `GET` | `/download/project-doc` | Downloads the complete Capstone Project Word Documentation (.docx). |

---

## 8. License & Academic Attribution
Developed by **Ananthi Merciya M** (Register No: `ASML24005`) for the final-year B.Sc. Artificial Intelligence and Machine Learning academic capstone project, November 2026. All rights reserved.

