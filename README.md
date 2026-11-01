# Python Deep Dive

Python learning labs organized by lab number. Each lab folder contains runnable Python examples and a README describing the concepts covered.

## Available Labs

- [Lab 6 - Variables and Data Types](Lab%206/)
- [Lab 7 - Basic Operators](Lab%207/)
- [Lab 8 - Control Flow Statements](Lab%208/)
- [Lab 9 - Functions and Scope](Lab%209/)
- [Lab 10 - Functions and Return Values](Lab%2010/)
- [Lab 11 - Error Handling and Exceptions](Lab%2011/)
- [Lab 12 - Multiple Exceptions and Custom Exceptions](Lab%2012/)
- [Lab 13 - Nested Control Flow](Lab%2013/)
- [Lab 14 - Functions with Loops](Lab%2014/)
- [Lab 15 - Simple Python Calculator Project](Lab%2015/)
- [Lab 16 - Lists and List Operations](Lab%2016/)
- [Lab 17 - List Comprehensions](Lab%2017/)
- [Lab 18 - Tuples and Sequences](Lab%2018/)
- [Lab 19 - Working with Sequences](Lab%2019/)
- [Lab 20 - Dictionaries](Lab%2020/)
- [Lab 21 - Sets](Lab%2021/)
- [Lab 22 - Advanced Set Operations](Lab%2022/)
- [Lab 23 - Strings and String Manipulation](Lab%2023/)
- [Lab 24 - String Formatting and Advanced Manipulation](Lab%2024/)
- [Lab 25 - Files and Input/Output](Lab%2025/)
- [Lab 26 - Working with CSV Files](Lab%2026/)
- [Lab 27 - Reading and Writing JSON Files](Lab%2027/)
- [Lab 28 - Advanced File I/O and Context Managers](Lab%2028/)
- [Lab 29 - Data Structures and File I/O Final Project](Lab%2029/)
- [Lab 31 - Importing Modules and Standard Libraries](Lab%2031/)
- [Lab 32 - Creating and Using Python Packages](Lab%2032/)
- [Lab 33 - Exploring the Python Standard Library](Lab%2033/)
- [Lab 34 - Advanced Package Usage](Lab%2034/)
- [Lab 35 - Final Project: Building a Package with Python](Lab%2035/)
- [Lab 36 - Introduction to Classes and Objects](Lab%2036/)
- [Lab 37 - Constructor and Initialization: Using __init__](Lab%2037/)
- [Lab 38 - Methods and Functions: Defining and Calling Methods](Lab%2038/)
- [Lab 39 - Inheritance: Basic Inheritance Concept](Lab%2039/)
- [Lab 40 - Polymorphism: Understanding Polymorphism](Lab%2040/)
- [Lab 41 - Encapsulation: Getters, Setters, and Properties](Lab%2041/)
- [Lab 47 - Multiple Inheritance](Lab%2047/)
- [Lab 48 - Final Project: OOP Library Management System](Lab%2048/)
- [Lab 49 - Introduction to Python Decorators](Lab%2049/)
- [Lab 50 - Understanding Python Generators](Lab%2050/)
- [Lab 51 - Context Managers](Lab%2051/)
- [Lab 52 - Iterators and Iterables](Lab%2052/)
- [Lab 53 - Metaclasses](Lab%2053/)

## Proof of Completion — Daily Work Log

Use the terminal-based tracker to record what you worked on each day and link the entry to a real GitHub commit when available. It uses only the Python standard library.

From the repository root, run:

    python3 progress_tracker.py add

Other commands:

    python3 progress_tracker.py list
    python3 progress_tracker.py report

- `add` asks for the date, lab/topic, work completed, what you learned, and status.
- The tracker can attach the latest local Git commit and create its GitHub commit URL from the repository's `origin` remote.
- Entries are stored in `progress/work_log.json`.
- A readable report is generated at `progress/PROOF_OF_COMPLETION.md`.

For valid commit links, run the script from a local clone of this repository with Git installed and the GitHub `origin` remote configured. The daily work description is self-reported; a commit link proves that a commit exists, not that every described task was independently verified.

## Running a Lab

Open a lab folder and follow its README. Most scripts can be run with Python 3 without interactive input.

For Lab 32:

    python3 test_mathtools.py
    python3 advanced_test.py

For Lab 33:

    python3 os_demo.py
    python3 shutil_demo.py
    python3 sys_demo.py Arman
    python3 backup_script.py
    python3 exit_demo.py

For Lab 34:

    python3 main_demo.py
    python3 -m unittest advanced_test.py -v

For Lab 35:

    python3 example_usage.py
    python3 test_mathtools.py
    python3 validate_package.py

For Lab 36:

    python3 person_class.py
    python3 multiple_persons.py
    python3 enhanced_person.py
    python3 self_demo.py
    python3 student_system.py
    python3 object_experiments.py
    python3 -m unittest advanced_test.py -v

For Lab 37:

    python3 student_class.py
    python3 book_library.py
    python3 vehicle_system.py
    python3 inventory_system.py
    python3 default_parameters.py
    python3 -m unittest -v test_lab37.py

For Lab 38:

    python3 student_manager.py
    python3 test_students.py
    python3 advanced_student.py
    python3 student_system.py
    python3 -m unittest -v test_student_management.py

For Lab 39, run these commands from inside the Lab 39 directory:

    python3 test_inheritance.py
    python3 enhanced_test.py
    python3 override_test.py
    python3 experiment.py
    python3 advanced_concepts.py
    python3 -m unittest -v test_lab39.py

For Lab 40, run these commands from inside the Lab 40 directory:

    python3 shapes.py
    python3 -m unittest -v test_lab40.py

For Lab 41:

    python3 person_class.py
    python3 test_validation.py
    python3 test_direct_access.py
    python3 encapsulation_demo.py
    python3 person_with_properties.py
    python3 -m unittest -v test_lab41.py
