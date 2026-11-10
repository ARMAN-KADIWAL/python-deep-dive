# Python Deep Dive 🐍

<p align="center">
  <img alt="Python learning labs" src="https://img.shields.io/badge/Learning-Python-3979AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="Organized lab folders" src="https://img.shields.io/badge/Organized_Labs-51-5de6d4?style=for-the-badge&labelColor=17243b" />
  <img alt="Topics" src="https://img.shields.io/badge/Topics-OOP_%7C_SQLite_%7C_Pandas-9987ff?style=for-the-badge&labelColor=17243b" />
</p>

A practical Python learning collection, organized by lab number — from syntax and algorithms to OOP, databases, and Pandas. Each lab folder contains runnable code and a README.

> **Start here:** Pick a learning path below, open any lab folder, and follow that lab's README. For GitHub-linked proof of work, see the [daily tracker](#proof-of-completion--daily-work-log).

## Learning paths

Choose a topic below. Every linked lab has runnable examples and its own instructions.

<details>
<summary><strong>01 — Fundamentals & core data structures · 24 labs</strong></summary>

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

</details>

<details>
<summary><strong>02 — Packages & standard library · 5 labs</strong></summary>

- [Lab 31 - Importing Modules and Standard Libraries](Lab%2031/)
- [Lab 32 - Creating and Using Python Packages](Lab%2032/)
- [Lab 33 - Exploring the Python Standard Library](Lab%2033/)
- [Lab 34 - Advanced Package Usage](Lab%2034/)
- [Lab 35 - Final Project: Building a Package with Python](Lab%2035/)

</details>

<details>
<summary><strong>03 — Object-oriented Python · 8 labs</strong></summary>

- [Lab 36 - Introduction to Classes and Objects](Lab%2036/)
- [Lab 37 - Constructor and Initialization: Using __init__](Lab%2037/)
- [Lab 38 - Methods and Functions: Defining and Calling Methods](Lab%2038/)
- [Lab 39 - Inheritance: Basic Inheritance Concept](Lab%2039/)
- [Lab 40 - Polymorphism: Understanding Polymorphism](Lab%2040/)
- [Lab 41 - Encapsulation: Getters, Setters, and Properties](Lab%2041/)
- [Lab 47 - Multiple Inheritance](Lab%2047/)
- [Lab 48 - Final Project: OOP Library Management System](Lab%2048/)

</details>

<details>
<summary><strong>04 — Advanced Python & file handling · 8 labs</strong></summary>

- [Lab 49 - Introduction to Python Decorators](Lab%2049/)
- [Lab 50 - Understanding Python Generators](Lab%2050/)
- [Lab 51 - Context Managers](Lab%2051/)
- [Lab 52 - Iterators and Iterables](Lab%2052/)
- [Lab 53 - Metaclasses](Lab%2053/)
- [Lab 54 - Reading and Writing Files](Lab%2054/)
- [Lab 55 - Handling CSV Data](Lab%2055/)
- [Lab 56 - Handling JSON Data](Lab%2056/)

</details>

<details open>
<summary><strong>05 — Databases, SQLite & Pandas · 6 labs</strong></summary>

- [Lab 57 - Interacting with Databases - Using SQLite](Lab%2057/)
- [Lab 58 - Querying and Filtering Data in SQLite](Lab%2058/)
- [Lab 59 - Integrating Databases with User Input](Lab%2059/)
- [Lab 60 - Introduction to Pandas - Working with DataFrames](Lab%2060/)
- [Lab 61 - Data Cleaning with Pandas - Handling Missing Data](Lab%2061/)
- [Lab 62 - Advanced Pandas Operations - Merging and Grouping Data](Lab%2062/)

</details>

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

For Lab 56, run these commands from inside the Lab 56 directory:

    python3 read_json.py
    python3 write_json.py
    python3 parse_nested_json.py
    python3 handle_json_errors.py
    python3 modify_json.py
    python3 -m unittest -v

For Lab 57, run these commands from inside the Lab 57 directory:

    python3 -m pip install -r requirements.txt
    python3 student_management.py
    python3 data_insertion.py
    python3 data_queries.py --search John
    python3 data_updates.py
    python3 -m unittest -v

For Lab 58, run these commands from inside the Lab 58 directory:

    python3 setup_database.py
    python3 filtering_queries.py
    python3 advanced_filtering.py
    python3 sorting_limiting.py
    python3 join_operations.py
    python3 advanced_joins.py
    python3 grouping_aggregation.py
    python3 advanced_aggregation.py
    python3 -m unittest -v

For Lab 59, run these commands from inside the Lab 59 directory:

    python3 database_setup.py
    python3 user_management.py
    python3 security_demo.py
    python3 -m unittest -v test_system.py
    python3 database_report.py

For Lab 60, run these commands from inside the Lab 60 directory:

    python3 -m pip install -r requirements.txt
    python3 pandas_lab.py
    python3 -m unittest -v

For Lab 61, run these commands from inside the Lab 61 directory:

    python3 -m pip install -r requirements.txt
    python3 pandas_lab.py
    python3 -m unittest -v test_pandas_lab.py

For Lab 62, run these commands from inside the Lab 62 directory:

    python3 -m pip install -r requirements.txt
    python3 lab_62.py
    python3 -m unittest -v test_lab_62.py

For Lab 41:

    python3 person_class.py
    python3 test_validation.py
    python3 test_direct_access.py
    python3 encapsulation_demo.py
    python3 person_with_properties.py
    python3 -m unittest -v test_lab41.py
