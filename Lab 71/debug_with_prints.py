# debug_with_prints.py - Calculator with debug print statements
import math

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    print(f"DEBUG: calculate_average called with: {numbers}")
    print(f"DEBUG: Length of numbers list: {len(numbers)}")
    
    if len(numbers) == 0:
        print("DEBUG: Empty list detected, returning 0")
        return 0
    
    total = 0
    for num in numbers:
        print(f"DEBUG: Adding {num} to total. Current total: {total}")
        total += num
    
    print(f"DEBUG: Final total: {total}")
    average = total / len(numbers)
    print(f"DEBUG: Calculated average: {average}")
    return average

def get_square_root(number):
    """Get the square root of a number"""
    print(f"DEBUG: get_square_root called with: {number}")
    print(f"DEBUG: Checking if {number} < 0")
    
    # Fixed the typo: numbr -> number
    if number < 0:
        print("DEBUG: Negative number detected")
        return "Cannot calculate square root of negative number"
    
    result = math.sqrt(number)
    print(f"DEBUG: Square root calculated: {result}")
    return result

def access_list_element(data_list, index):
    """Access an element from a list by index"""
    print(f"DEBUG: access_list_element called with list: {data_list}")
    print(f"DEBUG: Requested index: {index}")
    print(f"DEBUG: List length: {len(data_list)}")
    print(f"DEBUG: Valid index range: 0 to {len(data_list)-1}")
    
    if index >= len(data_list) or index < 0:
        print("DEBUG: Index out of range detected")
        return "Index out of range"
    
    element = data_list[index]
    print(f"DEBUG: Retrieved element: {element}")
    return element

def convert_to_integer(value):
    """Convert a value to integer"""
    print(f"DEBUG: convert_to_integer called with: {value}")
    print(f"DEBUG: Type of value: {type(value)}")
    
    try:
        result = int(value)
        print(f"DEBUG: Conversion successful: {result}")
        return result
    except (TypeError, ValueError) as e:
        print(f"DEBUG: Conversion failed: {e}")
        return f"Cannot convert {type(value).__name__} to integer"

def main():
    print("=== Calculator with Debug Prints ===")
    
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
    
    # Test case 3: Accessing valid and invalid indices
    print("\n--- Test Case 3: List Access ---")
    sample_list = [1, 2, 3, 4, 5]
    print(f"Accessing element at index 2 from list: {sample_list}")
    element = access_list_element(sample_list, 2)
    print(f"Element: {element}")
    
    print(f"\nAccessing element at index 10 from list: {sample_list}")
    element = access_list_element(sample_list, 10)
    print(f"Element: {element}")
    
    # Test case 4: Type conversion
    print("\n--- Test Case 4: Type Conversion ---")
    print("Converting string '42' to integer...")
    valid_conversion = convert_to_integer("42")
    print(f"Integer result: {valid_conversion}")
    
    print("\nConverting dictionary to integer...")
    invalid_value = {"key": "value"}
    integer_result = convert_to_integer(invalid_value)
    print(f"Integer result: {integer_result}")

if __name__ == "__main__":
    main()
