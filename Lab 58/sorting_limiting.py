#!/usr/bin/env python3
"""Demonstrate ORDER BY and LIMIT clauses."""
from db_utils import execute_query


def demonstrate_sorting_limiting(db_path=None):
    queries = [
        ("SELECT first_name, last_name, salary FROM employees ORDER BY salary ASC", "Employees sorted by salary (ascending)"),
        ("SELECT first_name, last_name, salary FROM employees ORDER BY salary DESC", "Employees sorted by salary (descending)"),
        ("SELECT first_name, last_name, department_id, salary FROM employees ORDER BY department_id ASC, salary DESC", "Employees sorted by department, then salary (desc)"),
        ("SELECT first_name, last_name, hire_date FROM employees ORDER BY hire_date DESC", "Employees sorted by hire date (newest first)"),
        ("SELECT first_name, last_name, salary FROM employees ORDER BY salary DESC LIMIT 5", "Top 5 highest paid employees"),
        ("SELECT first_name, last_name, salary FROM employees ORDER BY salary DESC LIMIT 5 OFFSET 2", "Employees ranked 3-7 by salary"),
        ("SELECT project_name, budget, status FROM projects ORDER BY budget DESC", "Projects sorted by budget (highest first)"),
        ("SELECT project_name, budget, status FROM projects WHERE status = 'Active' ORDER BY budget DESC LIMIT 3", "Top 3 most expensive active projects"),
    ]
    return [execute_query(query, description, db_path=db_path) for query, description in queries]


if __name__ == "__main__":
    demonstrate_sorting_limiting()
