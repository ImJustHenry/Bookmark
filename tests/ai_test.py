import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ai import get_recommendations   

class TestRecommendations(unittest.TestCase):

    # Test when no API key exists
    @patch.dict(os.environ, {}, clear=True)
    def test_no_api_key(self):
        recs = get_recommendations([], "Test Book")
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["title"], "Test Book")
        self.assertIn("No AI recommendations", recs[0]["summary"])

    # Test successful AI response (mocked)
    @patch("ai.genai.Client")
    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake"})
    def test_mocked_ai_response(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value.text = """
        [
            {"title": "Book A", "summary": "Summary A"},
            {"title": "Book B", "summary": "Summary B"}
        ]
        """
        mock_client_class.return_value = mock_client

        recs = get_recommendations(["1984"], "Dune")

        self.assertEqual(len(recs), 2)
        self.assertEqual(recs[0]["title"], "Book A")

    # Test string previous_searches
    def test_string_previous_search(self):
        recs = get_recommendations("Harry Potter", "The Hobbit")
        self.assertTrue(isinstance(recs, list))

if __name__ == "__main__":
    unittest.main()
