

import unittest
import app
import json


class TestVariantEPredictorClass(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.application.test_client()
        
        
    def test_vep_class(self):
        vep_url = "http://127.0.0.1:5000/Variant Effect Predictor/vep/"
        # Simulate a GET request to /variant_recoder/human/ENST00000366667:c.803C>T

        #response = self.app.get("http://127.0.0.1:5000/Variant Effect Predictor/vep/human/hgvs/ENST00000366667%3Ac.803C%3ETs?Content-type=application%2Fjson")
        response = self.app.get(f"{vep_url}human/hgvs/%20ENST00000366667%3Ac.803C%3ET?Content-type=text%2Fxml&refseq=True&dbNSFP=chr")
        # Check the status code
        self.assertEqual(response.status_code, 200)
        content = response.get_json()
        self.assertEqual(len(content), 1)
        self.assertEqual(response.headers['Content-Type'], 'text/xml')
        self.assertEqual(content[0]['input'], 'ENST00000366667:c.803C>T')
        self.assertIsInstance(content, list)

class TestVariantValidatorClass(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.application.test_client()
    def test_vv_class(self):
        # Simulate a GET request to /variant_recoder/human/ENST00000366667:c.803C>T
        vv_url = "http://127.0.0.1:5000/Variant Validator/variantvalidator/"
        response = self.app.get(f"{vv_url}hg38/NM_001384479.1%3Ac.803C%3ET/NM_001384479.1?content-type=application%2Fjson")
        # Check the status code
        self.assertEqual(response.status_code, 200)
        content = response.get_json()
        self.assertEqual(len(content), 3)
        self.assertEqual(response.headers['Content-Type'], 'application/json')


class TestVariantRecoderClass(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.application.test_client()
    def test_vr_class(self):
        vr_url = "http://127.0.0.1:5000/Variant Recoder/variant_recoder/"
        # Simulate a GET request to /variant_recoder/human/ENST00000366667:c.803C>T

        #response = self.app.get("http://127.0.0.1:5000/Variant Effect Predictor/vep/human/hgvs/ENST00000366667%3Ac.803C%3ETs?Content-type=application%2Fjson")
        response = self.app.get(f"{vr_url}human/%20ENST00000366667%3Ac.803C%3ET?variant%20allele=t")
        # Check the status code
        self.assertEqual(response.status_code, 200)
        content = response.get_json()
        self.assertEqual(len(content), 1)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertIn('T', content)
        self.assertIsInstance(content, dict)    


if __name__ == '__main__':
    unittest.main()
    app.run()
