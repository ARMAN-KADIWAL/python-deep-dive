#!/usr/bin/env python3
"""
Lab 96: IndexError Demonstration
This script demonstrates how Python provides enhanced error messages for IndexError
"""

def demonstrate_index_error():
    """Function to trigger IndexError with detailed context"""

    # Example 1: List index out of range
    print("=== IndexError Example 1: List Access ===")
    fruits = ["apple", "banana", "orange"]
    print(f"List contents: {fruits}")
    print(f"List length: {len(fruits)}")

    try:
        # This will cause an IndexError
        invalid_fruit = fruits[5]
        print(f"Fruit at index 5: {invalid_fruit}")
    except IndexError as e:
        print(f"IndexError caught: {e}")
        print(f"Error type: {type(e).__name__}")

    print("\n" + "="*50 + "\n")

    # Example 2: String index out of range
    print("=== IndexError Example 2: String Access ===")
    message = "Hello"
    print(f"String: '{message}'")
    print(f"String length: {len(message)}")

    try:
        # This will cause an IndexError
        invalid_char = message[10]
        print(f"Character at index 10: {invalid_char}")
    except IndexError as e:
        print(f"IndexError caught: {e}")
        print(f"Error type: {type(e).__name__}")

def demonstrate_negative_index_error():
    """Function to show negative index errors"""
    print("=== IndexError Example 3: Negative Index Beyond Range ===")
    numbers = [1, 2, 3]
    print(f"List: {numbers}")

    try:
        # This will cause an IndexError with negative index
        invalid_number = numbers[-5]
        print(f"Number at index -5: {invalid_number}")
    except IndexError as e:
        print(f"IndexError caught: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    print("Python Enhanced IndexError Messages Demo")
    print("=" * 50)

    demonstrate_index_error()
    print("\n" + "="*50 + "\n")
    demonstrate_negative_index_error()
