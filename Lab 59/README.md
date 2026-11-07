# Lab 59: Integrating Databases with User Input

A complete **Python 3 + SQLite3** command-line user management system for the Al Nafi Lab 59 assignment. The lab uses only the Python standard library; no packages need to be installed.

## Learning objectives and task checklist

| Task | Implementation |
| --- | --- |
| 1. User registration with SQLite | `database_setup.py`, `user_management.py` |
| 2. Search by username, email, city, age or list all | `UserManager.search_users()` |
| 3. Update user and delete with two confirmations | `UserManager.update_user()` / `delete_user()` |
| 4. Prevent SQL injection with parameterized queries | `security_demo.py` |
| 5. Test the complete application and generate a report | `test_system.py`, `database_report.py` |

## Run this lab

In a terminal, navigate to the `Lab 59` folder and run:

```bash
python3 database_setup.py
python3 user_management.py
```

The interactive app presents five menu choices:

```text
USER MANAGEMENT SYSTEM
1. Register new user
2. Search users
3. Update user profile
4. Delete user account
5. Exit
```

Username must contain **3–20 ASCII letters or numbers**; email must be valid; full name and city cannot be blank; age must be **13–120**. SQLite enforces unique usernames/emails. Database values are always bound as `?` parameters, including in search, update and delete operations. Search and update column names are selected from explicit allowlists.

### Security demonstration

```bash
python3 security_demo.py
```

The demo shows how an unsafe username lookup can return unintended rows with `' OR 1=1 --`, whereas the parameterized lookup treats the same input as data. **Unsafe SQL executes only inside a temporary in-memory demo database** and never touches your saved users. (Python's `sqlite3.execute()` rejects multiple statements; this does not make interpolated SQL safe.)

### Automated tests

```bash
python3 test_system.py
# or
python3 -m unittest -v test_system
```

The `unittest` suite covers table setup, registration, validation, duplicate accounts, all search types, age ranges, SQL injection, all update fields, deletion confirmation/cancel, reporting, and a complete simulated menu session. Tests use disposable temporary databases and **do not modify your real `user_management.db`**.

### Database report (Task 5.4)

```bash
python3 database_report.py
python3 database_report.py --output report_output.txt
```

The live report shows total users, age range and average, user counts per city and five latest registrations. It handles an empty database. The provided assignment text ends just after the report-script instruction, so this implementation supplies a reasonable final report format.

### Reset database (destructive)

```bash
python3 database_setup.py --reset
```

Normal setup **preserves existing data**. Only `--reset` removes the existing SQLite database; use it only when intentional.

## Suggested manual test scenarios

1. Register three new users, then try an invalid email/age and duplicate username/email.
2. Search using a partial username, email, city, and an age range; view all users.
3. Update email, full name, age, and city; try a duplicate email.
4. Delete an account after confirming with `yes` and `DELETE`, then verify that it is gone; try cancellation and a missing user ID.
5. Run `security_demo.py`, `test_system.py`, and `database_report.py`.

## Files

```text
Lab 59/
├── .gitignore           # Keeps personal SQLite data and generated files out of Git
├── README.md            # Instructions and task checklist
├── database_setup.py    # Database schema and optional explicit reset
├── user_management.py   # Interactive CRUD, searches, and validation
├── security_demo.py     # Safe SQL injection demonstration
├── test_system.py       # Automated test suite (stdlib unittest)
└── database_report.py   # Final live database statistics report
```

**Privacy:** Never push your local `user_management.db` with real registration data. It is ignored by Git in this folder.
