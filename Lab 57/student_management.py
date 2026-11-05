#!/usr/bin/env python3
"""Create the SQLite database and students table."""
import argparse
import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).with_name("student_records.db")


def create_database(db_path=DEFAULT_DB):
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        print("✓ Database connection established successfully")
        return connection
    except sqlite3.Error as error:
        print(f"✗ Error creating database: {error}")
        return None


def create_students_table(connection):
    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                major TEXT,
                gpa REAL,
                enrollment_date DATE DEFAULT CURRENT_DATE
            )
        """)
        connection.commit()
        print("✓ Students table created successfully")
        return True
    except sqlite3.Error as error:
        connection.rollback()
        print(f"✗ Error creating table: {error}")
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    args = parser.parse_args()
    print("=== Student Management System ===")
    connection = create_database(args.db)
    if connection is None:
        raise SystemExit(1)
    try:
        if not create_students_table(connection):
            raise SystemExit(1)
    finally:
        connection.close()
        print("✓ Database connection closed")


if __name__ == "__main__":
    main()
