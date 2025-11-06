import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from fetch_html import fetch_html

class TestFetchHTMLReal(unittest.TestCase):
    def test_fetch_html_real_page(self):
        url = "https://www.abebooks.com/"
        
        try:
            html = fetch_html(url)
        except Exception as e:
            self.fail(f"fetch_html raised an exception: {e}")
            return 
        
        self.assertIsInstance(html, str)
        self.assertIn("AbeBooks", html)
        self.assertIn("Books", html)
        self.assertTrue(len(html) > 100, "HTML seems too short — maybe not fetched properly.")

if __name__ == "__main__":
    unittest.main()
