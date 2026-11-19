def sort_numbers(numbers):
    """
    Sort a list of numbers in ascending order.
    
    Args:
        numbers (list): List of numbers to sort
        
    Returns:
        list: New sorted list of numbers (original list unchanged)
        
    Raises:
        TypeError: If input is not a list or contains non-numeric values
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    # Check if all elements are numbers
    for item in numbers:
        if not isinstance(item, (int, float)):
            raise TypeError(f"All elements must be numbers, found: {type(item).__name__}")
    
    # Handle empty list
    if not numbers:
        return []
    
    # Create a copy to avoid modifying the original list
    sorted_list = numbers.copy()
    sorted_list.sort()
    return sorted_list


def sort_numbers_desc(numbers):
    """
    Sort a list of numbers in descending order.
    
    Args:
        numbers (list): List of numbers to sort
        
    Returns:
        list: New sorted list of numbers in descending order
        
    Raises:
        TypeError: If input is not a list or contains non-numeric values
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    # Check if all elements are numbers
    for item in numbers:
        if not isinstance(item, (int, float)):
            raise TypeError(f"All elements must be numbers, found: {type(item).__name__}")
    
    # Handle empty list
    if not numbers:
        return []
    
    # Create a copy and sort in descending order
    sorted_list = numbers.copy()
    sorted_list.sort(reverse=True)
    return sorted_list


def flexible_sort(numbers, ascending=True):
    """
    Sort a list of numbers in ascending or descending order.
    
    Args:
        numbers (list): List of numbers to sort
        ascending (bool): True for ascending order, False for descending
        
    Returns:
        list: New sorted list of numbers
        
    Raises:
        TypeError: If input is not a list or contains non-numeric values
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    # Check if all elements are numbers
    for item in numbers:
        if not isinstance(item, (int, float)):
            raise TypeError(f"All elements must be numbers, found: {type(item).__name__}")
    
    # Handle empty list
    if not numbers:
        return []
    
    # Create a copy and sort based on the ascending parameter
    sorted_list = numbers.copy()
    sorted_list.sort(reverse=not ascending)
    return sorted_list
