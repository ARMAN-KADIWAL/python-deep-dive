"""
Arithmetic Operations Module - Refactored Version
This module contains enhanced arithmetic functions with improved error handling.
"""

def add(*args):
    """
    Add multiple numbers and return the result.
    
    Args:
        *args: Variable number of numeric arguments
    
    Returns:
        int/float: Sum of all arguments
        
    Raises:
        TypeError: If any argument is not a number
    """
    if not args:
        return 0
    
    result = 0
    for num in args:
        if not isinstance(num, (int, float)):
            raise TypeError(f"All arguments must be numbers, got {type(num).__name__}")
        result += num
    return result

def subtract(a, b):
    """
    Subtract second number from first number and return the result.
    Enhanced with type checking.
    
    Args:
        a (int/float): First number
        b (int/float): Second number
    
    Returns:
        int/float: Difference of a and b
        
    Raises:
        TypeError: If arguments are not numbers
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a - b

def multiply(*args):
    """
    Multiply multiple numbers and return the result.
    
    Args:
        *args: Variable number of numeric arguments
    
    Returns:
        int/float: Product of all arguments
        
    Raises:
        TypeError: If any argument is not a number
    """
    if not args:
        return 1
    
    result = 1
    for num in args:
        if not isinstance(num, (int, float)):
            raise TypeError(f"All arguments must be numbers, got {type(num).__name__}")
        result *= num
    return result

def divide(a, b, precision=None):
    """
    Divide first number by second number and return the result.
    Enhanced with precision control.
    
    Args:
        a (int/float): Dividend
        b (int/float): Divisor
        precision (int, optional): Number of decimal places to round to
    
    Returns:
        float: Quotient of a divided by b
    
    Raises:
        ValueError: If divisor is zero
        TypeError: If arguments are not numbers
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    
    if b == 0:
        raise ValueError("Cannot divide by zero")
    
    result = a / b
    
    if precision is not None:
        if not isinstance(precision, int) or precision < 0:
            raise ValueError("Precision must be a non-negative integer")
        result = round(result, precision)
    
    return result

def power(a, b):
    """
    Calculate a raised to the power of b.
    Enhanced with type checking.
    
    Args:
        a (int/float): Base number
        b (int/float): Exponent
    
    Returns:
        int/float: Result of a^b
        
    Raises:
        TypeError: If arguments are not numbers
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a ** b


def factorial(n):
    """
    Calculate the factorial of a non-negative integer.
    
    Args:
        n (int): Non-negative integer
    
    Returns:
        int: Factorial of n
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    if not isinstance(n, int):
        raise TypeError("Argument must be an integer")
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result
