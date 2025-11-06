import unittest
from flask_server import app

# Returns 404 not found instead of server crashing
class TestUnknownPaths(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_invalid_route(self):
        response = self.client.get("/urldoesntexist")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()