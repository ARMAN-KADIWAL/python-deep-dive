# fixed_calculator.py - Debugged and corrected calculator
import math
import pdb

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    if len(numbers) == 0:
        print("Warning: Cannot calculate average of empty list")
        return 0
    
    total = sum(numbers)
    average = total / len(numbers)
    return average

def get_square_root(number):
    """Get the square root of a number"""
    # Fixed: numbr -> number
    if number < 0:
        return "Cannot calculate square root of negative number"
    return math.sqrt(number)

def access_list_element(data_list, index):
    """Access an element from a list by index"""
    # Fixed: Added bounds checking
    if index < 0 or index >= len(data_list):
        return f"Index {index} is out of range for list of length {len(data_list)}"
    return data_list[index]

def convert_to_integer(value):
    """Convert a value to integer"""
    # Fixed: Added proper error handling
    try:
        return int(value)
    except (TypeError, ValueError) as e:
        return f"Cannot convert {type(value).__name__} to integer: {str(e)}"

def main():
    print("=== Fixed Calculator ===")
    
    # Test case 1: Empty list for average calculation
    print("\n--- Test Case 1: Empty List Average ---")
    empty_list = []
    print("Calculating average of empty list...")
    avg = calculate_average(empty_list)
    print(f"Average: {avg}")
    
    # Test case 2: Square root calculation
    print("\n--- Test Case 2: Square Root ---")
    print("Calculating square root of 16...")
    sqrt_result = get_square_root(16)
    print(f"Square root: {sqrt_result}")
    
    print("Calculating square root of -4...")
    sqrt_result = get_square_root(-4)
    print(f"Square root: {sqrt_result}")
    
    # Test case 3: List access
    print("\n--- Test Case 3: List Access ---")
    sample_list = [1, 2, 3, 4, 5]
    print(f"Accessing element at index 2 from list: {sample_list}")
    element = access_list_element(sample_list, 2)
    print(f"Element: {element}")
    
    print(f"Accessing element at index 10 from list: {sample_list}")
    element = access_list_element(sample_list, 10)
    print(f"Element: {element}")
    
    # Test case 4: Type conversion
    print("\n--- Test Case 4: Type Conversion ---")
    print("Converting string '42' to integer...")
    valid_conversion = convert_to_integer("42")
    print(f"Integer result: {valid_conversion}")
    
    print("Converting dictionary to integer...")
    invalid_value = {"key": "value"}
    integer_result = convert_to_integer(invalid_value)
    print(f"Integer result: {integer_result}")

if __name__ == "__main__":
    main()
