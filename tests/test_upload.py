"""
SmartRetail AI - Unit Tests for Upload and Ingestion Pipeline
Author: Ananthi Merciya M (Reg No: ASML24005)
"""

import os
import io
import shutil
import unittest
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from config import Config

class TestUploadPipeline(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Backup active cleaned dataset to prevent cross-test contamination
        self.backup_path = Config.DATASET_PROCESSED + '.test_bak'
        if os.path.exists(Config.DATASET_PROCESSED):
            shutil.copy2(Config.DATASET_PROCESSED, self.backup_path)

    def tearDown(self):
        # Restore active cleaned dataset
        if os.path.exists(self.backup_path):
            shutil.copy2(self.backup_path, Config.DATASET_PROCESSED)
            os.remove(self.backup_path)

    def test_upload_page_get(self):
        """Verify upload view loads successfully with 200 OK."""
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dataset Upload', response.data)

    def test_upload_missing_file_payload(self):
        """Verify POST /api/upload without file part returns 400."""
        response = self.client.post('/api/upload')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])

    def test_upload_invalid_extension(self):
        """Verify unsupported file extension returns 400."""
        data = {
            'file': (io.BytesIO(b"dummy,text,file"), 'test.txt')
        }
        response = self.client.post('/api/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertFalse(json_data['success'])
        self.assertIn('Invalid file type', json_data['error'])

    def test_upload_missing_required_columns(self):
        """Verify upload fails validation when required columns are absent."""
        invalid_csv = "Customer ID,Customer Name\n101,John Doe\n102,Jane Smith\n"
        data = {
            'file': (io.BytesIO(invalid_csv.encode('utf-8')), 'invalid.csv')
        }
        response = self.client.post('/api/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 422)
        json_data = response.get_json()
        self.assertFalse(json_data['success'])
        self.assertIn('missing required columns', json_data['error'])

    def test_upload_valid_sample_csv(self):
        """Verify valid retail CSV is ingested, cleaned, and logged successfully."""
        valid_csv = (
            "Order Date,Sales,Profit,Quantity,Discount,Category,Sub-Category,Region\n"
            "2016-01-15,250.00,45.00,2,0.1,Technology,Phones,West\n"
            "2016-02-20,120.00,-15.00,1,0.4,Furniture,Chairs,East\n"
            "2016-03-10,50.00,12.50,5,0.0,Office Supplies,Paper,Central\n"
        )
        data = {
            'file': (io.BytesIO(valid_csv.encode('utf-8')), 'sample_retail.csv')
        }
        response = self.client.post('/api/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['cleaning']['processed_rows'], 3)
        self.assertIn('upload_id', json_data)

    def test_download_processed_csv(self):
        """Verify processed dataset download endpoint works."""
        response = self.client.get('/download/processed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

if __name__ == '__main__':
    unittest.main()
