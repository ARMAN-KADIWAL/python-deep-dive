#!/usr/bin/env python3
"""Query student records using SELECT, filtering, search, and aggregates."""
import argparse
import sqlite3
from tabulate import tabulate
from student_management import DEFAULT_DB, create_database, create_students_table


def connect_to_database(db_path=DEFAULT_DB):
    connection = create_database(db_path)
    if connection:
        connection.row_factory = sqlite3.Row
        if not create_students_table(connection):
            connection.close()
            return None
    return connection


def display_results(results, headers):
    if not results:
        print("No records found.")
        return
    print(tabulate([list(row) for row in results], headers=headers, tablefmt="grid"))


def query_all_students(connection):
    try:
        rows = connection.execute("""SELECT student_id, first_name, last_name, email, age, major, gpa,
        enrollment_date FROM students ORDER BY last_name, first_name""").fetchall()
        print("\n=== All Students ===")
        display_results(rows, ["ID", "First Name", "Last Name", "Email", "Age", "Major", "GPA", "Enrollment Date"])
        return rows
    except sqlite3.Error as error:
        print(f"✗ Error querying all students: {error}")
        return []


def query_students_by_major(connection, major):
    try:
        rows = connection.execute("""SELECT first_name, last_name, email, age, gpa FROM students
        WHERE major=? ORDER BY gpa DESC""", (major,)).fetchall()
        print(f"\n=== Students in {major} ===")
        display_results(rows, ["First Name", "Last Name", "Email", "Age", "GPA"])
        return rows
    except sqlite3.Error as error:
        print(f"✗ Error querying students by major: {error}")
        return []


def query_high_performing_students(connection, min_gpa=3.5):
    try:
        rows = connection.execute("""SELECT first_name, last_name, major, gpa FROM students
        WHERE gpa>=? ORDER BY gpa DESC, last_name""", (min_gpa,)).fetchall()
        print(f"\n=== High Performing Students (GPA >= {min_gpa}) ===")
        display_results(rows, ["First Name", "Last Name", "Major", "GPA"])
        return rows
    except sqlite3.Error as error:
        print(f"✗ Error querying high performing students: {error}")
        return []


def query_student_statistics(connection):
    try:
        by_major = connection.execute("""SELECT major, COUNT(*) AS student_count, AVG(gpa) AS avg_gpa
        FROM students GROUP BY major ORDER BY student_count DESC""").fetchall()
        print("\n=== Statistics by Major ===")
        display_results(by_major, ["Major", "Student Count", "Average GPA"])
        overall = connection.execute("""SELECT COUNT(*) AS total_students, AVG(age) AS avg_age,
        AVG(gpa) AS avg_gpa, MIN(gpa) AS min_gpa, MAX(gpa) AS max_gpa FROM students""").fetchone()
        print("\n=== Overall Statistics ===")
        print(f"Total Students: {overall['total_students']}")
        if overall["total_students"]:
            print(f"Average Age: {overall['avg_age']:.1f}")
            print(f"Average GPA: {overall['avg_gpa']:.2f}")
            print(f"Lowest GPA: {overall['min_gpa']:.2f}")
            print(f"Highest GPA: {overall['max_gpa']:.2f}")
        else:
            print("No student data available for averages.")
        return {"by_major": by_major, "overall": overall}
    except sqlite3.Error as error:
        print(f"✗ Error generating statistics: {error}")
        return None


def search_students(connection, search_term):
    try:
        pattern = f"%{search_term}%"
        rows = connection.execute("""SELECT student_id, first_name, last_name, email, major, gpa
        FROM students WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
        ORDER BY last_name, first_name""", (pattern, pattern, pattern)).fetchall()
        print(f"\n=== Search Results for '{search_term}' ===")
        display_results(rows, ["ID", "First Name", "Last Name", "Email", "Major", "GPA"])
        return rows
    except sqlite3.Error as error:
        print(f"✗ Error searching students: {error}")
        return []


def demonstrate_queries(db_path=DEFAULT_DB, search_term=None):
    connection = connect_to_database(db_path)
    if connection is None:
        return
    try:
        print("=== Database Query Demonstration ===")
        query_all_students(connection)
        query_students_by_major(connection, "Computer Science")
        query_high_performing_students(connection, 3.8)
        query_student_statistics(connection)
        if search_term is None:
            search_term = input("\nEnter search term (name or email): ").strip()
        if search_term:
            search_students(connection, search_term)
    finally:
        connection.close()
        print("\n✓ All query operations completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--search")
    args = parser.parse_args()
    demonstrate_queries(args.db, args.search)
