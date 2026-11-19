# Lab 74: Full TDD Cycle - Developing with Test-Driven Development

## Objectives

By the end of this lab, students will be able to:

- Understand and apply the Red-Green-Refactor cycle of Test-Driven Development (TDD)
- Write comprehensive unit tests before implementing functionality
- Develop a sorting algorithm using TDD principles
- Implement edge case testing and handle various input scenarios
- Refactor code while maintaining test coverage
- Add new features using the TDD approach
- Use Python's unittest framework for test automation

## Prerequisites

Before starting this lab, students should have:

- Basic knowledge of Python programming (variables, functions, lists, loops)
- Understanding of basic sorting concepts
- Familiarity with command-line operations
- Basic understanding of software testing concepts

## Ready-to-Use Cloud Machines

Al Nafi provides Linux-based cloud machines with Python pre-installed. Simply click **Start Lab** to access your development environment. No need to build your own virtual machine or install additional software.

## Lab Environment Setup

### Step 1: Access Your Cloud Machine

1. Click the **Start Lab** button to launch your Linux-based cloud machine
2. Wait for the machine to initialize (approximately 30-60 seconds)
3. Open the terminal application

### Step 2: Verify Python Installation

```bash
python3 --version

```

Expected output should show Python 3.x.x

### Step 3: Create Lab Directory

```bash
mkdir ~/tdd_sorting_lab
cd ~/tdd_sorting_lab

```

## Task 1: Write Initial Tests for a Simple Sorting Function

### Understanding TDD Cycle

Test-Driven Development follows the **Red-Green-Refactor** cycle:

- **Red**: Write a failing test
- **Green**: Write minimal code to make the test pass
- **Refactor**: Improve the code while keeping tests passing

### Step 1.1: Create Test File

Create a test file for our sorting function:

```bash
touch test_sorting.py

```

### Step 1.2: Write Initial Test Cases

Open the test file and add the following content:

```bash
nano test_sorting.py

```

Add the following code:

```python
import unittest
from sorting import sort_numbers

class TestSortNumbers(unittest.TestCase):
    
    def test_sort_basic_list(self):
        """Test sorting a basic list of numbers"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [1, 1, 2, 3, 4, 5, 6, 9]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_single_element(self):
        """Test sorting a list with single element"""
        input_list = [42]
        expected = [42]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_two_elements(self):
        """Test sorting a list with two elements"""
        input_list = [5, 2]
        expected = [2, 5]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 1.3: Run Initial Tests (Red Phase)

```bash
python3 test_sorting.py

```

Expected output: Tests will fail because we haven't created the sorting module yet. This is the **Red** phase of TDD.

## Task 2: Write Minimal Sorting Function to Pass Tests

### Step 2.1: Create Sorting Module

```bash
touch sorting.py

```

### Step 2.2: Implement Minimal Sorting Function (Green Phase)

```bash
nano sorting.py

```

Add the following minimal implementation:

```python
def sort_numbers(numbers):
    """
    Sort a list of numbers in ascending order.
    
    Args:
        numbers (list): List of numbers to sort
        
    Returns:
        list: Sorted list of numbers
    """
    if not numbers:
        return []
    
    # Simple implementation using Python's built-in sort
    sorted_list = numbers.copy()
    sorted_list.sort()
    return sorted_list

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 2.3: Run Tests Again (Green Phase)

```bash
python3 test_sorting.py

```

Expected output: All tests should now pass. This completes the **Green** phase.

### Step 2.4: Verify Test Results

```bash
python3 -m unittest test_sorting.py -v

```

This will show detailed test results with verbose output.

## Task 3: Refactor and Add Edge Case Tests

### Step 3.1: Add Edge Case Tests

Edit the test file to include more comprehensive test cases:

```bash
nano test_sorting.py

```

Add the following test methods to the TestSortNumbers class:

```python
    def test_sort_empty_list(self):
        """Test sorting an empty list"""
        input_list = []
        expected = []
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_already_sorted(self):
        """Test sorting an already sorted list"""
        input_list = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_reverse_sorted(self):
        """Test sorting a reverse sorted list"""
        input_list = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_with_duplicates(self):
        """Test sorting a list with duplicate values"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_with_negative_numbers(self):
        """Test sorting a list with negative numbers"""
        input_list = [-3, 1, -4, 0, 5, -2]
        expected = [-4, -3, -2, 0, 1, 5]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_original_list_unchanged(self):
        """Test that the original list is not modified"""
        input_list = [3, 1, 4, 1, 5]
        original_copy = input_list.copy()
        sort_numbers(input_list)
        self.assertEqual(input_list, original_copy)

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 3.2: Run Extended Tests

```bash
python3 test_sorting.py -v

