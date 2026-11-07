"""Set up the SQLite database for Lab 59.

Running this repeatedly preserves existing records. Use --reset only when you
explicitly want to erase the database and start again.
"""

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3

DEFAULT_DB = Path(__file__).resolve().parent / "user_management.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    age INTEGER CHECK (age BETWEEN 13 AND 120),
    city TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def create_database(db_name=DEFAULT_DB, reset=False):
    """Create the user table, optionally resetting the database explicitly."""
    db_path = Path(db_name)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if reset and db_path.exists():
        db_path.unlink()
    with closing(sqlite3.connect(db_path)) as conn:
        with conn:
            conn.execute(SCHEMA)
    return db_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize Lab 59 SQLite database")
    parser.add_argument("--reset", action="store_true", help="Erase all existing users")
    args = parser.parse_args()
    path = create_database(reset=args.reset)
    print(f"Database and users table ready: {path}")
