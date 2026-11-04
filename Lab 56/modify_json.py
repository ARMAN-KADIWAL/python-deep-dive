#!/usr/bin/env python3
"""Add, update, and remove fields in a JSON document."""

import json


def modify_student_data(source="student_data.json", destination="modified_student_data.json"):
    try:
        with open(source, "r", encoding="utf-8") as file:
            student = json.load(file)
        student["phone"] = "+1-555-0100"
        student["gpa"] = 3.9
        student.pop("active", None)
        with open(destination, "w", encoding="utf-8") as file:
            json.dump(student, file, indent=4)
        print(f"Updated JSON saved to {destination}")
        return student
    except FileNotFoundError:
        print(f"Source file not found: {source}")
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {source}: {error}")
    except OSError as error:
        print(f"File operation failed: {error}")
    return None


if __name__ == "__main__":
    modify_student_data()
