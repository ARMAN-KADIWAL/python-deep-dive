#!/usr/bin/env python3
"""
Demonstration of TDD-developed sorting functions
"""

from sorting import sort_numbers, sort_numbers_desc, flexible_sort

def demonstrate_sorting():
    """Demonstrate all sorting functions"""
    
    print("=== TDD Sorting Functions Demonstration ===\n")
    
    # Test data
    test_data = [64, 34, 25, 12, 22, 11, 90, -5, 0, 88]
    print(f"Original list: {test_data}")
    print()
    
    # Ascending sort
    ascending_result = sort_numbers(test_data)
    print(f"Ascending sort: {ascending_result}")
    
    # Descending sort
    descending_result = sort_numbers_desc(test_data)
    print(f"Descending sort: {descending_result}")
    
    # Flexible sort - ascending
    flexible_asc = flexible_sort(test_data, ascending=True)
    print(f"Flexible sort (ascending): {flexible_asc}")
    
    # Flexible sort - descending
    flexible_desc = flexible_sort(test_data, ascending=False)
    print(f"Flexible sort (descending): {flexible_desc}")
    
    print()
    print("=== Edge Cases ===")
    
    # Empty list
    empty_result = sort_numbers([])
    print(f"Empty list: {empty_result}")
    
    # Single element
    single_result = sort_numbers([42])
    print(f"Single element: {single_result}")
    
    # Already sorted
    sorted_input = [1, 2, 3, 4, 5]
    already_sorted = sort_numbers(sorted_input)
    print(f"Already sorted: {already_sorted}")
    
    # Verify original list unchanged
    print(f"Original test data unchanged: {test_data}")
    
    print("\n=== All demonstrations completed successfully! ===")

if __name__ == '__main__':
    demonstrate_sorting()
