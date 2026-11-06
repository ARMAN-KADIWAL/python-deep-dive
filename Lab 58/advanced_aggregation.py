#!/usr/bin/env python3
"""Demonstrate aggregate filtering with GROUP BY and HAVING."""
from db_utils import execute_query


def demonstrate_advanced_aggregation(db_path=None):
    queries = [
        ("""SELECT department_id, COUNT(*) AS employee_count
            FROM employees GROUP BY department_id HAVING COUNT(*) > 1
            ORDER BY employee_count DESC""", "Departments with more than one employee"),
        ("""SELECT d.department_name, COUNT(e.employee_id) AS employee_count,
                   SUM(e.salary) AS total_salary_cost
            FROM departments d INNER JOIN employees e ON d.department_id = e.department_id
            GROUP BY d.department_id, d.department_name
            HAVING SUM(e.salary) > 140000 ORDER BY total_salary_cost DESC""", "Departments with total salary cost above $140,000"),
        ("""SELECT d.department_name, COUNT(p.project_id) AS project_count,
                   SUM(p.budget) AS total_project_budget
            FROM departments d INNER JOIN projects p ON d.department_id = p.department_id
            GROUP BY d.department_id, d.department_name
            HAVING COUNT(p.project_id) >= 2 ORDER BY total_project_budget DESC""", "Departments managing at least two projects"),
        ("""SELECT status, COUNT(*) AS project_count, SUM(budget) AS total_budget
            FROM projects GROUP BY status HAVING SUM(budget) > 100000
            ORDER BY total_budget DESC""", "Project statuses with combined budgets above $100,000"),
    ]
    return [execute_query(query, description, db_path=db_path) for query, description in queries]


if __name__ == "__main__":
    demonstrate_advanced_aggregation()
