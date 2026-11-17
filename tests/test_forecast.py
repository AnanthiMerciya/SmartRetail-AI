"""
SmartRetail AI - Unit Tests for Machine Learning Forecasting Pipeline
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

class TestForecastingPipeline(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_forecast_page_get(self):
        """Verify forecasting view loads successfully."""
        response = self.client.get('/forecast')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Machine Learning Sales Forecasting', response.data)

    def test_api_model_metrics(self):
        """Verify model evaluation metrics match expected benchmarks."""
        response = self.client.get('/api/model-metrics')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])

        metrics = json_data['metrics']
        self.assertEqual(metrics['best_model'], 'linear_regression')
        
        lr = metrics['models']['linear_regression']
        self.assertAlmostEqual(lr['r2_score'], 0.5734, places=2)
        self.assertAlmostEqual(lr['mae'], 12180.97, delta=100.0)

    def test_api_actual_vs_predicted(self):
        """Verify actual vs predicted test set contains 12 validation periods for 2017."""
        response = self.client.get('/api/actual-vs-predicted?model=linear_regression')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])

        data = json_data['data']
        self.assertEqual(len(data['months']), 12)
        self.assertEqual(len(data['actual']), 12)
        self.assertEqual(len(data['predicted']), 12)
        self.assertTrue(all(m.startswith('2017-') for m in data['months']))

    def test_api_forecast_horizon_12(self):
        """Verify 12-month future sales forecast projection starting in Jan 2018."""
        payload = {
            "model": "linear_regression",
            "horizon": 12
        }
        response = self.client.post('/api/forecast', json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])

        fc = json_data['forecast']
        self.assertEqual(fc['horizon_months'], 12)
        self.assertEqual(len(fc['table']), 12)
        self.assertEqual(fc['table'][0]['month'], '2018-01')
        self.assertEqual(fc['table'][-1]['month'], '2018-12')
        self.assertTrue(fc['total_predicted_sales'] > 600000.0)
        self.assertTrue(fc['highest_sales'] > fc['lowest_sales'])

    def test_api_forecast_horizon_3_and_6(self):
        """Verify quarterly (3-month) and semi-annual (6-month) horizons."""
        for horizon in [3, 6]:
            payload = {"model": "linear_regression", "horizon": horizon}
            response = self.client.post('/api/forecast', json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['success'])
            self.assertEqual(len(data['forecast']['table']), horizon)

    def test_download_forecast_csv(self):
        """Verify forecast CSV export route returns downloadable attachment."""
        response = self.client.get('/download/forecast-csv?model=linear_regression&horizon=12')
        self.assertEqual(response.status_code, 200)
        content_type = response.headers.get('Content-Type', '')
        self.assertTrue('text/csv' in content_type or 'application/vnd.ms-excel' in content_type)
        self.assertTrue(b'predicted_sales' in response.data)

if __name__ == '__main__':
    unittest.main()
