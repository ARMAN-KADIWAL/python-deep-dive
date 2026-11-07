"""Lab 59: illustrate SQL injection safely, with a throwaway in-memory DB."""

import sqlite3
from contextlib import closing
from user_management import UserManager


class SecurityDemo:
    def __init__(self, db_name=None):
        self.manager = UserManager(db_name) if db_name is not None else UserManager()

    @staticmethod
    def compare_queries(username):
        """Return unsafe/safe match counts against *disposable* demo-only data."""
        # Never execute user-controlled unsafe SQL on the real users database.
        with closing(sqlite3.connect(":memory:")) as conn:
            conn.execute("CREATE TABLE users (username TEXT NOT NULL)")
            conn.executemany("INSERT INTO users VALUES (?)", [("admin",), ("alice123",)])
            unsafe_sql = f"SELECT * FROM users WHERE username = '{username}'"
            try:
                unsafe_count = len(conn.execute(unsafe_sql).fetchall())
            except sqlite3.Error:
                unsafe_count = None
            safe_count = len(conn.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchall())
        return unsafe_sql, unsafe_count, safe_count

    def safe_search_example(self, username):
        """Actual user database is accessed *only* with a parameterized query."""
        with self.manager.connection() as conn:
            rows = conn.execute(
                "SELECT username, email FROM users WHERE username = ?", (username,)
            ).fetchall()
        print(f"Safe query: SELECT ... WHERE username = ? | parameter={username!r}")
        print(f"Matched {len(rows)} user(s): {rows}")
        return rows

    def demonstrate_sql_injection_attempt(self):
        print("\n" + "=" * 60)
        print("SQL INJECTION PROTECTION DEMONSTRATION")
        print("=" * 60)
        malicious = "' OR 1=1 --"
        unsafe_sql, unsafe_count, safe_count = self.compare_queries(malicious)
        print(f"Malicious input: {malicious!r}")
        print(f"Unsafe SQL (in-memory demo only): {unsafe_sql}")
        print(f"Unsafe results: {unsafe_count} | Parameterized results: {safe_count}")
        self.safe_search_example(malicious)
        print("Note: sqlite3.execute() rejects multiple SQL statements, but unsafe")
        print("string interpolation is still vulnerable to boolean/WHERE injection.")

    @staticmethod
    def show_parameterized_query_examples():
        print("\nPARAMETERIZED QUERY EXAMPLES")
        examples = [
            ("SELECT * FROM users WHERE user_id = ?", "(user_id,)"),
            ("INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
             "(username, email, age)"),
            ("SELECT * FROM users WHERE city LIKE ?", '(f"%{city}%",)'),
            ("SELECT * FROM users WHERE age BETWEEN ? AND ?", "(min_age, max_age)"),
            ("UPDATE users SET email = ? WHERE user_id = ?", "(email, user_id)"),
            ("DELETE FROM users WHERE user_id = ?", "(user_id,)"),
        ]
        for i, (query, params) in enumerate(examples, 1):
            print(f"{i}. {query}\n   Parameters: {params}")


if __name__ == "__main__":
    demo = SecurityDemo()
    demo.demonstrate_sql_injection_attempt()
    demo.show_parameterized_query_examples()
