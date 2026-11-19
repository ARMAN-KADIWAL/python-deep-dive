# buggy_calculator.py - A calculator with intentional bugs
import math

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    total = 0
    for num in numbers:
        total += num
    # Bug 1: Division by zero potential
    average = total / len(numbers)
    return average

def get_square_root(number):
    """Get the square root of a number"""
    # Bug 2: NameError - undefined variable
    if numbr < 0:
        return "Cannot calculate square root of negative number"
    return math.sqrt(number)

def access_list_element(data_list, index):
    """Access an element from a list by index"""
    # Bug 3: IndexError potential
    return data_list[index]

def convert_to_integer(value):
    """Convert a value to integer"""
    # Bug 4: TypeError potential
    return int(value)

def main():
    print("=== Buggy Calculator ===")
    
    # Test case 1: Empty list for average calculation
    empty_list = []
    print("Calculating average of empty list...")
    avg = calculate_average(empty_list)
    print(f"Average: {avg}")
    
    # Test case 2: Square root with typo
    print("\nCalculating square root of 16...")
    sqrt_result = get_square_root(16)
    print(f"Square root: {sqrt_result}")
    
    # Test case 3: Accessing invalid index
    sample_list = [1, 2, 3, 4, 5]
    print(f"\nAccessing element at index 10 from list: {sample_list}")
    element = access_list_element(sample_list, 10)
    print(f"Element: {element}")
    
    # Test case 4: Converting invalid type
    print("\nConverting dictionary to integer...")
    invalid_value = {"key": "value"}
    integer_result = convert_to_integer(invalid_value)
    print(f"Integer result: {integer_result}")

if __name__ == "__main__":
    main()
