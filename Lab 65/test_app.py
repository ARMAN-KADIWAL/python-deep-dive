import unittest

from app import app


class IntroFlaskTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_main_routes(self):
        for path in ["/", "/about", "/contact", "/user/Arman", "/product/42"]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_dynamic_parameter_is_escaped(self):
        response = self.client.get("/user/%3Cscript%3E")
        self.assertNotIn(b"<script>", response.data)
        self.assertIn(b"&lt;script&gt;", response.data)

    def test_invalid_routes(self):
        self.assertEqual(self.client.get("/missing").status_code, 404)
        self.assertEqual(self.client.get("/product/no-number").status_code, 404)


if __name__ == "__main__":
    unittest.main()
