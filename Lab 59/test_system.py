"""Automated Lab 59 tests; all DB changes use isolated temporary databases."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from database_report import generate_report
from database_setup import create_database
from security_demo import SecurityDemo
from user_management import UserManager


DEMO_USERS = (
    ("alice123", "alice@email.com", "Alice Johnson", 25, "New York"),
    ("bob456", "bob@email.com", "Bob Smith", 30, "Los Angeles"),
    ("charlie789", "charlie@email.com", "Charlie Brown", 22, "Chicago"),
    ("diana101", "diana@email.com", "Diana Prince", 28, "Miami"),
    ("eve202", "eve@email.com", "Eve Wilson", 35, "Seattle"),
)


class Lab59SystemTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db_name = Path(self.temp.name) / "user_management.db"
        self.manager = UserManager(self.db_name)

    def seed_users(self):
        return [self.manager.add_user(*data) for data in DEMO_USERS]

    def test_01_database_schema_and_idempotent_setup(self):
        ids = self.seed_users()
        create_database(self.db_name)
        with self.manager.connection() as conn:
            cols = [row[1] for row in conn.execute("PRAGMA table_info(users)")]
        self.assertEqual(cols, ["user_id", "username", "email", "full_name",
                                "age", "city", "created_date"])
        self.assertEqual(len(self.manager.find_users()), 5)
        self.assertEqual(self.manager.get_user_by_id(ids[0])[1], "alice123")

    def test_02_explicit_database_reset(self):
        self.seed_users()
        create_database(self.db_name, reset=True)
        self.assertEqual(self.manager.find_users(), [])

    def test_03_registration_and_normalization(self):
        user_id = self.manager.add_user(" Tester9 ", " Test@Example.COM ",
                                        "  jane smith ", 19, " new york ")
        row = self.manager.get_user_by_id(user_id)
        self.assertEqual(row[1:6], ("Tester9", "test@example.com",
                                    "Jane Smith", 19, "New York"))

    def test_04_registration_duplicate_username(self):
        self.manager.add_user(*DEMO_USERS[0])
        with self.assertRaises(sqlite3.IntegrityError):
            self.manager.add_user("alice123", "different@email.com", "Different", 20, "Miami")

    def test_05_registration_duplicate_email(self):
        self.manager.add_user(*DEMO_USERS[0])
        with self.assertRaises(sqlite3.IntegrityError):
            self.manager.add_user("unique1", "ALICE@email.com", "Different", 20, "Miami")

    def test_06_validate_emails(self):
        for email, valid in (("valid@email.com", True), ("invalid.email", False),
                             ("@invalid.com", False), ("valid.email@domain.co.uk", True),
                             ("", False)):
            with self.subTest(email=email):
                self.assertEqual(self.manager.validate_email(email), valid)

    def test_07_validate_usernames_and_ages(self):
        for username in ("ab", "bad_name", "space name", "x" * 21, "' OR 1=1--"):
            with self.subTest(username=username):
                with self.assertRaises(ValueError):
                    self.manager.add_user(username, "valid@email.com", "Valid", 20, "Pune")
        for age in (12, 121, "30", True):
            with self.subTest(age=age):
                with self.assertRaises(ValueError):
                    self.manager.add_user("valid123", "valid@email.com", "Valid", age, "Pune")

    def test_08_reject_empty_names_and_city(self):
        for name, city in (("", "Pune"), ("Tester", "  ")):
            with self.subTest(name=name, city=city):
                with self.assertRaises(ValueError):
                    self.manager.add_user("valid123", "valid@email.com", name, 20, city)

    def test_09_username_search_partial_case_insensitive(self):
        self.seed_users()
        results = self.manager.find_users("username", "ALI")
        self.assertEqual([r[1] for r in results], ["alice123"])

    def test_10_search_by_email(self):
        self.seed_users()
        self.assertEqual(len(self.manager.find_users("email", "@email.com")), 5)
        self.assertEqual(self.manager.find_users("email", "notfound"), [])

    def test_11_search_by_city(self):
        self.seed_users()
        self.assertEqual([r[1] for r in self.manager.find_users("city", "new")], ["alice123"])

    def test_12_search_by_age_range(self):
        self.seed_users()
        self.assertEqual({r[1] for r in self.manager.find_users(min_age=25, max_age=30)},
                         {"alice123", "bob456", "diana101"})
        with self.assertRaises(ValueError):
            self.manager.find_users(min_age=40, max_age=20)

    def test_13_search_field_allowlist_and_wildcard_literal(self):
        self.seed_users()
        with self.assertRaises(ValueError):
            self.manager.find_users("username; DROP TABLE users", "abc")
        with self.assertRaises(ValueError):
            self.manager.find_users("username", " ")
        self.assertEqual(self.manager.find_users("username", "%"), [])
        self.assertEqual(self.manager.find_users("username", "_"), [])
        self.assertEqual(len(self.manager.find_users()), 5)

    def test_14_update_all_editable_fields(self):
        ids = self.seed_users()
        user_id = ids[0]
        self.assertTrue(self.manager.update_user_record(user_id, "email", " NEW@EMAIL.COM "))
        self.assertTrue(self.manager.update_user_record(user_id, "full_name", " alice cooper "))
        self.assertTrue(self.manager.update_user_record(user_id, "age", 26))
        self.assertTrue(self.manager.update_user_record(user_id, "city", " mumbai "))
        self.assertEqual(self.manager.get_user_by_id(user_id)[1:6],
                         ("alice123", "new@email.com", "Alice Cooper", 26, "Mumbai"))

    def test_15_update_duplicate_email_rollback(self):
        ids = self.seed_users()
        with self.assertRaises(sqlite3.IntegrityError):
            self.manager.update_user_record(ids[0], "email", "bob@email.com")
        self.assertEqual(self.manager.get_user_by_id(ids[0])[2], "alice@email.com")

    def test_16_update_reject_bad_values_and_fields(self):
        ids = self.seed_users()
        for field, value in (("age", 0), ("age", "12"), ("email", "no-at"),
                             ("city", ""), ("full_name", " "),
                             ("username", "changed")):
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValueError):
                    self.manager.update_user_record(ids[0], field, value)
        self.assertFalse(self.manager.update_user_record(999999, "city", "Mumbai"))

    def test_17_delete_existing_and_missing_user(self):
        ids = self.seed_users()
        self.assertTrue(self.manager.delete_user_record(ids[0]))
        self.assertIsNone(self.manager.get_user_by_id(ids[0]))
        self.assertFalse(self.manager.delete_user_record(999999))
        self.assertEqual(len(self.manager.find_users()), 4)

    def test_18_delete_interactive_confirmations(self):
        ids = self.seed_users()
        with patch("builtins.input", side_effect=[str(ids[0]), "no"]), redirect_stdout(StringIO()):
            self.manager.delete_user()
        self.assertIsNotNone(self.manager.get_user_by_id(ids[0]))
        with patch("builtins.input", side_effect=[str(ids[0]), "yes", "wrong"]), redirect_stdout(StringIO()):
            self.manager.delete_user()
        self.assertIsNotNone(self.manager.get_user_by_id(ids[0]))
        with patch("builtins.input", side_effect=[str(ids[0]), "yes", "DELETE"]), redirect_stdout(StringIO()):
            self.manager.delete_user()
        self.assertIsNone(self.manager.get_user_by_id(ids[0]))

    def test_19_sql_injection_safe_vs_unsafe(self):
        malicious = "' OR 1=1 --"
        unsafe_sql, unsafe_count, safe_count = SecurityDemo.compare_queries(malicious)
        self.assertIn("OR 1=1", unsafe_sql)
        self.assertEqual(unsafe_count, 2)
        self.assertEqual(safe_count, 0)
        self.seed_users()
        self.assertEqual(SecurityDemo(self.db_name).safe_search_example(malicious), [])
        self.assertEqual(len(self.manager.find_users()), 5)

    def test_20_report_includes_aggregated_results(self):
        self.seed_users()
        output = generate_report(self.manager)
        self.assertIn("Total registered users: 5", output)
        self.assertIn("Age range: 22-35", output)
        self.assertIn("Average age: 28.0", output)
        self.assertIn("New York: 1", output)
        self.assertIn("alice123", output)

    def test_21_empty_database_report(self):
        output = generate_report(self.manager)
        self.assertIn("Total registered users: 0", output)
        self.assertIn("Age statistics: no registered users", output)

    def test_22_main_menu_register_search_update_delete_exit(self):
        responses = [
            "1", "testuser", "test@example.com", "Test User", "24", "Surat",
            "2", "1", "test",
            "3", "1", "4", "Ahmedabad",
            "4", "1", "yes", "DELETE",
            "5",
        ]
        out = StringIO()
        with patch("builtins.input", side_effect=responses), redirect_stdout(out):
            self.manager.main_menu()
        text = out.getvalue()
        self.assertIn("User registered successfully", text)
        self.assertIn("Found 1 user(s)", text)
        self.assertIn("User profile updated successfully", text)
        self.assertIn("Ahmedabad", text)
        self.assertIn("permanently deleted", text)
        self.assertIn("Thank you", text)
        self.assertEqual(self.manager.find_users(), [])

    def test_23_interactive_bad_input_and_duplicate_registration(self):
        self.manager.add_user(*DEMO_USERS[0])
        responses = [
            "not a number", "1",     # main menu choice
            "x_", "newuser123",      # username validation
            "invalid", "new@email.com", # email validation
            "", "Jane Doe",          # full name validation
            "twelve", "10", "20",    # age validation
            "", "Mumbai",            # city validation
            "5",                     # exit
        ]
        out = StringIO()
        with patch("builtins.input", side_effect=responses), redirect_stdout(out):
            self.manager.main_menu()
        self.assertIn("valid number", out.getvalue())
        self.assertIn("Username must", out.getvalue())
        self.assertIn("valid email", out.getvalue())
        self.assertIn("User registered successfully", out.getvalue())
        self.assertEqual(len(self.manager.find_users()), 2)

    def test_24_interactive_duplicate_registration(self):
        self.manager.add_user(*DEMO_USERS[0])
        responses = ["alice123", "different@email.com", "Another User", "21", "Pune"]
        out = StringIO()
        with patch("builtins.input", side_effect=responses), redirect_stdout(out):
            self.assertIsNone(self.manager.register_user())
        self.assertIn("already exists", out.getvalue())
        self.assertEqual(len(self.manager.find_users()), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
