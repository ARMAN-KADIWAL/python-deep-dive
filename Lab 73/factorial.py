def factorial(n):
    """
    Calculate the factorial of a number using recursion
    
    Args:
        n: A non-negative integer
        
    Returns:
        The factorial of n
        
    Raises:
        TypeError: If n is not an integer
        ValueError: If n is negative
    """
    # Type checking
    if not isinstance(n, int):
        raise TypeError("Factorial is only defined for integers")
    
    # Value checking
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    # Base cases
    if n == 0 or n == 1:
        return 1
    
    # Recursive case
    return n * factorial(n - 1)
