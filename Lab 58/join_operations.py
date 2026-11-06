#!/usr/bin/env python3
"""Demonstrate INNER JOIN operations across related tables."""
from db_utils import execute_query


def demonstrate_joins(db_path=None):
    queries = [
        ("""SELECT e.first_name, e.last_name, e.salary, d.department_name
            FROM employees e INNER JOIN departments d ON e.department_id = d.department_id""", "Employees with their department names (INNER JOIN)"),
        ("""SELECT e.first_name, e.last_name, e.salary, d.department_name
            FROM employees e INNER JOIN departments d ON e.department_id = d.department_id
            WHERE e.salary > 75000""", "High-salary employees with department names"),
        ("""SELECT p.project_name, p.budget, p.status, d.department_name
            FROM projects p INNER JOIN departments d ON p.department_id = d.department_id""", "Projects with their department names"),
        ("""SELECT e.first_name, e.last_name, d.department_name, p.project_name, p.status
            FROM employees e INNER JOIN departments d ON e.department_id = d.department_id
            INNER JOIN projects p ON d.department_id = p.department_id
            WHERE p.status = 'Active'""", "Employees in departments with active projects"),
        ("""SELECT e.first_name, e.last_name, e.salary, d.department_name
            FROM employees e INNER JOIN departments d ON e.department_id = d.department_id
            ORDER BY d.department_name, e.salary DESC""", "Employees by department, ordered by salary"),
    ]
    return [execute_query(query, description, db_path=db_path) for query, description in queries]


if __name__ == "__main__":
    demonstrate_joins()
