"""Interactive, parameterized SQLite user management for Lab 59."""

from contextlib import contextmanager
import re
import sqlite3
from pathlib import Path

from database_setup import DEFAULT_DB, create_database

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9]{3,20}$")
COLUMNS = "user_id, username, email, full_name, age, city, created_date"
SEARCH_FIELDS = frozenset(("username", "email", "city"))
UPDATE_FIELDS = frozenset(("email", "full_name", "age", "city"))


class UserManager:
    def __init__(self, db_name=DEFAULT_DB):
        self.db_name = str(Path(db_name))
        create_database(self.db_name)

    def get_connection(self):
        """Return a new SQLite connection (caller must close it)."""
        return sqlite3.connect(self.db_name)

    @contextmanager
    def connection(self):
        """Commit or roll back on exit and always close the connection."""
        conn = self.get_connection()
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    @staticmethod
    def validate_email(email):
        return isinstance(email, str) and EMAIL_PATTERN.fullmatch(email) is not None

    @staticmethod
    def validate_username(username):
        return isinstance(username, str) and USERNAME_PATTERN.fullmatch(username) is not None

    @staticmethod
    def validate_age(age):
        return type(age) is int and 13 <= age <= 120

    @staticmethod
    def validate_text(value, label):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} cannot be empty")
        return value.strip().title()

    def add_user(self, username, email, full_name, age, city):
        """Register a validated user; raise ValueError/IntegrityError if invalid."""
        username = username.strip() if isinstance(username, str) else username
        email = email.strip().lower() if isinstance(email, str) else email
        if not self.validate_username(username):
            raise ValueError("Username must be 3-20 ASCII letters or digits")
        if not self.validate_email(email):
            raise ValueError("Please enter a valid email address")
        if not self.validate_age(age):
            raise ValueError("Age must be a whole number between 13 and 120")
        full_name = self.validate_text(full_name, "Full name")
        city = self.validate_text(city, "City")
        with self.connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, email, full_name, age, city) VALUES (?, ?, ?, ?, ?)",
                (username, email, full_name, age, city),
            )
            return cursor.lastrowid

    def get_user_by_id(self, user_id):
        with self.connection() as conn:
            return conn.execute(
                f"SELECT {COLUMNS} FROM users WHERE user_id = ?", (user_id,)
            ).fetchone()

    @staticmethod
    def escape_like(value):
        """Treat %, _ and backslash literally in partial searches."""
        return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

    def find_users(self, field=None, value=None, min_age=None, max_age=None):
        """Find users by a whitelisted text field, age range, or list all."""
        query = f"SELECT {COLUMNS} FROM users"
        params = ()
        if field is not None:
            if field not in SEARCH_FIELDS:
                raise ValueError("Unsupported search field")
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Search text cannot be empty")
            query += f" WHERE {field} LIKE ? ESCAPE '\\' COLLATE NOCASE"
            params = (f"%{self.escape_like(value.strip())}%",)
        elif min_age is not None or max_age is not None:
            if (type(min_age) is not int or type(max_age) is not int
                    or not (0 <= min_age <= max_age <= 120)):
                raise ValueError("Enter a valid minimum and maximum age")
            query += " WHERE age BETWEEN ? AND ?"
            params = (min_age, max_age)
        query += " ORDER BY created_date DESC, user_id DESC"
        with self.connection() as conn:
            return conn.execute(query, params).fetchall()

    def update_user_record(self, user_id, field, value):
        if field not in UPDATE_FIELDS:
            raise ValueError("Unsupported update field")
        if field == "email":
            value = value.strip().lower() if isinstance(value, str) else value
            if not self.validate_email(value):
                raise ValueError("Please enter a valid email address")
        elif field == "age":
            if not self.validate_age(value):
                raise ValueError("Age must be between 13 and 120")
        else:
            value = self.validate_text(value, field.replace("_", " ").title())
        # Column names are constrained by the allowlist above; values are bound.
        with self.connection() as conn:
            cursor = conn.execute(
                f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id)
            )
            return cursor.rowcount > 0

    def delete_user_record(self, user_id):
        with self.connection() as conn:
            cursor = conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            return cursor.rowcount > 0

    @staticmethod
    def ask_number(prompt, minimum, maximum):
        while True:
            try:
                value = int(input(prompt).strip())
                if minimum <= value <= maximum:
                    return value
                print(f"Please enter a number between {minimum} and {maximum}.")
            except ValueError:
                print("Please enter a valid number.")

    def register_user(self):
        print("\n=== USER REGISTRATION ===")
        while True:
            username = input("Enter username (3-20 alphanumeric characters): ").strip()
            if self.validate_username(username):
                break
            print("Username must be 3-20 letters or digits!")
        while True:
            email = input("Enter email address: ").strip().lower()
            if self.validate_email(email):
                break
            print("Please enter a valid email address!")
        while True:
            full_name = input("Enter full name: ").strip()
            if full_name:
                break
            print("Full name cannot be empty!")
        age = self.ask_number("Enter age (13-120): ", 13, 120)
        while True:
            city = input("Enter city: ").strip()
            if city:
                break
            print("City cannot be empty!")
        try:
            user_id = self.add_user(username, email, full_name, age, city)
            print(f"\n✓ User registered successfully! User ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError:
            print("✗ Registration failed: username or email already exists.")
        except (sqlite3.Error, ValueError) as exc:
            print(f"✗ Registration failed: {exc}")
        return None

    @staticmethod
    def display_search_results(results):
        if not results:
            print("\n✗ No users found matching your criteria.")
            return
        print(f"\n✓ Found {len(results)} user(s):")
        print(f"{'ID':<5} {'Username':<20} {'Email':<28} {'Name':<25} {'Age':<5} City")
        print("-" * 100)
        for user_id, username, email, name, age, city, _ in results:
            print(f"{user_id:<5} {username:<20} {email:<28} {name:<25} {age:<5} {city}")

    def search_users(self):
        print("\n=== USER SEARCH ===")
        print("1. Search by username\n2. Search by email\n3. Search by city")
        print("4. Search by age range\n5. View all users")
        choice = self.ask_number("Enter choice (1-5): ", 1, 5)
        try:
            if choice in (1, 2, 3):
                field = {1: "username", 2: "email", 3: "city"}[choice]
                results = self.find_users(field=field, value=input(f"Enter {field}: "))
            elif choice == 4:
                minimum = self.ask_number("Enter minimum age: ", 0, 120)
                maximum = self.ask_number("Enter maximum age: ", minimum, 120)
                results = self.find_users(min_age=minimum, max_age=maximum)
            else:
                results = self.find_users()
            self.display_search_results(results)
        except (ValueError, sqlite3.Error) as exc:
            print(f"✗ Search failed: {exc}")

    def update_user(self):
        print("\n=== UPDATE USER PROFILE ===")
        user_id = self.ask_number("Enter User ID: ", 1, 2_147_483_647)
        user = self.get_user_by_id(user_id)
        if user is None:
            print("✗ User not found!")
            return
        print(f"Current details: {user[1]} | {user[2]} | {user[3]} | {user[4]} | {user[5]}")
        print("1. Email\n2. Full Name\n3. Age\n4. City\n5. Cancel")
        choice = self.ask_number("Choose field (1-5): ", 1, 5)
        if choice == 5:
            print("Update cancelled.")
            return
        field = {1: "email", 2: "full_name", 3: "age", 4: "city"}[choice]
        if field == "age":
            value = self.ask_number("Enter new age (13-120): ", 13, 120)
        else:
            value = input(f"Enter new {field.replace('_', ' ')}: ").strip()
        try:
            if self.update_user_record(user_id, field, value):
                print("✓ User profile updated successfully!")
                self.display_search_results([self.get_user_by_id(user_id)])
            else:
                print("✗ User not found!")
        except (ValueError, sqlite3.IntegrityError, sqlite3.Error) as exc:
            print(f"✗ Update failed: {exc}")

    def delete_user(self):
        print("\n=== DELETE USER ACCOUNT ===")
        print("⚠ WARNING: This action cannot be undone!")
        user_id = self.ask_number("Enter User ID to delete: ", 1, 2_147_483_647)
        user = self.get_user_by_id(user_id)
        if user is None:
            print("✗ User not found!")
            return
        print(f"User to delete: ID={user[0]}, username={user[1]}, email={user[2]}")
        confirm = input(f"Are you sure you want to delete '{user[1]}'? (yes/no): ").strip().lower()
        if confirm not in ("yes", "y"):
            print("Deletion cancelled.")
            return
        if input("Type DELETE to confirm permanent deletion: ").strip() != "DELETE":
            print("Deletion cancelled.")
            return
        try:
            if self.delete_user_record(user_id):
                print(f"✓ User '{user[1]}' has been permanently deleted!")
            else:
                print("✗ User not found!")
        except sqlite3.Error as exc:
            print(f"✗ Deletion failed: {exc}")

    def main_menu(self):
        actions = {1: self.register_user, 2: self.search_users,
                   3: self.update_user, 4: self.delete_user}
        try:
            while True:
                print("\n" + "=" * 50)
                print("USER MANAGEMENT SYSTEM")
                print("=" * 50)
                print("1. Register new user\n2. Search users\n3. Update user profile")
                print("4. Delete user account\n5. Exit")
                choice = self.ask_number("Enter your choice (1-5): ", 1, 5)
                if choice == 5:
                    print("Thank you for using User Management System!")
                    break
                actions[choice]()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting program...")


if __name__ == "__main__":
    UserManager().main_menu()
