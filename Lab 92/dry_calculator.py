# DRY Calculator - Eliminating Code Duplication
import math

def apply_operation_with_optional_third(first_number, second_number, third_number, operation_func):
    """Apply an operation to two numbers, optionally including a third number."""
    result = operation_func(first_number, second_number)
    if third_number != 0:
        result = operation_func(result, third_number)
    return result

def safe_divide(dividend, divisor):
    """Safely divide two numbers, checking for division by zero."""
    if divisor == 0:
        raise ValueError("Division by zero")
    return dividend / divisor

def add_numbers(first_number, second_number, third_number=0):
    """Add two or three numbers together."""
    return apply_operation_with_optional_third(first_number, second_number, third_number, lambda x, y: x + y)

def subtract_numbers(first_number, second_number, third_number=0):
    """Subtract second and third numbers from the first number."""
    return apply_operation_with_optional_third(first_number, second_number, third_number, lambda x, y: x - y)

def multiply_numbers(first_number, second_number, third_number=0):
    """Multiply two or three numbers together."""
    return apply_operation_with_optional_third(first_number, second_number, third_number, lambda x, y: x * y)

def divide_numbers(first_number, second_number, third_number=0):
    """Divide first number by second and optionally by third number."""
    try:
        return apply_operation_with_optional_third(first_number, second_number, third_number, safe_divide)
    except ValueError as error:
        return f"Error: {error}"

def calculate_power(base, exponent, second_exponent=0):
    """Calculate power of a number, optionally raised to another power."""
    return apply_operation_with_optional_third(base, exponent, second_exponent, lambda x, y: x ** y)

def calculate_square_root(number):
    """Calculate square root of a number."""
    if number < 0:
        return "Error: Cannot calculate square root of negative number"
    return math.sqrt(number)

def get_operation_function(operation):
    """Return the appropriate function for the given operation."""
    operation_functions = {
        "add": add_numbers,
        "subtract": subtract_numbers,
        "sub": subtract_numbers,
        "multiply": multiply_numbers,
        "mul": multiply_numbers,
        "divide": divide_numbers,
        "div": divide_numbers,
        "power": calculate_power,
        "sqrt": lambda x, y, z: calculate_square_root(x)
    }
    return operation_functions.get(operation)

def perform_calculation(first_number, second_number, third_number, operation):
    """Perform the specified calculation."""
    operation_function = get_operation_function(operation)
    
    if operation_function is None:
        return "Error: Unknown operation"
    
    return operation_function(first_number, second_number, third_number)

def find_extreme_value(numbers, comparison_func):
    """Find extreme value (min or max) using a comparison function."""
    if len(numbers) == 0:
        return None
    
    extreme_value = numbers[0]
    for number in numbers:
        if comparison_func(number, extreme_value):
            extreme_value = number
    return extreme_value

def calculate_sum(numbers):
    """Calculate the sum of a list of numbers."""
    return sum(numbers)  # Using built-in sum function

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if len(numbers) == 0:
        return 0
    return calculate_sum(numbers) / len(numbers)

def find_maximum(numbers):
    """Find the maximum value in a list of numbers."""
    return find_extreme_value(numbers, lambda current, extreme: current > extreme)

def find_minimum(numbers):
    """Find the minimum value in a list of numbers."""
    return find_extreme_value(numbers, lambda current, extreme: current < extreme)

def calculate_statistics(data):
    """Calculate and return statistics for a list of numbers."""
    return {
        'total': calculate_sum(data),
        'average': calculate_average(data),
        'maximum': find_maximum(data),
        'minimum': find_minimum(data)
    }

def display_statistics(statistics):
    """Display statistics in a formatted way."""
    for stat_name, stat_value in statistics.items():
        print(f"{stat_name.capitalize()}: {stat_value}")

def process_number_data(data):
    """Process a list of numbers and display statistics."""
    statistics = calculate_statistics(data)
    display_statistics(statistics)

def main():
    print("Calculator Results:")
    print(perform_calculation(10, 5, 2, "add"))
    print(perform_calculation(10, 5, 2, "multiply"))
    print(perform_calculation(16, 0, 0, "sqrt"))
    print(perform_calculation(10, 0, 0, "divide"))
    
    print("\nData Processing Results:")
    sample_data = [10, 20, 30, 40, 50]
    process_number_data(sample_data)

if __name__ == "__main__":
    main()
