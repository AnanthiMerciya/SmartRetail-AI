"""
SmartRetail AI - Unit Tests for Analytics and Metrics Engine
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

class TestAnalysisEngine(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_analysis_page_get(self):
        """Verify sales analysis view loads successfully."""
        response = self.client.get('/analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Deep Diagnostic Sales Analysis', response.data)

    def test_api_dashboard_benchmark_kpis(self):
        """Verify API dashboard KPIs match exact Superstore benchmark values."""
        response = self.client.get('/api/dashboard')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])

        kpis = data['kpis']
        self.assertAlmostEqual(kpis['total_sales'], 2297200.86, places=1)
        self.assertAlmostEqual(kpis['total_profit'], 286397.02, places=1)
        self.assertAlmostEqual(kpis['profit_margin'], 12.47, places=1)
        self.assertEqual(kpis['total_orders'], 5009)
        self.assertEqual(kpis['total_customers'], 793)
        self.assertEqual(kpis['total_quantity'], 37873)

    def test_api_dashboard_filtered_by_year(self):
        """Verify dashboard responds accurately to temporal filtering."""
        response = self.client.get('/api/dashboard?year=2016')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        kpis = data['kpis']
        self.assertTrue(kpis['total_sales'] < 2297200.86)
        self.assertTrue(kpis['total_sales'] > 500000.0)

    def test_api_analysis_10_dimensions(self):
        """Verify API analysis endpoint computes all 10 analytical dimensions."""
        response = self.client.get('/api/analysis')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])
        res = json_data['data']

        # 1. Year-wise
        self.assertEqual(len(res['year_wise']), 4)
        # 2. Monthly Seasonality
        self.assertEqual(len(res['monthly_seasonality']), 12)
        # 3. Category-wise
        self.assertEqual(len(res['category_wise']), 3)
        # 4. Sub-category-wise
        self.assertEqual(len(res['subcategory_wise']), 17)
        # 5. Region-wise
        self.assertEqual(len(res['region_wise']), 4)
        # 6. States
        self.assertEqual(len(res['top_states']), 10)
        self.assertEqual(len(res['bottom_states']), 10)
        # 7. Products & Loss Leaders
        self.assertTrue(len(res['bottom_loss_products']) > 0)
        for p in res['bottom_loss_products']:
            self.assertTrue(p['Profit'] < 0)
        # 8. Customer & Segments
        self.assertEqual(len(res['segment_wise']), 3)
        self.assertEqual(len(res['ship_wise']), 4)
        # 9. Discount analysis
        self.assertTrue(len(res['discount_wise']) > 0)

    def test_api_endpoints_sub_routes(self):
        """Verify individual analytics API endpoints."""
        endpoints = [
            '/api/sales-by-year',
            '/api/category-analysis',
            '/api/discount-analysis'
        ]
        for ep in endpoints:
            res = self.client.get(ep)
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()

