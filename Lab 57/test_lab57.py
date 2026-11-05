import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

import data_deletion
import data_insertion
import data_queries
import data_updates
from student_management import create_students_table


class SQLiteLabTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_students.db"
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.assertTrue(create_students_table(self.connection))
        self.sample = [
            ("John", "Doe", "john@example.com", 20, "Computer Science", 3.75),
            ("Jane", "Smith", "jane@example.com", 19, "Mathematics", 3.90),
            ("Mike", "Johnson", "mike@example.com", 21, "Computer Science", 3.60),
        ]
        self.assertEqual(data_insertion.insert_multiple_students(self.connection, self.sample), 3)

    def tearDown(self):
        self.connection.close()
        self.temp_dir.cleanup()

    def test_database_table_exists(self):
        columns = self.connection.execute("PRAGMA table_info(students)").fetchall()
        self.assertIn("student_id", [column["name"] for column in columns])

    def test_single_insert_and_duplicate_email(self):
        row = ("Sam", "Green", "sam@example.com", 22, "Physics", 3.4)
        self.assertIsNotNone(data_insertion.insert_single_student(self.connection, row))
        self.assertIsNone(data_insertion.insert_single_student(self.connection, row))

    def test_query_filter_search_and_aggregate(self):
        self.assertEqual(len(data_queries.query_all_students(self.connection)), 3)
        self.assertEqual(len(data_queries.query_students_by_major(self.connection, "Computer Science")), 2)
        self.assertEqual(len(data_queries.query_high_performing_students(self.connection, 3.8)), 1)
        self.assertEqual(len(data_queries.search_students(self.connection, "John")), 2)
        self.assertEqual(data_queries.query_student_statistics(self.connection)["overall"]["total_students"], 3)

    def test_update_gpa_major_and_contact(self):
        self.assertTrue(data_updates.update_student_gpa(self.connection, 1, 3.85))
        self.assertTrue(data_updates.update_student_major(self.connection, 2, "Applied Mathematics"))
        self.assertTrue(data_updates.update_student_contact(self.connection, 3, "mike.new@example.com", 22))
        self.assertEqual(self.connection.execute("SELECT gpa FROM students WHERE student_id=1").fetchone()[0], 3.85)
        self.assertFalse(data_updates.update_student_gpa(self.connection, 1, 5.0))

    def test_bulk_gpa_update_requires_confirmation(self):
        self.assertFalse(data_updates.bulk_update_gpa_by_major(self.connection, "Computer Science", 0.1, "n"))
        self.assertTrue(data_updates.bulk_update_gpa_by_major(self.connection, "Computer Science", 0.1, "y"))
        values = [row[0] for row in self.connection.execute("SELECT gpa FROM students WHERE major='Computer Science'")]
        self.assertAlmostEqual(sum(values), 7.55)

    def test_single_delete_creates_backup_and_requires_confirmation(self):
        folder = Path(self.temp_dir.name) / "single_backups"
        self.assertFalse(data_deletion.delete_student_by_id(self.connection, 1, confirm="no", backup_dir=folder))
        self.assertIsNotNone(self.connection.execute("SELECT 1 FROM students WHERE student_id=1").fetchone())
        self.assertTrue(data_deletion.delete_student_by_id(self.connection, 1, confirm="DELETE", backup_dir=folder))
        self.assertIsNone(self.connection.execute("SELECT 1 FROM students WHERE student_id=1").fetchone())
        backups = [json.loads(path.read_text(encoding="utf-8")) for path in folder.glob("*.json")]
        self.assertEqual(len(backups), 2)
        self.assertTrue(all(item["email"] == "john@example.com" for item in backups))

    def test_bulk_delete_allowlist_backup_and_confirmation(self):
        folder = Path(self.temp_dir.name) / "bulk_backups"
        self.assertFalse(data_deletion.delete_students_by_criteria(self.connection, "major; DROP TABLE students", "Computer Science", "DELETE", folder))
        self.assertFalse(data_deletion.delete_students_by_criteria(self.connection, "major", "Computer Science", "no", folder))
        self.assertTrue(data_deletion.delete_students_by_criteria(self.connection, "major", "Computer Science", "DELETE", folder))
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM students").fetchone()[0], 1)
        files = list(folder.glob("*.json"))
        self.assertTrue(files)
        self.assertEqual(len(json.loads(files[-1].read_text(encoding="utf-8"))), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
