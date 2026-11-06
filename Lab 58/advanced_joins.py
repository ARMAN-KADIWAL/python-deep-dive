#!/usr/bin/env python3
"""Demonstrate LEFT JOIN, self JOIN, and aggregate JOIN queries."""
from db_utils import execute_query


def demonstrate_advanced_joins(db_path=None):
    queries = [
        ("""SELECT d.department_name, d.budget, e.first_name, e.last_name, e.salary
            FROM departments d LEFT JOIN employees e ON d.department_id = e.department_id
            ORDER BY d.department_name""", "All departments with employees (LEFT JOIN)"),
        ("""SELECT d.department_name, COUNT(p.project_id) AS project_count
            FROM departments d LEFT JOIN projects p ON d.department_id = p.department_id
            GROUP BY d.department_id, d.department_name ORDER BY project_count DESC""", "Departments with project counts"),
        ("""SELECT e1.first_name || ' ' || e1.last_name AS employee1,
                   e2.first_name || ' ' || e2.last_name AS employee2, d.department_name
            FROM employees e1 INNER JOIN employees e2
              ON e1.department_id = e2.department_id AND e1.employee_id < e2.employee_id
            INNER JOIN departments d ON e1.department_id = d.department_id
            ORDER BY d.department_name""", "Employees in the same department (Self JOIN)"),
        ("""SELECT d.department_name, COUNT(DISTINCT e.employee_id) AS employee_count,
                   COUNT(DISTINCT p.project_id) AS project_count, AVG(e.salary) AS avg_salary,
                   SUM(DISTINCT p.budget) AS total_project_budget
            FROM departments d LEFT JOIN employees e ON d.department_id = e.department_id
            LEFT JOIN projects p ON d.department_id = p.department_id
            GROUP BY d.department_id, d.department_name ORDER BY employee_count DESC""", "Department summary with employee and project statistics"),
    ]
    return [execute_query(query, description, db_path=db_path) for query, description in queries]


if __name__ == "__main__":
    demonstrate_advanced_joins()
