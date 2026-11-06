"""Shared SQLite helpers for Lab 58."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("company_database.db")


def connect_database(db_path=DB_PATH):
    """Open the company database with foreign-key checks enabled."""
    if db_path is None:
        db_path = DB_PATH
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def execute_query(query, description, parameters=(), db_path=DB_PATH):
    """Run a query, display a formatted table, and return rows."""
    connection = None
    try:
        connection = connect_database(db_path)
        cursor = connection.execute(query, parameters)
        rows = cursor.fetchall()
        headers = [column[0] for column in (cursor.description or [])]
        print("\n" + "=" * 70)
        print(f"QUERY: {description}")
        print("=" * 70)
        print(f"SQL: {query.strip()}")
        print("-" * 70)
        if not headers:
            print("Query completed successfully.")
        elif not rows:
            print("No results found.")
        else:
            widths = [
                max(len(str(header)), *(len(str(row[index])) if row[index] is not None else 4 for row in rows))
                for index, header in enumerate(headers)
            ]
            print(" | ".join(str(header).ljust(widths[index]) for index, header in enumerate(headers)))
            print("-+-".join("-" * width for width in widths))
            for row in rows:
                print(" | ".join((str(value) if value is not None else "NULL").ljust(widths[index])
                                 for index, value in enumerate(row)))
        print(f"\nTotal records: {len(rows)}")
        return rows
    except sqlite3.Error as error:
        print(f"Error executing query: {error}")
        return []
    finally:
        if connection is not None:
            connection.close()
