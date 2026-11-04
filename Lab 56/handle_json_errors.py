#!/usr/bin/env python3
"""Demonstrate robust handling and validation of JSON data."""

import json
from pathlib import Path


def load_json_safely(filename, default_value=None):
    """Load JSON and return a default value when the file is absent or invalid."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: JSON file not found: {filename}")
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {filename}: {error.msg} (line {error.lineno}, column {error.colno})")
    except OSError as error:
        print(f"Could not read {filename}: {error}")
    return default_value


def validate_user_data(user_data):
    """Return (errors, warnings) for a user dictionary."""
    required_fields = ["id", "name", "email"]
    errors = []
    warnings = []
    for field in required_fields:
        if field not in user_data:
            errors.append(f"Missing required field: {field}")
        elif not user_data[field]:
            errors.append(f"Empty required field: {field}")
    if "id" in user_data and not isinstance(user_data["id"], int):
        errors.append("Field 'id' must be an integer")
    if "name" in user_data and not isinstance(user_data["name"], str):
        errors.append("Field 'name' must be a string")
    if "email" in user_data and not isinstance(user_data["email"], str):
        errors.append("Field 'email' must be a string")
    if "email" in user_data and isinstance(user_data["email"], str) and "@" not in user_data["email"]:
        warnings.append("Email format may be invalid")
    return errors, warnings


def handle_file_not_found():
    print("=== Handling File Not Found Errors ===")
    data = load_json_safely("nonexistent_file.json")
    if data is None:
        print("Creating a default file...")
        default_data = {
            "message": "Default data created",
            "timestamp": "2024-01-15T10:00:00Z",
            "status": "initialized",
        }
        with open("default_data.json", "w", encoding="utf-8") as file:
            json.dump(default_data, file, indent=4)
        print("Default file created: default_data.json")


def handle_malformed_json():
    print("\n=== Handling Malformed JSON ===")
    try:
        with open("malformed_json.json", "r", encoding="utf-8") as file:
            json.load(file)
        print("JSON loaded successfully")
    except FileNotFoundError:
        print("Error: malformed_json.json file not found!")
    except json.JSONDecodeError as error:
        print(f"JSON Decode Error: {error}")
        print(f"Error at line {error.lineno}, column {error.colno}")
        print(f"Error message: {error.msg}")
        print("\nAttempting to fix the JSON...")
        try:
            content = Path("malformed_json.json").read_text(encoding="utf-8")
            if content.count("{") > content.count("}"):
                fixed_content = content + "\n}"
                json.loads(fixed_content)
                Path("fixed_json.json").write_text(fixed_content, encoding="utf-8")
                print("Fix successful! Corrected JSON saved as: fixed_json.json")
            else:
                print("Automatic fix not applicable - manual correction needed")
        except (OSError, json.JSONDecodeError) as fix_error:
            print(f"Automatic fix failed - manual correction needed: {fix_error}")


def handle_invalid_syntax():
    print("\n=== Handling Invalid JSON Syntax ===")
    try:
        with open("invalid_syntax.json", "r", encoding="utf-8") as file:
            json.load(file)
        print("JSON loaded successfully")
    except FileNotFoundError:
        print("Error: invalid_syntax.json file not found!")
    except json.JSONDecodeError as error:
        print(f"JSON Syntax Error: {error}")
        print(f"Position: line {error.lineno}, column {error.colno}")
        try:
            lines = Path("invalid_syntax.json").read_text(encoding="utf-8").splitlines()
            error_line = error.lineno - 1
            print(f"\nProblematic area around line {error.lineno}:")
            for index in range(max(0, error_line - 2), min(len(lines), error_line + 3)):
                marker = ">>> " if index == error_line else "    "
                print(f"{marker}Line {index + 1}: {lines[index]}")
        except OSError as context_error:
            print(f"Could not show error context: {context_error}")


def handle_missing_keys():
    print("\n=== Handling Missing Keys ===")
    test_data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "email": "charlie@example.com"},
        ]
    }
    with open("incomplete_data.json", "w", encoding="utf-8") as file:
        json.dump(test_data, file, indent=4)
    try:
        with open("incomplete_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        print("Processing user data with missing fields:")
        for user in data["users"]:
            user_id = user.get("id", "Unknown ID")
            name = user.get("name", "Name not provided")
            email = user.get("email", "Email not provided")
            print(f"User {user_id}: {name} - {email}")
            try:
                print(f"  Complete record: {user['name']} - {user['email']}")
            except KeyError as error:
                print(f"  Missing required field: {error}")
    except (OSError, json.JSONDecodeError, KeyError) as error:
        print(f"Error processing incomplete data: {error}")


def demonstrate_structure_validation():
    print("\n=== JSON Structure Validation ===")
    test_cases = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": "1", "name": "Bob", "email": "bob@example.com"},
        {"name": "Charlie", "email": "charlie@example.com"},
        {"id": 3, "name": "", "email": "dave@example.com"},
        {"id": 4, "name": "Eve", "email": "invalid-email"},
    ]
    for index, test_case in enumerate(test_cases, 1):
        print(f"\nValidating test case {index}: {test_case}")
        errors, warnings = validate_user_data(test_case)
        if errors:
            print(f"  Errors: {errors}")
        if warnings:
            print(f"  Warnings: {warnings}")
        if not errors and not warnings:
            print("  Valid data structure")


def robust_json_loader():
    print("\n=== Robust JSON Loader ===")
    sample = {"status": "ok", "items": [1, 2, 3]}
    with open("robust_sample.json", "w", encoding="utf-8") as file:
        json.dump(sample, file, indent=2)
    loaded = load_json_safely("robust_sample.json", default_value={})
    print(f"Loaded data: {loaded}")
    fallback = load_json_safely("missing_sample.json", default_value={"status": "default"})
    print(f"Fallback data: {fallback}")


if __name__ == "__main__":
    handle_file_not_found()
    handle_malformed_json()
    handle_invalid_syntax()
    handle_missing_keys()
    demonstrate_structure_validation()
    robust_json_loader()
