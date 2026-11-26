"""Practice functions for the enhanced Python REPL."""
import pdb


def greet(name):
    return f"Hello, {name}!"


def calculate_area(length, width):
    if length <= 0 or width <= 0:
        return "Invalid dimensions"
    return f"Area: {length * width} square units"


def factorial_bug(n):
    result = 1
    for i in range(1, n):
        result *= i
    return result


def calculate_factorial(n):
    if n < 0:
        raise ValueError("Expected a non-negative integer")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def process_list(numbers):
    total = 0
    for num in numbers:
        if num > 0:
            total += num
        else:
            total -= abs(num)
    return total


def analyze_data(data_list, debug=False):
    if debug:
        pdb.set_trace()
    filtered_data = [x for x in data_list if x > 10]
    average = sum(filtered_data) / len(filtered_data) if filtered_data else 0
    return {
        "average": average,
        "maximum": max(filtered_data) if filtered_data else 0,
        "minimum": min(filtered_data) if filtered_data else 0,
        "count": len(filtered_data),
    }


def find_errors(data, debug=False):
    errors = []
    for i, value in enumerate(data):
        if value < 0:
            if debug:
                pdb.set_trace()
            errors.append(f"Negative value {value} at index {i}")
        elif value > 100:
            errors.append(f"Value too large: {value} at index {i}")
    return errors
