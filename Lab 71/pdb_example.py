# pdb_example.py - Introduction to Python Debugger
import pdb

def calculate_factorial(n):
    """Calculate factorial of a number"""
    print(f"Calculating factorial of {n}")
    
    # Set a breakpoint here
    pdb.set_trace()
    
    if n < 0:
        return "Factorial not defined for negative numbers"
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
            print(f"Step {i}: result = {result}")
        return result

def main():
    print("=== Factorial Calculator with pdb ===")
    
    # Test with different values
    test_values = [5, 0, -3]
    
    for value in test_values:
        print(f"\nTesting factorial({value}):")
        result = calculate_factorial(value)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
