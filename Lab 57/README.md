# Lab 57: Interacting with Databases - Using SQLite

## Objectives
- Create SQLite databases and tables with Python's built-in \`sqlite3\`.
- Insert single and multiple records using parameterized SQL.
- Query, filter, sort, search, and aggregate records with \`SELECT\`.
- Update individual and grouped records with \`UPDATE\`.
- Delete records safely with confirmation and JSON backups.
- Handle database errors, transactions, and connection cleanup.

## Requirements
Python 3.8+, built-in SQLite support, and \`tabulate\`.

    python3 -m pip install -r requirements.txt

On Ubuntu systems that block global pip installs:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Files
- \`student_management.py\`: create the database and students table.
- \`data_insertion.py\`: insert single and batch records; optional interactive insert.
- \`data_queries.py\`: list, filter, search, and calculate student statistics.
- \`data_updates.py\`: update GPA, major, contact details, and bulk GPA values.
- \`data_deletion.py\`: preview, back up, confirm, and delete records.
- \`requirements.txt\`: formatted table dependency.
- \`test_lab57.py\`: automated tests using temporary databases.

## Run the lab
Run commands from this folder:

    python3 student_management.py
    python3 data_insertion.py
    python3 data_queries.py --search John
    python3 data_updates.py

Optional interactive insertion and update menu:

    python3 data_insertion.py --interactive
    python3 data_updates.py --interactive

Bulk GPA adjustment is cancelled by default. Use \`--confirm-bulk\` to apply it.

Delete a student only after reviewing the record. This example backs up student ID 1 before deletion:

    python3 data_deletion.py --student-id 1 --confirm-delete

## Verify database

    ls -la *.db
    python3 -c "import sqlite3; c=sqlite3.connect('student_records.db'); print(c.execute('SELECT COUNT(*) FROM students').fetchone()[0]); c.close()"

## Run automated tests

    python3 -m unittest -v

## Implementation notes
- SQL values are passed as parameters (\`?\`), not interpolated into SQL.
- Bulk deletion allows only known column names and parameterizes the filter value.
- Single and bulk deletion create JSON backups before requesting confirmation.
- The supplied lab source stops partway through \`delete_students_by_criteria()\`. That unfinished ending is completed here according to the source's stated objectives for previews, backups, confirmation, and safe deletion.
- Database files and generated backup JSON files are runtime outputs, not committed artifacts.
