#!/usr/bin/env python3
"""Demonstrate GROUP BY and aggregate functions."""
from db_utils import execute_query


def demonstrate_grouping_aggregation(db_path=None):
    queries = [
        ("SELECT department_id, COUNT(*) AS employee_count FROM employees GROUP BY department_id ORDER BY employee_count DESC", "Employee count by department"),
        ("""SELECT e.department_id, d.department_name, COUNT(*) AS employee_count,
                   AVG(e.salary) AS avg_salary, MIN(e.salary) AS min_salary, MAX(e.salary) AS max_salary
            FROM employees e INNER JOIN departments d ON e.department_id = d.department_id
            GROUP BY e.department_id, d.department_name ORDER BY avg_salary DESC""", "Salary statistics by department"),
        ("""SELECT d.department_name, SUM(e.salary) AS total_salary_cost, COUNT(e.employee_id) AS employee_count
            FROM departments d LEFT JOIN employees e ON d.department_id = e.department_id
            GROUP BY d.department_id, d.department_name ORDER BY total_salary_cost DESC""", "Total salary cost by department"),
        ("""SELECT d.department_name, COUNT(p.project_id) AS project_count,
                   SUM(p.budget) AS total_budget, AVG(p.budget) AS avg_budget
            FROM departments d LEFT JOIN projects p ON d.department_id = p.department_id
            GROUP BY d.department_id, d.department_name HAVING COUNT(p.project_id) > 0
            ORDER BY total_budget DESC""", "Project statistics by department (departments with projects)"),
        ("""SELECT status, COUNT(*) AS project_count, SUM(budget) AS total_budget, AVG(budget) AS avg_budget
            FROM projects GROUP BY status ORDER BY total_budget DESC""", "Project summary by status"),
        ("""SELECT strftime('%Y', hire_date) AS hire_year, COUNT(*) AS employees_hired
            FROM employees GROUP BY strftime('%Y', hire_date) ORDER BY hire_year""", "Employees hired by year"),
    ]
    return [execute_query(query, description, db_path=db_path) for query, description in queries]


if __name__ == "__main__":
    demonstrate_grouping_aggregation()
