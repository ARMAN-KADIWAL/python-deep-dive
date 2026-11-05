#!/usr/bin/env python3
"""Delete student records safely, with JSON backups and confirmation."""
import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from student_management import DEFAULT_DB, create_database, create_students_table

ALLOWED_CRITERIA_FIELDS = {"student_id", "first_name", "last_name", "email", "age", "major", "gpa", "enrollment_date"}


def connect_to_database(db_path=DEFAULT_DB):
    connection = create_database(db_path)
    if connection:
        connection.row_factory = sqlite3.Row
        if not create_students_table(connection):
            connection.close()
            return None
    return connection


def backup_student_record(connection, student_id, backup_dir="backups"):
    try:
        row = connection.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
        if row is None:
            print(f"✗ No student found with ID: {student_id}")
            return None
        data = dict(row)
        data["backup_timestamp"] = datetime.now().isoformat()
        folder = Path(backup_dir)
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = folder / f"student_backup_{student_id}_{stamp}.json"
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"✓ Student record backed up to: {path}")
        return str(path)
    except (sqlite3.Error, OSError, TypeError) as error:
        print(f"✗ Error creating backup: {error}")
        return None


def display_student_details(connection, student_id):
    try:
        row = connection.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
        if row is None:
            print(f"✗ No student found with ID: {student_id}")
            return False
        print("\n" + "=" * 50 + "\nSTUDENT RECORD TO BE DELETED\n" + "=" * 50)
        for key in ("student_id", "first_name", "last_name", "email", "age", "major", "gpa", "enrollment_date"):
            print(f"{key.replace('_', ' ').title()}: {row[key]}")
        print("=" * 50)
        return True
    except sqlite3.Error as error:
        print(f"✗ Error displaying student: {error}")
        return False


def delete_student_by_id(connection, student_id, create_backup=True, confirm=None, backup_dir="backups"):
    if not display_student_details(connection, student_id):
        return False
    backup_file = backup_student_record(connection, student_id, backup_dir) if create_backup else None
    if create_backup and not backup_file:
        print("✗ Failed to create backup. Deletion cancelled for safety.")
        return False
    if confirm is None:
        confirm = input(f"\nAre you sure you want to delete student ID {student_id}? (type 'DELETE' to confirm): ")
    if confirm != "DELETE":
        print("Deletion cancelled")
        return False
    try:
        cursor = connection.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        connection.commit()
        if cursor.rowcount:
            print(f"✓ Student ID {student_id} deleted successfully")
            if backup_file:
                print(f"✓ Backup saved as: {backup_file}")
            return True
        print(f"✗ No student found with ID: {student_id}")
        return False
    except sqlite3.Error as error:
        connection.rollback()
        print(f"✗ Error deleting student: {error}")
        return False


def delete_students_by_criteria(connection, criteria_field, criteria_value, confirm=None, backup_dir="backups"):
    if criteria_field not in ALLOWED_CRITERIA_FIELDS:
        print(f"✗ Unsupported criteria field: {criteria_field}")
        return False
    try:
        rows = connection.execute(
            f"SELECT student_id, first_name, last_name, {criteria_field} FROM students WHERE {criteria_field}=?",
            (criteria_value,)
        ).fetchall()
        if not rows:
            print(f"✗ No students found with {criteria_field} = '{criteria_value}'")
            return False
        print(f"\nStudents with {criteria_field} = '{criteria_value}' that will be deleted:")
        backups = []
        for row in rows:
            print(f"  ID {row['student_id']}: {row['first_name']} {row['last_name']} ({row[criteria_field]})")
            record = dict(connection.execute("SELECT * FROM students WHERE student_id=?", (row["student_id"],)).fetchone())
            record["backup_timestamp"] = datetime.now().isoformat()
            backups.append(record)
        folder = Path(backup_dir)
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = folder / f"students_backup_{stamp}.json"
        path.write_text(json.dumps(backups, indent=2), encoding="utf-8")
        print(f"✓ Backup saved as: {path}")
        if confirm is None:
            confirm = input(f"\nType 'DELETE' to delete these {len(rows)} records: ")
        if confirm != "DELETE":
            print("Deletion cancelled")
            return False
        cursor = connection.execute(f"DELETE FROM students WHERE {criteria_field}=?", (criteria_value,))
        connection.commit()
        print(f"✓ {cursor.rowcount} student records deleted")
        return True
    except (sqlite3.Error, OSError, TypeError) as error:
        connection.rollback()
        print(f"✗ Error deleting students: {error}")
        return False


def demonstrate_deletion(db_path=DEFAULT_DB, student_id=None, confirm="n"):
    connection = connect_to_database(db_path)
    if connection is None:
        return
    try:
        print("=== Database Deletion Demonstration ===")
        if student_id is not None:
            delete_student_by_id(connection, student_id, True, confirm)
        else:
            print("Pass --student-id and --confirm-delete to run the deletion demonstration.")
    finally:
        connection.close()
        print("\n✓ Database connection closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--student-id", type=int)
    parser.add_argument("--confirm-delete", action="store_true")
    args = parser.parse_args()
    demonstrate_deletion(args.db, args.student_id, "DELETE" if args.confirm_delete else "n")
