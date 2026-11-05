#!/usr/bin/env python3
"""Insert one or many student records into SQLite."""
import argparse
import sqlite3
from student_management import DEFAULT_DB, create_database, create_students_table

INSERT_SQL = """INSERT INTO students
(first_name, last_name, email, age, major, gpa) VALUES (?, ?, ?, ?, ?, ?)"""


def connect_to_database(db_path=DEFAULT_DB):
    connection = create_database(db_path)
    if connection and not create_students_table(connection):
        connection.close()
        return None
    return connection


def insert_single_student(connection, student_data):
    try:
        cursor = connection.execute(INSERT_SQL, student_data)
        connection.commit()
        print(f"✓ Student {student_data[0]} {student_data[1]} added successfully")
        print(f"  Student ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.IntegrityError as error:
        connection.rollback()
        print(f"✗ Data integrity error: {error}")
        return None
    except sqlite3.Error as error:
        connection.rollback()
        print(f"✗ Error inserting student: {error}")
        return None


def insert_multiple_students(connection, students_list):
    try:
        cursor = connection.executemany(INSERT_SQL, students_list)
        connection.commit()
        print(f"✓ {len(students_list)} students added successfully")
        return cursor.rowcount
    except sqlite3.Error as error:
        connection.rollback()
        print(f"✗ Error inserting multiple students: {error}")
        return 0


def add_interactive_student(connection):
    try:
        print("Enter student information:")
        first = input("First Name: ").strip()
        last = input("Last Name: ").strip()
        email = input("Email: ").strip()
        age = int(input("Age: "))
        major = input("Major: ").strip()
        gpa = float(input("GPA: "))
        if not first or not last or not email or not 0 <= gpa <= 4:
            raise ValueError("Names/email are required and GPA must be between 0 and 4")
        return insert_single_student(connection, (first, last, email, age, major, gpa))
    except ValueError as error:
        print(f"✗ Invalid input format: {error}")
        return None


def demonstrate_data_insertion(db_path=DEFAULT_DB, interactive=False):
    connection = connect_to_database(db_path)
    if connection is None:
        return
    single = ("John", "Doe", "john.doe@email.com", 20, "Computer Science", 3.75)
    batch = [
        ("Jane", "Smith", "jane.smith@email.com", 19, "Mathematics", 3.90),
        ("Mike", "Johnson", "mike.johnson@email.com", 21, "Physics", 3.60),
        ("Sarah", "Williams", "sarah.williams@email.com", 20, "Chemistry", 3.85),
        ("David", "Brown", "david.brown@email.com", 22, "Biology", 3.70),
        ("Emily", "Davis", "emily.davis@email.com", 19, "Engineering", 3.95),
    ]
    try:
        print("\n=== Data Insertion Demonstration ===")
        if connection.execute("SELECT 1 FROM students WHERE email=?", (single[2],)).fetchone():
            print("John Doe already exists; skipping duplicate sample record")
        else:
            print("\n1. Inserting single student:")
            insert_single_student(connection, single)
        new_batch = [row for row in batch if not connection.execute(
            "SELECT 1 FROM students WHERE email=?", (row[2],)).fetchone()]
        print("\n2. Inserting multiple students:")
        if new_batch:
            insert_multiple_students(connection, new_batch)
        else:
            print("Sample batch already exists; skipping duplicate records")
        if interactive:
            print("\n3. Interactive student addition:")
            add_interactive_student(connection)
    finally:
        connection.close()
        print("\n✓ All insertion operations completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()
    demonstrate_data_insertion(args.db, args.interactive)
