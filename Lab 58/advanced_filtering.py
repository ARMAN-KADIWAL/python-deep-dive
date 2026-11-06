#!/usr/bin/env python3
"""Demonstrate NOT, NOT LIKE, compound conditions, and CASE."""
from db_utils import execute_query


def demonstrate_advanced_filtering(db_path=None):
    queries = [
        ("SELECT first_name, last_name, department_id FROM employees WHERE department_id NOT IN (2, 4)", "Employees NOT in Engineering or Sales departments"),
        ("SELECT first_name, last_name, email FROM employees WHERE email NOT LIKE '%.com'", "Employees with non-.com email addresses"),
        ("SELECT first_name, last_name, salary, department_id FROM employees WHERE (salary > 80000 AND department_id = 2) OR (salary > 70000 AND department_id = 4)", "High-salary employees in Engineering OR Sales"),
        ("""SELECT first_name, last_name, salary,
            CASE WHEN salary > 85000 THEN 'High'
                 WHEN salary > 70000 THEN 'Medium'
                 ELSE 'Low' END AS salary_category
            FROM employees""", "Employees with salary categories"),
    ]
    return [execute_query(query, description, db_path=db_path) for query, description in queries]


if __name__ == "__main__":
    demonstrate_advanced_filtering()
