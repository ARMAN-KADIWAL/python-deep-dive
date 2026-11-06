"""Automated tests for Lab 58 SQLite query examples."""
import sqlite3
import tempfile
import unittest
from pathlib import Path

import advanced_aggregation
import advanced_filtering
import advanced_joins
import filtering_queries
import grouping_aggregation
import join_operations
import sorting_limiting
from setup_database import create_sample_database


class Lab58Tests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "company_database.db"
        self.assertTrue(create_sample_database(self.db_path))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_setup_creates_three_tables_and_sample_rows(self):
        with sqlite3.connect(self.db_path) as connection:
            tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertTrue({"employees", "departments", "projects"}.issubset(tables))
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM employees").fetchone()[0], 10)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM departments").fetchone()[0], 5)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM projects").fetchone()[0], 7)

    def test_setup_is_repeatable(self):
        self.assertTrue(create_sample_database(self.db_path))
        with sqlite3.connect(self.db_path) as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM employees").fetchone()[0], 10)

    def test_basic_filtering_conditions(self):
        with sqlite3.connect(self.db_path) as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM employees WHERE salary > 75000").fetchone()[0], 4)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM employees WHERE department_id=2").fetchone()[0], 3)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM projects WHERE status='Active'").fetchone()[0], 4)

    def test_advanced_filtering_and_case(self):
        with sqlite3.connect(self.db_path) as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM employees WHERE department_id NOT IN (2,4)").fetchone()[0], 5)
            categories = connection.execute("SELECT DISTINCT CASE WHEN salary > 85000 THEN 'High' WHEN salary > 70000 THEN 'Medium' ELSE 'Low' END FROM employees").fetchall()
            self.assertEqual({row[0] for row in categories}, {"High", "Medium", "Low"})

    def test_sorting_and_limits(self):
        with sqlite3.connect(self.db_path) as connection:
            top = connection.execute("SELECT first_name, salary FROM employees ORDER BY salary DESC LIMIT 5").fetchall()
            self.assertEqual(len(top), 5)
            self.assertEqual(top[0][0], "Sarah")
            self.assertGreaterEqual(top[0][1], top[-1][1])

    def test_inner_and_left_joins(self):
        with sqlite3.connect(self.db_path) as connection:
            joined = connection.execute("SELECT COUNT(*) FROM employees e INNER JOIN departments d ON e.department_id=d.department_id").fetchone()[0]
            self.assertEqual(joined, 10)
            left = connection.execute("SELECT COUNT(*) FROM departments d LEFT JOIN employees e ON d.department_id=e.department_id").fetchone()[0]
            self.assertGreaterEqual(left, 10)

    def test_self_join_and_project_join(self):
        with sqlite3.connect(self.db_path) as connection:
            pairs = connection.execute("SELECT COUNT(*) FROM employees e1 JOIN employees e2 ON e1.department_id=e2.department_id AND e1.employee_id<e2.employee_id").fetchone()[0]
            self.assertEqual(pairs, 6)
            projects = connection.execute("SELECT COUNT(*) FROM projects p JOIN departments d ON p.department_id=d.department_id").fetchone()[0]
            self.assertEqual(projects, 7)

    def test_grouping_aggregation_and_having(self):
        with sqlite3.connect(self.db_path) as connection:
            grouped = connection.execute("SELECT department_id, COUNT(*) FROM employees GROUP BY department_id HAVING COUNT(*)>1").fetchall()
            self.assertEqual({row[0] for row in grouped}, {1, 2, 3, 4})
            totals = connection.execute("SELECT status, SUM(budget) FROM projects GROUP BY status").fetchall()
            self.assertEqual(len(totals), 2)

    def test_all_demonstration_functions_execute(self):
        for function in (
            filtering_queries.demonstrate_filtering,
            advanced_filtering.demonstrate_advanced_filtering,
            sorting_limiting.demonstrate_sorting_limiting,
            join_operations.demonstrate_joins,
            advanced_joins.demonstrate_advanced_joins,
            grouping_aggregation.demonstrate_grouping_aggregation,
            advanced_aggregation.demonstrate_advanced_aggregation,
        ):
            with self.subTest(function=function.__name__):
                results = function(self.db_path)
                self.assertTrue(results)
                self.assertTrue(all(isinstance(result, list) for result in results))


if __name__ == "__main__":
    unittest.main(verbosity=2)
