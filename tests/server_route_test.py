import unittest
import sys, os
sys.path.insert(0, os.path.abspath("./src"))

from flask_server import app

class TestServer(unittest.TestCase):
    #flask gives a test client for us to simulate the server
    def setUp(self):
        self.client = app.test_client()

    #server should not crash when loading homepage.
    def test_load_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bookmark!", response.data)

    #If status code 200, page loads. If 400,no book selected logic works.
    def test_results_not_crashing(self):
        response = self.client.get("/results")
        self.assertTrue(response.status_code in [200,400])
        
if __name__ == "__main__":
    unittest.main()