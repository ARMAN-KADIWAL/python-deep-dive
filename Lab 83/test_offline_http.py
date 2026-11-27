"""Exercise the HTTP examples without external traffic."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch
import basic_get
import post_request


class OfflineHTTPTests(unittest.TestCase):
    def test_get(self):
        response = Mock(status_code=200, headers={"content-type": "application/json"})
        response.json.return_value = {"id": 1, "title": "fixture"}
        with patch("basic_get.requests.get", return_value=response) as get:
            out = io.StringIO()
            with redirect_stdout(out):
                basic_get.make_basic_get_request()
            get.assert_called_once()
            self.assertIn("fixture", out.getvalue())
            self.assertIn("Request successful", out.getvalue())

    def test_post_and_put(self):
        for method, demo, status, expected in [
            ("post", post_request.create_new_post, 201, "Post created successfully"),
            ("put", post_request.update_existing_post, 200, "Post updated successfully"),
        ]:
            response = Mock(status_code=status)
            response.json.return_value = {"id": 1, "title": "fixture"}
            with patch(f"post_request.requests.{method}", return_value=response) as call:
                out = io.StringIO()
                with redirect_stdout(out):
                    demo()
                self.assertIn(expected, out.getvalue())
                self.assertIn("json", call.call_args.kwargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
