# flow_control_demo.py - Demonstrating pdb flow control
import pdb

def outer_function(x):
    """Outer function that calls inner functions"""
    print(f"Outer function called with x = {x}")
    pdb.set_trace()  # Main breakpoint
    
    result1 = inner_function_a(x)
    result2 = inner_function_b(x)
    
    final_result = combine_results(result1, result2)
    return final_result

def inner_function_a(value):
    """First inner function"""
    print(f"Inner function A: processing {value}")
    processed = value * 2
    return processed

def inner_function_b(value):
    """Second inner function"""
    print(f"Inner function B: processing {value}")
    processed = value + 10
    return processed

def combine_results(a, b):
    """Combine two results"""
    print(f"Combining {a} and {b}")
    return a + b

def main():
    print("=== Flow Control Demonstration ===")
    
    test_values = [5, 10]
    
    for value in test_values:
        print(f"\n--- Processing value: {value} ---")
        result = outer_function(value)
        print(f"Final result: {result}")

if __name__ == "__main__":
    main()
