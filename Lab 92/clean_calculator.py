# Clean Calculator - After Refactoring Step 1
import math

def add_numbers(first_number, second_number, third_number=0):
    """Add two or three numbers together."""
    result = first_number + second_number
    if third_number != 0:
        result += third_number
    return result

def subtract_numbers(first_number, second_number, third_number=0):
    """Subtract second and third numbers from the first number."""
    result = first_number - second_number
    if third_number != 0:
        result -= third_number
    return result

def multiply_numbers(first_number, second_number, third_number=0):
    """Multiply two or three numbers together."""
    result = first_number * second_number
    if third_number != 0:
        result *= third_number
    return result

def divide_numbers(first_number, second_number, third_number=0):
    """Divide first number by second and optionally by third number."""
    if second_number == 0:
        return "Error: Division by zero"
    
    result = first_number / second_number
    
    if third_number != 0:
        if third_number == 0:  # This check is redundant - we'll fix it later
            return "Error: Division by zero"
        result /= third_number
    
    return result

def calculate_power(base, exponent, second_exponent=0):
    """Calculate power of a number, optionally raised to another power."""
    result = base ** exponent
    if second_exponent != 0:
        result = result ** second_exponent
    return result

def calculate_square_root(number):
    """Calculate square root of a number."""
    if number < 0:
        return "Error: Cannot calculate square root of negative number"
    return math.sqrt(number)

def perform_calculation(first_number, second_number, third_number, operation):
    """Main calculation dispatcher function."""
    operation_map = {
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
    
    if operation in operation_map:
        return operation_map[operation](first_number, second_number, third_number)
    else:
        return "Error: Unknown operation"


def calculate_sum(numbers):
    """Calculate the sum of a list of numbers."""
    total = 0
    for number in numbers:
        total += number
    return total

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if len(numbers) == 0:
        return 0
    return calculate_sum(numbers) / len(numbers)

def find_maximum(numbers):
    """Find the maximum value in a list of numbers."""
    if len(numbers) == 0:
        return None
    
    max_value = numbers[0]
    for number in numbers:
        if number > max_value:
            max_value = number
    return max_value

def find_minimum(numbers):
    """Find the minimum value in a list of numbers."""
    if len(numbers) == 0:
        return None
    
    min_value = numbers[0]
    for number in numbers:
        if number < min_value:
            min_value = number
    return min_value

def process_number_data(data):
    """Process a list of numbers and display statistics."""
    total = calculate_sum(data)
    average = calculate_average(data)
    maximum = find_maximum(data)
    minimum = find_minimum(data)
    
    print("Total:", total)
    print("Average:", average)
    print("Maximum:", maximum)
    print("Minimum:", minimum)

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
