import csv
import io
import re
import tempfile
import unittest
from pathlib import Path

import app as lab


def token(response):
    match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
    if match is None:
        raise AssertionError("CSRF token missing from HTML")
    return match.group(1).decode()


class FormsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        lab.DATA_DIR = Path(self.tmp.name)
        lab.DATA_FILE = lab.DATA_DIR / "submissions.json"
        lab.TEXT_FILE = lab.DATA_DIR / "form_data.txt"
        lab.app.config["TESTING"] = True
        self.client = lab.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def submit_valid(self):
        csrf = token(self.client.get("/"))
        return self.client.post("/submit", data={
            "csrf_token": csrf, "first_name": "Arman", "last_name": "Kadiwal",
            "email": "arman@example.com", "phone": "123-456-7890",
            "age": "20", "country": "India", "interests": ["Python", "Data Science"],
            "message": "Practicing Flask forms in my lab.", "newsletter": "yes",
        })

    def test_routes_validation_and_persistence(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/submissions").status_code, 200)
        self.assertEqual(self.client.post("/submit", data={}).status_code, 400)
        csrf = token(self.client.get("/"))
        bad = self.client.post("/submit", data={"csrf_token": csrf, "first_name": "A"})
        self.assertEqual(bad.status_code, 302)
        self.assertEqual(len(lab.load_submissions()), 0)
        self.assertEqual(self.submit_valid().status_code, 302)
        self.assertEqual(len(lab.load_submissions()), 1)
        self.assertTrue(lab.TEXT_FILE.exists())
        self.assertIn(b"Arman", self.client.get("/submission/0").data)
        self.assertEqual(self.client.get("/submission/99").status_code, 302)

    def test_export_and_clear(self):
        self.submit_valid()
        export = self.client.get("/export")
        self.assertEqual(export.status_code, 200)
        rows = list(csv.reader(io.StringIO(export.get_data(as_text=True))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(self.client.get("/clear").status_code, 405)
        csrf = token(self.client.get("/submissions"))
        cleared = self.client.post("/clear", data={"csrf_token": csrf})
        self.assertEqual(cleared.status_code, 302)
        self.assertEqual(len(lab.load_submissions()), 0)


if __name__ == "__main__":
    unittest.main()