```

All tests should pass. If any fail, update the sorting function accordingly.

### Step 3.3: Refactor Sorting Function (Refactor Phase)

Let's improve our sorting function with better documentation and error handling:

```bash
nano sorting.py

```

Update the function:

```python
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

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 3.4: Add Tests for Error Handling

Add these test methods to your test file:

```bash
nano test_sorting.py

```

Add at the end of the TestSortNumbers class:

```python
    def test_sort_non_list_input(self):
        """Test that non-list input raises TypeError"""
        with self.assertRaises(TypeError):
            sort_numbers("not a list")
    
    def test_sort_non_numeric_elements(self):
        """Test that non-numeric elements raise TypeError"""
        with self.assertRaises(TypeError):
            sort_numbers([1, 2, "three", 4])

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 3.5: Run All Tests

```bash
python3 test_sorting.py -v

```

## Task 4: Implement Descending Order Feature Using TDD

### Step 4.1: Write Tests for Descending Order (Red Phase)

Create a new test file for the enhanced sorting functionality:

```bash
touch test_advanced_sorting.py

```

```bash
nano test_advanced_sorting.py

```

Add the following content:

```python
import unittest
from sorting import sort_numbers, sort_numbers_desc

class TestAdvancedSorting(unittest.TestCase):
    
    def test_sort_descending_basic(self):
        """Test sorting in descending order"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [9, 6, 5, 4, 3, 2, 1, 1]
        result = sort_numbers_desc(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_descending_empty(self):
        """Test sorting empty list in descending order"""
        input_list = []
        expected = []
        result = sort_numbers_desc(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_descending_single(self):
        """Test sorting single element in descending order"""
        input_list = [42]
        expected = [42]
        result = sort_numbers_desc(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_descending_with_negatives(self):
        """Test sorting with negative numbers in descending order"""
        input_list = [-3, 1, -4, 0, 5, -2]
        expected = [5, 1, 0, -2, -3, -4]
        result = sort_numbers_desc(input_list)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 4.2: Run New Tests (Red Phase)

```bash
python3 test_advanced_sorting.py

```

Tests will fail because the sort_numbers_desc function doesn't exist yet.

### Step 4.3: Implement Descending Sort Function (Green Phase)

```bash
nano sorting.py

```

Add the new function to the existing file:

```python
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

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 4.4: Run Tests Again (Green Phase)

```bash
python3 test_advanced_sorting.py -v

```

All tests should now pass.

## Task 5: Add Flexible Sorting Function with More Tests

### Step 5.1: Write Tests for Flexible Sorting Function

```bash
nano test_advanced_sorting.py

```

Add these test methods to the TestAdvancedSorting class:

```python
    def test_flexible_sort_ascending(self):
        """Test flexible sort function with ascending order"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [1, 1, 2, 3, 4, 5, 6, 9]
        result = flexible_sort(input_list, ascending=True)
        self.assertEqual(result, expected)
    
    def test_flexible_sort_descending(self):
        """Test flexible sort function with descending order"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [9, 6, 5, 4, 3, 2, 1, 1]
        result = flexible_sort(input_list, ascending=False)
        self.assertEqual(result, expected)
    
    def test_flexible_sort_default_ascending(self):
        """Test flexible sort function with default ascending order"""
        input_list = [3, 1, 4, 1, 5]
        expected = [1, 1, 3, 4, 5]
        result = flexible_sort(input_list)
        self.assertEqual(result, expected)

```

Add the import at the top of the file:

```python
from sorting import sort_numbers, sort_numbers_desc, flexible_sort

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 5.2: Implement Flexible Sort Function

```bash
nano sorting.py

```

Add the flexible_sort function:

```python
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

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 5.3: Run All Advanced Tests

```bash
python3 test_advanced_sorting.py -v

```

### Step 5.4: Run All Tests Together

Create a test runner to execute all tests:

```bash
touch run_all_tests.py

```

```bash
nano run_all_tests.py

```

Add the following content:

```python
import unittest
import sys

# Import test modules
import test_sorting
import test_advanced_sorting

def run_all_tests():
    """Run all test suites"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromModule(test_sorting))
    suite.addTests(loader.loadTestsFromModule(test_advanced_sorting))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 5.5: Execute All Tests

```bash
python3 run_all_tests.py

```

## Task 6: Performance Testing and Final Validation

### Step 6.1: Create Performance Tests

```bash
touch test_performance.py

```

