# Lab 56: Handling JSON Data - Reading and Writing JSON Files

## Objectives
- Understand JSON objects, arrays, name/value pairs, and string quoting rules.
- Read JSON files with Python's built-in json module.
- Convert Python dictionaries and lists to JSON files.
- Parse and search nested JSON structures.
- Handle missing files, malformed JSON, missing fields, and invalid data types.
- Add, update, and remove JSON fields.

## Requirements
Python 3.8 or later. This lab uses only the Python standard library.

## Files
- student_data.json: sample student object for reading.
- university_data.json: sample university object with nested departments and facilities.
- read_json.py: read JSON from files and strings and pretty-print JSON.
- write_json.py: serialize dictionaries and lists with different formatting options.
- parse_nested_json.py: create, parse, safely access, and search nested API response data.
- malformed_json.json: intentionally incomplete JSON for error-handling practice.
- invalid_syntax.json: intentionally invalid JSON with a trailing comma.
- handle_json_errors.py: handle missing files, decode errors, missing keys, validation, and safe loading.
- modify_json.py: add, update, and remove fields in a JSON document.
- test_json_lab.py: automated tests for the lab examples.

## Run the examples
Run commands from inside the Lab 56 directory:

    python3 read_json.py
    python3 write_json.py
    python3 parse_nested_json.py
    python3 handle_json_errors.py
    python3 modify_json.py

## Run automated tests

    python3 -m unittest -v

## Notes
- write_json.py, parse_nested_json.py, handle_json_errors.py, and modify_json.py create output files in the current working directory.
- malformed_json.json and invalid_syntax.json are deliberately invalid. They are test fixtures, not files to repair before running the lab.
- handle_json_errors.py demonstrates a conservative repair for a missing closing brace. More complex JSON syntax errors require manual correction.
- The supplied lab document ends partway through the robust_json_loader() example. That incomplete ending is completed here as a reusable safe-loading function with a caller-provided fallback, consistent with the lab's stated error-handling objectives.
