#!/usr/bin/env python3
"""
Demonstration of TDD Factorial Implementation
"""

from factorial import factorial

def main():
    print("=== TDD Factorial Function Demo ===")
    print()
    
    # Test normal cases
    test_cases = [0, 1, 2, 3, 4, 5, 6, 7]
    
    print("Normal test cases:")
    for n in test_cases:
        result = factorial(n)
        print(f"factorial({n}) = {result}")
    
    print()
    print("Edge case handling:")
    
    # Test error cases
    try:
        factorial(-1)
    except ValueError as e:
        print(f"factorial(-1) raises ValueError: {e}")
    
    try:
        factorial(3.5)
    except TypeError as e:
        print(f"factorial(3.5) raises TypeError: {e}")
    
    try:
        factorial("5")
    except TypeError as e:
        print(f"factorial('5') raises TypeError: {e}")

if __name__ == "__main__":
    main()
