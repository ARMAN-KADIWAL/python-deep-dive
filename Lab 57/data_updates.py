#!/usr/bin/env python3
"""Update student records and demonstrate UPDATE statements."""
import argparse
import sqlite3
from student_management import DEFAULT_DB, create_database, create_students_table


def connect_to_database(db_path=DEFAULT_DB):
    connection = create_database(db_path)
    if connection:
        connection.row_factory = sqlite3.Row
        if not create_students_table(connection):
            connection.close()
            return None
    return connection


def display_student(connection, student_id):
    try:
        row = connection.execute("""SELECT student_id, first_name, last_name, email, age, major, gpa
        FROM students WHERE student_id=?""", (student_id,)).fetchone()
        if row:
            for label, field in [("Student ID", "student_id"), ("Name", None), ("Email", "email"),
                                 ("Age", "age"), ("Major", "major"), ("GPA", "gpa")]:
                value = f"{row['first_name']} {row['last_name']}" if field is None else row[field]
                print(f"{label}: {value}")
            return True
        print(f"✗ No student found with ID: {student_id}")
        return False
    except sqlite3.Error as error:
        print(f"✗ Error displaying student: {error}")
        return False


def update_student_gpa(connection, student_id, new_gpa):
    if not 0 <= new_gpa <= 4:
        print("✗ GPA must be between 0 and 4")
        return False
    try:
        if not display_student(connection, student_id):
            return False
        cur = connection.execute("UPDATE students SET gpa=? WHERE student_id=?", (new_gpa, student_id))
        connection.commit()
        if cur.rowcount:
            print(f"✓ GPA updated to {new_gpa} for student ID {student_id}")
            display_student(connection, student_id)
            return True
        return False
    except sqlite3.Error as error:
        connection.rollback()
        print(f"✗ Error updating GPA: {error}")
        return False


def update_student_major(connection, student_id, new_major):
    if not new_major.strip():
        print("✗ Major cannot be empty")
        return False
    try:
        if not display_student(connection, student_id):
            return False
        cur = connection.execute("UPDATE students SET major=? WHERE student_id=?", (new_major.strip(), student_id))
        connection.commit()
        if cur.rowcount:
            print(f"✓ Major updated to '{new_major}' for student ID {student_id}")
            display_student(connection, student_id)
            return True
        return False
    except sqlite3.Error as error:
        connection.rollback()
        print(f"✗ Error updating major: {error}")
        return False


def update_student_contact(connection, student_id, new_email=None, new_age=None):
    fields, values = [], []
    if new_email is not None:
        if not new_email.strip():
            print("✗ Email cannot be empty")
            return False
        fields.append("email=?")
        values.append(new_email.strip())
    if new_age is not None:
        if new_age < 0:
            print("✗ Age cannot be negative")
            return False
        fields.append("age=?")
        values.append(new_age)
    if not fields:
        print("✗ No fields to update")
        return False
    try:
        if not display_student(connection, student_id):
            return False
        values.append(student_id)
        cur = connection.execute(f"UPDATE students SET {', '.join(fields)} WHERE student_id=?", values)
        connection.commit()
        if cur.rowcount:
            print(f"✓ Contact information updated for student ID {student_id}")
            display_student(connection, student_id)
            return True
        return False
    except sqlite3.IntegrityError as error:
        connection.rollback()
        print(f"✗ Data integrity error (email might already exist): {error}")
        return False
    except sqlite3.Error as error:
        connection.rollback()
        print(f"✗ Error updating contact information: {error}")
        return False


def bulk_update_gpa_by_major(connection, major, gpa_adjustment, confirm=None):
    try:
        rows = connection.execute("""SELECT student_id, first_name, last_name, gpa, gpa+? AS new_gpa
        FROM students WHERE major=?""", (gpa_adjustment, major)).fetchall()
        if not rows:
            print(f"✗ No students found in major: {major}")
            return False
        if any(row["new_gpa"] < 0 or row["new_gpa"] > 4 for row in rows):
            print("✗ Adjustment would move one or more GPAs outside 0 to 4")
            return False
        print(f"\nStudents in {major} who will be affected:")
        for row in rows:
            print(f"  {row['first_name']} {row['last_name']}: {row['gpa']} → {row['new_gpa']:.2f}")
        if confirm is None:
            confirm = input(f"\nApply {gpa_adjustment:+.2f} GPA adjustment to {len(rows)} students? (y/n): ")
        if confirm.lower() != "y":
            print("Update cancelled")
            return False
        cur = connection.execute("UPDATE students SET gpa=gpa+? WHERE major=?", (gpa_adjustment, major))
        connection.commit()
        print(f"✓ GPA adjustment applied to {cur.rowcount} students in {major}")
        return True
    except sqlite3.Error as error:
        connection.rollback()
        print(f"✗ Error in bulk GPA update: {error}")
        return False


def interactive_student_update(connection):
    try:
        students = connection.execute("SELECT student_id, first_name, last_name, major FROM students ORDER BY student_id").fetchall()
        print("\nAvailable students:")
        for row in students:
            print(f"  ID {row['student_id']}: {row['first_name']} {row['last_name']} ({row['major']})")
        sid = int(input("\nEnter student ID to update: "))
        print("\n1. GPA\n2. Major\n3. Email\n4. Age\n5. Multiple fields")
        choice = input("Enter choice (1-5): ").strip()
        if choice == "1":
            return update_student_gpa(connection, sid, float(input("Enter new GPA: ")))
        if choice == "2":
            return update_student_major(connection, sid, input("Enter new major: ").strip())
        if choice == "3":
            return update_student_contact(connection, sid, new_email=input("Enter new email: ").strip())
        if choice == "4":
            return update_student_contact(connection, sid, new_age=int(input("Enter new age: ")))
        if choice == "5":
            email = input("Enter new email (or Enter to skip): ").strip() or None
            age_text = input("Enter new age (or Enter to skip): ").strip()
            return update_student_contact(connection, sid, email, int(age_text) if age_text else None)
        print("Invalid choice")
    except ValueError as error:
        print(f"✗ Invalid input: {error}")
    return False


def demonstrate_updates(db_path=DEFAULT_DB, interactive=False, bulk_confirm="n"):
    connection = connect_to_database(db_path)
    if connection is None:
        return
    try:
        print("=== Database Update Demonstration ===")
        update_student_gpa(connection, 1, 3.85)
        update_student_major(connection, 2, "Data Science")
        update_student_contact(connection, 3, new_email="new.email@example.com", new_age=21)
        bulk_update_gpa_by_major(connection, "Computer Science", 0.1, confirm=bulk_confirm)
        if interactive:
            interactive_student_update(connection)
    finally:
        connection.close()
        print("\n✓ All update operations completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--confirm-bulk", action="store_true")
    args = parser.parse_args()
    demonstrate_updates(args.db, args.interactive, "y" if args.confirm_bulk else "n")