```bash
nano test_performance.py

```

Add performance testing code:

```python
import unittest
import time
import random
from sorting import sort_numbers, sort_numbers_desc, flexible_sort

class TestSortingPerformance(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.small_list = [random.randint(1, 100) for _ in range(100)]
        self.medium_list = [random.randint(1, 1000) for _ in range(1000)]
        self.large_list = [random.randint(1, 10000) for _ in range(10000)]
    
    def test_small_list_performance(self):
        """Test performance with small list"""
        start_time = time.time()
        result = sort_numbers(self.small_list)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)  # Should complete in less than 1 second
        self.assertEqual(len(result), len(self.small_list))
    
    def test_medium_list_performance(self):
        """Test performance with medium list"""
        start_time = time.time()
        result = flexible_sort(self.medium_list)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertLess(execution_time, 2.0)  # Should complete in less than 2 seconds
        self.assertEqual(len(result), len(self.medium_list))
    
    def test_correctness_with_large_dataset(self):
        """Test correctness with large dataset"""
        result = sort_numbers(self.large_list)
        
        # Verify the result is actually sorted
        for i in range(1, len(result)):
            self.assertLessEqual(result[i-1], result[i])
        
        # Verify all elements are preserved
        self.assertEqual(len(result), len(self.large_list))
        self.assertEqual(sorted(self.large_list), result)

if __name__ == '__main__':
    unittest.main()

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 6.2: Run Performance Tests

```bash
python3 test_performance.py -v

```

### Step 6.3: Create Comprehensive Test Demo

```bash
touch demo_sorting.py

```

```bash
nano demo_sorting.py

```

Add demonstration code:

```python
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

```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 6.4: Run Demonstration

```bash
python3 demo_sorting.py

```

### Step 6.5: Final Test Suite Execution

```bash
python3 run_all_tests.py

```

## Troubleshooting Common Issues

### Issue 1: Import Errors

If you encounter import errors, ensure all files are in the same directory:

```bash
ls -la

```

You should see all Python files in the current directory.

### Issue 2: Test Failures

If tests fail unexpectedly, check:

1. Function names match exactly between test files and implementation
2. Return types are correct (lists, not other types)
3. Edge cases are handled properly

### Issue 3: Performance Issues

If performance tests fail:

1. The test environment might be slower than expected
2. Adjust time limits in performance tests if necessary
3. Ensure no infinite loops in sorting logic

### Issue 4: Python Version Issues

Ensure you're using Python 3:

```bash
python3 --version

```

If python3 is not available, try:

```bash
python --version

```

## Verification and Testing

### Final Verification Steps

1. **Run all tests one final time:**

```bash
python3 run_all_tests.py

```

2. **Check code coverage by running individual test suites:**

```bash
python3 test_sorting.py -v
python3 test_advanced_sorting.py -v
python3 test_performance.py -v

```

3. **Verify the demonstration works:**

```bash
python3 demo_sorting.py

```

### Expected Results

- All unit tests should pass
- Performance tests should complete within time limits
- Demonstration should show correct sorting behavior
- Original lists should remain unchanged after sorting

## Conclusion

Congratulations! You have successfully completed a full Test-Driven Development cycle. In this lab, you have:

**Mastered TDD Fundamentals:**

- Applied the Red-Green-Refactor cycle throughout the development process
- Learned to write tests before implementing functionality
- Experienced how TDD guides better software design

**Developed Comprehensive Testing Skills:**

- Created unit tests for basic functionality
- Implemented edge case testing for robust code
- Added performance testing to ensure efficiency
- Learned error handling and input validation

**Built a Complete Sorting Solution:**

- Implemented multiple sorting functions using TDD principles
- Created flexible, reusable code with proper documentation
- Ensured code quality through continuous testing

**Key Benefits of TDD You've Experienced:**

- **Better Code Quality**: Tests caught issues early in development
- **Improved Design**: Writing tests first led to cleaner, more modular code
- **Confidence in Changes**: Refactoring was safe because tests verified functionality
- **Documentation**: Tests serve as living documentation of expected behavior

**Real-World Applications:** This TDD approach is used in professional software development to:

- Reduce bugs in production systems
- Enable safe code refactoring and feature additions
- Improve team collaboration through clear specifications
- Maintain high code quality in large projects

The skills you've learned in this lab are directly applicable to any software development project, making you a more effective and confident programmer. TDD is particularly valuable in team environments where code reliability and maintainability are crucial.

Remember: **Red-Green-Refactor** is not just a development technique—it's a mindset that leads to better software engineering practices throughout your career.
