#!/usr/bin/env python3
"""Create and seed the company SQLite database used by Lab 58."""
import argparse
import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).with_name("company_database.db")


def create_sample_database(db_path=DEFAULT_DB):
    """Create related tables and insert deterministic sample records."""
    departments_data = [
        (1, "Human Resources", 101, 500000.00),
        (2, "Engineering", 102, 2000000.00),
        (3, "Marketing", 103, 800000.00),
        (4, "Sales", 104, 1200000.00),
        (5, "Finance", 105, 600000.00),
    ]
    employees_data = [
        (101, "John", "Smith", 1, 75000.00, "2020-01-15", "john.smith@company.com"),
        (102, "Sarah", "Johnson", 2, 95000.00, "2019-03-22", "sarah.johnson@company.com"),
        (103, "Mike", "Brown", 3, 68000.00, "2021-06-10", "mike.brown@company.com"),
        (104, "Lisa", "Davis", 4, 82000.00, "2020-09-05", "lisa.davis@company.com"),
        (105, "David", "Wilson", 5, 88000.00, "2018-11-30", "david.wilson@company.com"),
        (106, "Emma", "Taylor", 2, 72000.00, "2021-02-14", "emma.taylor@company.com"),
        (107, "James", "Anderson", 2, 78000.00, "2020-07-20", "james.anderson@company.com"),
        (108, "Maria", "Garcia", 3, 65000.00, "2022-01-08", "maria.garcia@company.com"),
        (109, "Robert", "Martinez", 4, 71000.00, "2021-04-12", "robert.martinez@company.com"),
        (110, "Jennifer", "Lee", 1, 69000.00, "2020-12-03", "jennifer.lee@company.com"),
    ]
    projects_data = [
        (1, "Website Redesign", 2, "2023-01-01", "2023-06-30", 150000.00, "Active"),
        (2, "Marketing Campaign Q1", 3, "2023-01-01", "2023-03-31", 75000.00, "Completed"),
        (3, "HR System Upgrade", 1, "2023-02-01", "2023-08-31", 120000.00, "Active"),
        (4, "Sales Training Program", 4, "2023-03-01", "2023-05-31", 50000.00, "Active"),
        (5, "Financial Audit", 5, "2023-01-15", "2023-04-15", 80000.00, "Completed"),
        (6, "Mobile App Development", 2, "2023-04-01", "2023-12-31", 300000.00, "Active"),
        (7, "Customer Survey", 3, "2023-02-15", "2023-04-30", 25000.00, "Completed"),
    ]
    connection = None
    try:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(db_path)
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS departments (
            department_id INTEGER PRIMARY KEY,
            department_name TEXT NOT NULL,
            manager_id INTEGER,
            budget REAL
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department_id INTEGER,
            salary REAL,
            hire_date DATE,
            email TEXT UNIQUE,
            FOREIGN KEY (department_id) REFERENCES departments (department_id)
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY,
            project_name TEXT NOT NULL,
            department_id INTEGER,
            start_date DATE,
            end_date DATE,
            budget REAL,
            status TEXT,
            FOREIGN KEY (department_id) REFERENCES departments (department_id)
        )""")
        cursor.executemany("""INSERT OR REPLACE INTO departments
            (department_id, department_name, manager_id, budget) VALUES (?, ?, ?, ?)""", departments_data)
        cursor.executemany("""INSERT OR REPLACE INTO employees
            (employee_id, first_name, last_name, department_id, salary, hire_date, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", employees_data)
        cursor.executemany("""INSERT OR REPLACE INTO projects
            (project_id, project_name, department_id, start_date, end_date, budget, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", projects_data)
        connection.commit()
        print("Sample database created successfully!")
        print("Tables created: employees, departments, projects")
        print(f"Database: {db_path}")
        return True
    except sqlite3.Error as error:
        if connection is not None:
            connection.rollback()
        print(f"Database setup failed: {error}")
        return False
    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Database file path")
    args = parser.parse_args()
    raise SystemExit(0 if create_sample_database(args.db) else 1)
