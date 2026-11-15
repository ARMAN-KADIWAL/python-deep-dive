import unittest

from app import app


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_pages_and_templates(self):
        for path in ["/", "/user/Arman", "/users", "/users/active",
                     "/search", "/search/results?q=Flask", "/item/1"]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_search_and_filter(self):
        result = self.client.get("/search/results?q=flask&category=tutorial")
        # Three tutorial descriptions/titles contain "Flask".
        self.assertIn(b"Results Found:</strong> 3", result.data)
        self.assertNotIn(b"Web Development News", result.data)
        self.assertIn(b"Flask Templates Guide", result.data)
        empty = self.client.get("/search/results?q=unmatchedterm")
        self.assertIn(b"No Results Found", empty.data)

    def test_users_and_404(self):
        active = self.client.get("/users/active")
        self.assertNotIn(b"Charlie Brown", active.data)
        self.assertEqual(self.client.get("/item/999").status_code, 404)


if __name__ == "__main__":
    unittest.main()
