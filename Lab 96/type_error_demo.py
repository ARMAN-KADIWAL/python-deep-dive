#!/usr/bin/env python3
"""
Lab 96: TypeError Demonstration
This script demonstrates enhanced TypeError messages in Python
"""

def demonstrate_type_errors():
    """Function to trigger various TypeError scenarios"""

    # Example 1: Unsupported operand types
    print("=== TypeError Example 1: Unsupported Operand Types ===")
    try:
        result = "Hello" + 42
        print(f"Result: {result}")
    except TypeError as e:
        print(f"TypeError caught: {e}")
        print(f"Error type: {type(e).__name__}")

    print("\n" + "="*40 + "\n")

    # Example 2: Function argument type mismatch
    print("=== TypeError Example 2: Function Argument Mismatch ===")
    def calculate_area(length, width):
        """Calculate rectangle area - expects numeric types"""
        return length * width

    try:
        area = calculate_area("10", 5.5)
        print(f"Area: {area}")
    except TypeError as e:
        print(f"TypeError caught: {e}")
        print(f"Error type: {type(e).__name__}")

    print("\n" + "="*40 + "\n")

    # Example 3: Incorrect number of arguments
    print("=== TypeError Example 3: Incorrect Argument Count ===")
    def greet_person(first_name, last_name):
        """Function expecting exactly 2 arguments"""
        return f"Hello, {first_name} {last_name}!"

    try:
        greeting = greet_person("John")
        print(greeting)
    except TypeError as e:
        print(f"TypeError caught: {e}")
        print(f"Error type: {type(e).__name__}")

def demonstrate_method_type_errors():
    """Demonstrate method-related type errors"""
    print("=== TypeError Example 4: Method Call on Wrong Type ===")

    try:
        # Trying to call string method on integer
        number = 42
        result = number.upper()
        print(f"Result: {result}")
    except AttributeError as e:
        print(f"AttributeError caught: {e}")
        print(f"Error type: {type(e).__name__}")

    print("\n" + "="*40 + "\n")

    # Example 5: Unhashable type
    print("=== TypeError Example 5: Unhashable Type ===")
    try:
        # Lists are unhashable and cannot be dictionary keys
        my_dict = {[1, 2, 3]: "value"}
        print(f"Dictionary: {my_dict}")
    except TypeError as e:
        print(f"TypeError caught: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    print("Python Enhanced TypeError Messages Demo")
    print("=" * 50)

    demonstrate_type_errors()
    print("\n" + "="*50 + "\n")
    demonstrate_method_type_errors()
