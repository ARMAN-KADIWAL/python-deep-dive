import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import handle_json_errors
import modify_json
import parse_nested_json
import read_json
import write_json


class TestJsonLab(unittest.TestCase):
    def test_sample_json_files_are_valid(self):
        base = Path(__file__).parent
        for filename in ("student_data.json", "university_data.json"):
            with (base / filename).open(encoding="utf-8") as file:
                self.assertIsInstance(json.load(file), dict)

    def test_read_json_functions_run(self):
        base = Path(__file__).parent
        original_directory = os.getcwd()
        try:
            os.chdir(base)
            output = StringIO()
            with redirect_stdout(output):
                read_json.read_simple_json()
                read_json.read_complex_json()
                read_json.demonstrate_json_methods()
        finally:
            os.chdir(original_directory)
        self.assertIn("Alice Johnson", output.getvalue())
        self.assertIn("Tech University", output.getvalue())

    def test_write_json_outputs(self):
        original_directory = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                with redirect_stdout(StringIO()):
                    write_json.write_simple_json()
                    write_json.write_complex_json()
                    write_json.write_list_to_json()
            finally:
                os.chdir(original_directory)
            for filename in ("employee_data.json", "company_data.json", "company_data_compact.json", "students_list.json"):
                with open(Path(directory) / filename, encoding="utf-8") as file:
                    json.load(file)

    def test_nested_json_search(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "nested.json"
            parse_nested_json.create_complex_json_file(filename)
            result = parse_nested_json.search_json_data(filename)
        self.assertEqual(result["dark_theme_users"], ["Alice Johnson"])
        self.assertEqual(result["email_enabled_users"], ["Alice Johnson"])
        self.assertEqual(result["high_activity_users"][0]["total_time"], 144)

    def test_safe_loader_returns_data_and_default(self):
        with tempfile.TemporaryDirectory() as directory:
            good = Path(directory) / "good.json"
            good.write_text('{"answer": 42}', encoding="utf-8")
            self.assertEqual(handle_json_errors.load_json_safely(good), {"answer": 42})
            self.assertEqual(handle_json_errors.load_json_safely(Path(directory) / "missing.json", {}), {})

    def test_safe_loader_handles_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.json"
            invalid.write_text('{"value": }', encoding="utf-8")
            self.assertEqual(handle_json_errors.load_json_safely(invalid, []), [])

    def test_user_validation(self):
        errors, warnings = handle_json_errors.validate_user_data(
            {"id": 1, "name": "Alice", "email": "alice@example.com"}
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        errors, warnings = handle_json_errors.validate_user_data(
            {"id": "1", "name": "Eve", "email": "invalid-email"}
        )
        self.assertIn("Field 'id' must be an integer", errors)
        self.assertIn("Email format may be invalid", warnings)

    def test_modify_json_adds_updates_and_removes_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.json"
            destination = Path(directory) / "updated.json"
            source.write_text(json.dumps({"name": "Alice", "gpa": 3.5, "active": True}), encoding="utf-8")
            result = modify_json.modify_student_data(source, destination)
            self.assertEqual(result["gpa"], 3.9)
            self.assertEqual(result["phone"], "+1-555-0100")
            self.assertNotIn("active", result)
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8")), result)

    def test_intentionally_malformed_fixtures_are_rejected(self):
        base = Path(__file__).parent
        for filename in ("malformed_json.json", "invalid_syntax.json"):
            with (base / filename).open(encoding="utf-8") as file:
                with self.assertRaises(json.JSONDecodeError):
                    json.load(file)


if __name__ == "__main__":
    unittest.main(verbosity=2)
