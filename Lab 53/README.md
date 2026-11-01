# Lab 53: Metaclasses - Introduction to Metaclasses and Advanced OOP

## Objectives
- Understand metaclasses and Python's class creation model.
- Create metaclasses that add attributes and track class definitions.
- Validate required methods and method signatures.
- Create classes dynamically with type() and custom metaclasses.
- Build framework-style model and declarative-base examples.

## Requirements
Python 3.8 or newer. Standard library only.

## Lab programs
- basic_metaclass.py: add class timestamps, IDs, and enhanced method aliases.
- custom_class_creation.py: track class attributes, names, and inheritance.
- validation_metaclass.py: enforce required methods and validate method signatures.
- dynamic_classes.py: create model classes using type() and DynamicMeta.
- framework_metaclass.py: build model fields, validation, and an in-memory query manager.
- declarative_base.py: build a SQLAlchemy-style declarative base and column validation.
- test_metaclasses.py: automated tests for the lab programs.

## Run the examples
Run these commands from inside the Lab 53 folder:

    python3 basic_metaclass.py
    python3 custom_class_creation.py
    python3 validation_metaclass.py
    python3 dynamic_classes.py
    python3 framework_metaclass.py
    python3 declarative_base.py

## Run automated tests

    python3 -m unittest -v

## Notes
- The framework and declarative examples are educational in-memory demonstrations, not replacements for Django or SQLAlchemy.
- The provided source ends partway through the generated attribute-assignment method in declarative_base.py. That incomplete program has been completed with column descriptors, defaults, validation, and a demonstration.
