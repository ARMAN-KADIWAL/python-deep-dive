#!/usr/bin/env python3
"""
Lab 96: Error Context Analysis
This script demonstrates how Python provides better error context
"""

import traceback
import sys

def analyze_syntax_like_errors():
    """Demonstrate errors that show code context"""
    print("=== Error Context Analysis ===")

    # Example 1: Dictionary key error with context
    print("1. Dictionary KeyError with context:")
    user_data = {
        "profile": {
            "personal": {
                "name": "Alice Smith",
                "email": "alice@example.com"
            },
            "preferences": {
                "theme": "dark",
                "language": "en"
            }
        }
    }

    try:
        # Accessing non-existent nested key
        user_phone = user_data["profile"]["contact"]["phone"]
        print(f"Phone: {user_phone}")
    except KeyError as e:
        print(f"   KeyError: {e}")
        traceback.print_exc(file=sys.stdout)

    print("\n" + "-"*50)

    # Example 2: List comprehension error
    print("2. List comprehension error context:")
    numbers = [1, 2, "three", 4, 5]

    try:
        # This will fail when it hits the string
        squared = [x ** 2 for x in numbers]
        print(f"Squared numbers: {squared}")
    except TypeError as e:
        print(f"   TypeError: {e}")
        traceback.print_exc(file=sys.stdout)

def analyze_import_errors():
    """Demonstrate enhanced import error messages"""
    print("\n3. Import error with suggestions:")

    try:
        # Intentional typo in module name
        import requsts  # Should be 'requests'
    except ModuleNotFoundError:
        traceback.print_exc(file=sys.stdout)
    except ImportError:
        traceback.print_exc(file=sys.stdout)

def analyze_function_call_errors():
    """Demonstrate function call error improvements"""
    print("\n4. Function call error analysis:")

    def calculate_discount(price, discount_rate, tax_rate=0.1):
        """Calculate final price with discount and tax"""
        discounted = price * (1 - discount_rate)
        final_price = discounted * (1 + tax_rate)
        return final_price

    try:
        # Wrong argument types
        result = calculate_discount("100", "0.2")
        print(f"Final price: {result}")
    except TypeError as e:
        print(f"   TypeError: {e}")
        traceback.print_exc(file=sys.stdout)

    print("\n" + "-"*50)

    try:
        # Missing required argument
        result = calculate_discount(100)  # Missing discount_rate
        print(f"Final price: {result}")
    except TypeError as e:
        print(f"   TypeError: {e}")
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    print("Python Error Context Analysis")
    print("=" * 40)

    analyze_syntax_like_errors()
    analyze_import_errors()
    analyze_function_call_errors()

    print("\n" + "="*40)
    print("Analysis complete! Notice the enhanced context in each error.")
