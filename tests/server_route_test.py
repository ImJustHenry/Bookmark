import unittest
import sys, os
sys.path.insert(0, os.path.abspath("./src"))

from flask_server import app

class TestServer(unittest.TestCase):
    #Set up Flask test client for each test.
    def setUp(self):
        self.client = app.test_client()

    def test_app_starts(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, [200,500])

    #server should not crash when loading homepage.
    def test_load_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bookmark!", response.data)

    # Ensures the UI search field exists.
    def test_homepage_has_search_input(self):
        response = self.client.get("/")
        self.assertIn(b'id="search_input"', response.data)

    #If status code 200, page loads. If 400,no book selected logic works.
    def test_results_not_crashing(self):
        response = self.client.get("/results")
        self.assertTrue(response.status_code in [200,400])

    # Ensures that the search query parameter exists
    def test_results_with_query_parameter(self):
        response = self.client.get("/results?query=test")
        self.assertIn(response.status_code, [200,400])
        
if __name__ == "__main__":
    unittest.main()