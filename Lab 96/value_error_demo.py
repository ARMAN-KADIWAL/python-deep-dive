#!/usr/bin/env python3
"""
Lab 96: ValueError Demonstration
This script demonstrates enhanced ValueError messages in Python
"""

import math

def demonstrate_value_errors():
    """Function to trigger various ValueError scenarios"""

    # Example 1: Invalid literal for int()
    print("=== ValueError Example 1: Invalid Integer Conversion ===")
    try:
        number = int("hello")
        print(f"Converted number: {number}")
    except ValueError as e:
        print(f"ValueError caught: {e}")
        print(f"Error type: {type(e).__name__}")

    print("\n" + "="*40 + "\n")

    # Example 2: Math domain error
    print("=== ValueError Example 2: Math Domain Error ===")
    try:
        result = math.sqrt(-1)
        print(f"Square root of -1: {result}")
    except ValueError as e:
        print(f"ValueError caught: {e}")
        print(f"Error type: {type(e).__name__}")

    print("\n" + "="*40 + "\n")

    # Example 3: Invalid base for int conversion
    print("=== ValueError Example 3: Invalid Base Conversion ===")
    try:
        number = int("123", base=1)  # Base must be >= 2
        print(f"Converted number: {number}")
    except ValueError as e:
        print(f"ValueError caught: {e}")
        print(f"Error type: {type(e).__name__}")

def demonstrate_list_value_errors():
    """Demonstrate list-related value errors"""
    print("=== ValueError Example 4: List Value Not Found ===")

    colors = ["red", "green", "blue"]
    print(f"Colors list: {colors}")

    try:
        index = colors.index("yellow")
        print(f"Index of yellow: {index}")
    except ValueError as e:
        print(f"ValueError caught: {e}")
        print(f"Error type: {type(e).__name__}")

    print("\n" + "="*40 + "\n")

    # Example 5: Unpacking value error
    print("=== ValueError Example 5: Unpacking Mismatch ===")
    try:
        coordinates = (10, 20, 30)  # 3 values
        x, y = coordinates  # Trying to unpack into 2 variables
        print(f"X: {x}, Y: {y}")
    except ValueError as e:
        print(f"ValueError caught: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    print("Python Enhanced ValueError Messages Demo")
    print("=" * 50)

    demonstrate_value_errors()
    print("\n" + "="*50 + "\n")
    demonstrate_list_value_errors()
