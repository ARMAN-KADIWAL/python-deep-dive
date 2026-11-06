# Lab 58: Querying and Filtering Data in SQLite

## Objectives
- Filter records with WHERE, AND, OR, IN, BETWEEN, LIKE, NOT, and CASE.
- Sort and limit rows with ORDER BY, LIMIT, and OFFSET.
- Combine tables with INNER JOIN, LEFT JOIN, and self joins.
- Group records with COUNT, SUM, AVG, MIN, MAX, and HAVING.

## Requirements
Python 3.8+ and built-in sqlite3. No third-party packages are required.

## Files
- setup_database.py: create and seed employees, departments, and projects.
- db_utils.py: shared SQLite connection and result formatting.
- filtering_queries.py: WHERE clause examples.
- advanced_filtering.py: NOT, NOT LIKE, compound conditions, and CASE.
- sorting_limiting.py: ORDER BY, LIMIT, and OFFSET.
- join_operations.py: INNER JOIN examples.
- advanced_joins.py: LEFT JOIN, self JOIN, and aggregate JOIN.
- grouping_aggregation.py: GROUP BY and aggregate functions.
- advanced_aggregation.py: HAVING clause examples.
- test_lab58.py: automated tests.

## Run the lab
From inside Lab 58:

    python3 setup_database.py
    python3 filtering_queries.py
    python3 advanced_filtering.py
    python3 sorting_limiting.py
    python3 join_operations.py
    python3 advanced_joins.py
    python3 grouping_aggregation.py
    python3 advanced_aggregation.py

## Optional SQLite CLI inspection

    sqlite3 company_database.db

Inside the SQLite prompt:

    .tables
    .schema employees
    .schema departments
    .schema projects
    .quit

The SQLite shell is optional. The Python scripts use the built-in sqlite3 module and do not require the sqlite3 command.

## Automated tests

    python3 -m unittest -v

## Notes
- The setup uses stable IDs and INSERT OR REPLACE, so it can be safely repeated without duplicating sample rows.
- The uploaded source ends immediately after the start of connect_database() in advanced_aggregation.py. That unfinished section is completed with grouped employee, salary, project, and status totals filtered by HAVING, consistent with the lab's stated objectives.
- The joined department summary uses distinct project budgets to avoid multiplying the same project budget for each employee in the department.
