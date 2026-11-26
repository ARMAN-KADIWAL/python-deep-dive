#!/usr/bin/env python3
"""
Lab 96: Enhanced Traceback Demonstration
This script shows how Python provides better traceback information
"""

import traceback
import sys

def level_three_function():
    """Third level function that will cause an error"""
    data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}

    # This will cause a KeyError with enhanced context
    user_age = data["users"][0]["age"]  # 'age' key doesn't exist
    return user_age

def level_two_function():
    """Second level function"""
    print("Entering level two function...")
    result = level_three_function()
    return result * 2

def level_one_function():
    """First level function"""
    print("Entering level one function...")
    try:
        final_result = level_two_function()
        return final_result
    except KeyError as e:
        print(f"KeyError caught in level_one_function: {e}")
        print("Enhanced traceback shows the full call stack!")
        raise  # Re-raise to see full traceback

def demonstrate_nested_errors():
    """Demonstrate nested function call errors"""
    print("=== Enhanced Traceback Demo ===")

    try:
        result = level_one_function()
        print(f"Final result: {result}")
    except KeyError as e:
        print(f"\nFinal exception handler caught: {e}")
        traceback.print_exc(file=sys.stdout)

def demonstrate_attribute_error_context():
    """Show enhanced AttributeError messages"""
    print("\n=== Enhanced AttributeError Context ===")

    class Person:
        def __init__(self, name):
            self.name = name
            self.email = None

    person = Person("John Doe")

    try:
        # Typo in attribute name
        person_phone = person.phone_number
        print(f"Phone: {person_phone}")
    except AttributeError as e:
        print(f"AttributeError caught: {e}")
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    print("Python Enhanced Traceback and Context Demo")
    print("=" * 55)

    demonstrate_nested_errors()
    demonstrate_attribute_error_context()
