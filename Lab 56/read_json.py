#!/usr/bin/env python3
"""Read simple and nested JSON data from files and strings."""

import json


def read_simple_json():
    print("=== Reading Simple JSON Data ===")
    try:
        with open("student_data.json", "r", encoding="utf-8") as file:
            student_data = json.load(file)
        print(f"Student Name: {student_data['name']}")
        print(f"Age: {student_data['age']}")
        print(f"Major: {student_data['major']}")
        print(f"GPA: {student_data['gpa']}")
        print(f"Courses: {', '.join(student_data['courses'])}")
        print(f"Active Status: {student_data['active']}")
        print(f"Graduation Year: {student_data['graduation_year']}")
        print(f"\nData type after loading: {type(student_data)}")
    except FileNotFoundError:
        print("Error: student_data.json file not found!")
    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON format - {error}")
    except KeyError as error:
        print(f"Error: Missing key in JSON data - {error}")


def read_complex_json():
    print("\n=== Reading Complex JSON Data ===")
    try:
        with open("university_data.json", "r", encoding="utf-8") as file:
            university_data = json.load(file)
        print(f"University: {university_data['university']}")
        print(f"Location: {university_data['location']}")
        print(f"Established: {university_data['established']}")
        print("\nDepartments:")
        for department in university_data["departments"]:
            print(f"  - {department['name']}")
            print(f"    Head: {department['head']}")
            print(f"    Students: {department['students']}")
            print(f"    Programs: {', '.join(department['programs'])}")
        print("\nFacilities:")
        facilities = university_data["facilities"]
        library = facilities["library"]
        print(f"  Library: {library['name']}")
        print(f"    Books: {library['books']:,}")
        print(f"    Digital Resources: {library['digital_resources']}")
        labs = facilities["labs"]
        print(f"  Computer Labs: {labs['computer_labs']}")
        print(f"  Research Labs: {labs['research_labs']}")
    except FileNotFoundError:
        print("Error: university_data.json file not found!")
    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON format - {error}")
    except KeyError as error:
        print(f"Error: Missing key in JSON data - {error}")


def demonstrate_json_methods():
    print("\n=== JSON Methods Demonstration ===")
    json_string = '{"name": "Bob", "age": 25, "city": "New York"}'
    data_from_string = json.loads(json_string)
    print(f"Data from string: {data_from_string}")
    try:
        with open("student_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        print("\nPretty printed JSON:")
        print(json.dumps(data, indent=4, sort_keys=True))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Error in demonstration: {error}")


if __name__ == "__main__":
    read_simple_json()
    read_complex_json()
    demonstrate_json_methods()
