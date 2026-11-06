#!/usr/bin/env python3
"""Demonstrate WHERE filtering conditions in SQLite."""
from db_utils import execute_query


def demonstrate_filtering(db_path=None):
    queries = [
        ("SELECT first_name, last_name, salary FROM employees WHERE salary > 75000", "Employees with salary greater than $75,000"),
        ("SELECT first_name, last_name, department_id FROM employees WHERE department_id = 2", "Employees in Engineering department (ID: 2)"),
        ("SELECT first_name, last_name, hire_date FROM employees WHERE hire_date BETWEEN '2020-01-01' AND '2021-12-31'", "Employees hired between 2020 and 2021"),
        ("SELECT first_name, last_name, email FROM employees WHERE email LIKE '%johnson%'", "Employees with 'johnson' in their email"),
        ("SELECT first_name, last_name, department_id FROM employees WHERE department_id IN (1, 3, 5)", "Employees in HR, Marketing, or Finance departments"),
        ("SELECT first_name, last_name, salary, department_id FROM employees WHERE salary > 70000 AND department_id = 2", "Engineering employees with salary > $70,000"),
        ("SELECT first_name, last_name, salary FROM employees WHERE salary > 90000 OR department_id = 1", "Employees with salary > $90,000 OR in HR department"),
        ("SELECT project_name, budget, status FROM projects WHERE status = 'Active'", "Active projects"),
    ]
    return [execute_query(query, description, db_path=db_path) for query, description in queries]


if __name__ == "__main__":
    demonstrate_filtering()
