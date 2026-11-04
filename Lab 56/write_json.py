#!/usr/bin/env python3
"""Convert Python objects into JSON files."""

import json
from datetime import datetime


def write_simple_json():
    print("=== Writing Simple JSON Data ===")
    employee_data = {
        "employee_id": 1001,
        "name": "Sarah Wilson",
        "department": "Engineering",
        "position": "Software Developer",
        "salary": 75000,
        "skills": ["Python", "JavaScript", "SQL", "Git"],
        "remote_work": True,
        "start_date": "2023-01-15",
    }
    try:
        with open("employee_data.json", "w", encoding="utf-8") as file:
            json.dump(employee_data, file, indent=4)
        print("Employee data successfully written to employee_data.json")
        print(f"Original data type: {type(employee_data)}")
        with open("employee_data.json", "r", encoding="utf-8") as file:
            loaded_data = json.load(file)
        print("Data successfully loaded back from file:")
        print(json.dumps(loaded_data, indent=2))
    except (OSError, TypeError, ValueError) as error:
        print(f"Error writing JSON: {error}")


def write_complex_json():
    print("\n=== Writing Complex JSON Data ===")
    company_data = {
        "company_name": "TechCorp Solutions",
        "founded": 2010,
        "headquarters": {
            "address": "123 Tech Street",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94105",
            "coordinates": {"latitude": 37.7749, "longitude": -122.4194},
        },
        "employees": [
            {"id": 1, "name": "John Doe", "position": "CEO", "department": "Executive",
             "contact": {"email": "john.doe@techcorp.com", "phone": "+1-555-0101"}},
            {"id": 2, "name": "Jane Smith", "position": "CTO", "department": "Technology",
             "contact": {"email": "jane.smith@techcorp.com", "phone": "+1-555-0102"}},
        ],
        "products": [
            {"name": "CloudSync", "version": "2.1.0", "release_date": "2024-01-15",
             "features": ["Real-time sync", "Multi-platform", "Encryption"]},
            {"name": "DataAnalyzer", "version": "1.5.2", "release_date": "2023-11-20",
             "features": ["Machine Learning", "Visualization", "API Integration"]},
        ],
        "financial": {"revenue_2023": 5000000, "employees_count": 150,
                      "offices": ["San Francisco", "New York", "Austin"]},
    }
    try:
        with open("company_data.json", "w", encoding="utf-8") as file:
            json.dump(company_data, file, indent=4, sort_keys=True)
        print("Company data written to company_data.json")
        with open("company_data_compact.json", "w", encoding="utf-8") as file:
            json.dump(company_data, file, separators=(",", ":"))
        print("Compact version written to company_data_compact.json")
    except (OSError, TypeError, ValueError) as error:
        print(f"Error writing complex JSON: {error}")


def write_list_to_json():
    print("\n=== Writing List Data to JSON ===")
    students_list = [
        {"student_id": "S001", "name": "Alice Brown", "major": "Computer Science", "year": 3, "gpa": 3.7},
        {"student_id": "S002", "name": "Bob Green", "major": "Mathematics", "year": 2, "gpa": 3.9},
        {"student_id": "S003", "name": "Carol White", "major": "Physics", "year": 4, "gpa": 3.5},
    ]
    try:
        with open("students_list.json", "w", encoding="utf-8") as file:
            json.dump(students_list, file, indent=2)
        print("Students list written to students_list.json")
        print(f"Number of students: {len(students_list)}")
    except (OSError, TypeError, ValueError) as error:
        print(f"Error writing list to JSON: {error}")


def demonstrate_json_serialization():
    print("\n=== JSON Serialization Options ===")
    data = {
        "name": "Test Data",
        "timestamp": datetime.now().isoformat(),
        "numbers": [1, 2, 3, 4, 5],
        "nested": {"level1": {"level2": "deep value"}},
    }
    print("1. Default formatting:")
    print(json.dumps(data))
    print("\n2. Pretty formatted:")
    print(json.dumps(data, indent=4))
    print("\n3. Sorted keys:")
    print(json.dumps(data, indent=2, sort_keys=True))
    print("\n4. Compact format:")
    print(json.dumps(data, separators=(",", ":")))


if __name__ == "__main__":
    write_simple_json()
    write_complex_json()
    write_list_to_json()
    demonstrate_json_serialization()
