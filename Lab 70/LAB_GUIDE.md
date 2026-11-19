# Lab 70: Writing Unit Tests with unittest - Introduction to Unit Testing

## Objectives

By the end of this lab, students will be able to:

- Understand the fundamental concepts of unit testing and its importance in software development
- Create simple Python functions for basic arithmetic operations
- Write comprehensive test cases using Python's built-in **unittest** framework
- Utilize **assertEqual()** and other assertion methods to validate function outputs
- Execute unit tests and interpret test results effectively
- Apply refactoring techniques while maintaining test integrity
- Implement test-driven development practices in Python projects

## Prerequisites

Before starting this lab, students should have:

- Basic knowledge of Python programming language
- Understanding of Python functions and return statements
- Familiarity with Python data types (integers, floats, strings)
- Basic command-line navigation skills
- Python 3.6 or higher installed (provided in the cloud environment)

## Ready-to-Use Cloud Machines

Al Nafi provides pre-configured Linux-based cloud machines with all necessary tools installed. Simply click **Start Lab** to access your development environment. No need to build your own virtual machine or install additional software.

Your cloud machine includes:

- Python 3.8+ with unittest framework
- Text editor (nano, vim)
- Terminal access
- All required dependencies pre-installed

## Lab Tasks

### Task 1: Create Basic Arithmetic Functions

#### Subtask 1.1: Set Up the Project Structure

First, let's create a proper directory structure for our unit testing project.

1. Open the terminal in your cloud machine
2. Create a new directory for the project:

```bash
mkdir unit_testing_lab
cd unit_testing_lab

```

3. Create the main Python file for our arithmetic functions:

```bash
touch arithmetic_operations.py

```

#### Subtask 1.2: Implement Arithmetic Functions

Now we'll create simple functions that perform basic mathematical operations.

1. Open the arithmetic_operations.py file using a text editor:

```bash
nano arithmetic_operations.py

```

2. Add the following code to create our arithmetic functions:

```python
"""
Arithmetic Operations Module
This module contains basic arithmetic functions for demonstration of unit testing.
"""

def add(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int/float): First number
        b (int/float): Second number
    
    Returns:
        int/float: Sum of a and b
    """
    return a + b

def subtract(a, b):
    """
    Subtract second number from first number and return the result.
    
    Args:
        a (int/float): First number
        b (int/float): Second number
    
    Returns:
        int/float: Difference of a and b
    """
    return a - b

def multiply(a, b):
    """
    Multiply two numbers and return the result.
    
    Args:
        a (int/float): First number
        b (int/float): Second number
    
    Returns:
        int/float: Product of a and b
    """
    return a * b

def divide(a, b):
    """
    Divide first number by second number and return the result.
    
    Args:
        a (int/float): Dividend
        b (int/float): Divisor
    
    Returns:
        float: Quotient of a divided by b
    
    Raises:
        ValueError: If divisor is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    """
    Calculate a raised to the power of b.
    
    Args:
        a (int/float): Base number
        b (int/float): Exponent
    
    Returns:
        int/float: Result of a^b
    """
    return a ** b

```

3. Save and exit the file (in nano: Ctrl+X, then Y, then Enter)

#### Subtask 1.3: Test the Functions Manually

Let's quickly verify our functions work correctly before writing formal tests.

1. Create a simple test script:

```bash
nano manual_test.py

```

2. Add the following code:

```python
from arithmetic_operations import add, subtract, multiply, divide, power

# Manual testing of our functions
print("Manual Testing Results:")
print(f"add(5, 3) = {add(5, 3)}")
print(f"subtract(10, 4) = {subtract(10, 4)}")
print(f"multiply(6, 7) = {multiply(6, 7)}")
print(f"divide(15, 3) = {divide(15, 3)}")
print(f"power(2, 3) = {power(2, 3)}")

```

3. Run the manual test:

```bash
python3 manual_test.py

```

Expected output:

```
Manual Testing Results:
add(5, 3) = 8
subtract(10, 4) = 6
multiply(6, 7) = 42
divide(15, 3) = 5.0
power(2, 3) = 8

```

### Task 2: Write Unit Tests Using unittest Framework

#### Subtask 2.1: Create the Test File

Now we'll create comprehensive unit tests for our arithmetic functions.

1. Create a new test file:

```bash
nano test_arithmetic_operations.py

```

2. Add the basic test structure:

```python
"""
Unit Tests for Arithmetic Operations Module
This module contains unit tests for testing arithmetic functions.
"""

import unittest
from arithmetic_operations import add, subtract, multiply, divide, power

class TestArithmeticOperations(unittest.TestCase):
    """Test case class for arithmetic operations"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        print(f"Running test: {self._testMethodName}")
    
    def tearDown(self):
        """Clean up after each test method."""
        print(f"Completed test: {self._testMethodName}")

if __name__ == '__main__':
    unittest.main()

```

#### Subtask 2.2: Write Test Cases for Addition Function

Add test methods for the addition function:

1. Edit the test file and add the following test methods inside the TestArithmeticOperations class:

```python
    def test_add_positive_numbers(self):
        """Test addition of positive numbers"""
        result = add(5, 3)
        self.assertEqual(result, 8)
        
    def test_add_negative_numbers(self):
        """Test addition of negative numbers"""
        result = add(-5, -3)
        self.assertEqual(result, -8)
        
    def test_add_positive_and_negative(self):
        """Test addition of positive and negative numbers"""
        result = add(10, -3)
        self.assertEqual(result, 7)
        
    def test_add_zero(self):
        """Test addition with zero"""
        result = add(5, 0)
        self.assertEqual(result, 5)
        
    def test_add_floats(self):
        """Test addition of floating point numbers"""
        result = add(2.5, 3.7)
        self.assertAlmostEqual(result, 6.2, places=1)

```

#### Subtask 2.3: Write Test Cases for Subtraction Function

Add test methods for the subtraction function:

```python
    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers"""
        result = subtract(10, 3)
        self.assertEqual(result, 7)
        
    def test_subtract_negative_numbers(self):
        """Test subtraction of negative numbers"""
        result = subtract(-5, -3)
        self.assertEqual(result, -2)
        
    def test_subtract_larger_from_smaller(self):
        """Test subtracting larger number from smaller"""
        result = subtract(3, 10)
        self.assertEqual(result, -7)
        
    def test_subtract_zero(self):
        """Test subtraction with zero"""
        result = subtract(5, 0)
        self.assertEqual(result, 5)
        
    def test_subtract_floats(self):
        """Test subtraction of floating point numbers"""
        result = subtract(5.8, 2.3)
        self.assertAlmostEqual(result, 3.5, places=1)

```

#### Subtask 2.4: Write Test Cases for Multiplication Function

Add test methods for the multiplication function:

```python
    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers"""
        result = multiply(4, 5)
        self.assertEqual(result, 20)
        
    def test_multiply_negative_numbers(self):
        """Test multiplication of negative numbers"""
        result = multiply(-3, -4)
        self.assertEqual(result, 12)
        
    def test_multiply_positive_and_negative(self):
        """Test multiplication of positive and negative numbers"""
        result = multiply(6, -2)
        self.assertEqual(result, -12)
        
    def test_multiply_by_zero(self):
        """Test multiplication by zero"""
        result = multiply(5, 0)
        self.assertEqual(result, 0)
        
    def test_multiply_by_one(self):
        """Test multiplication by one"""
        result = multiply(7, 1)
        self.assertEqual(result, 7)
        
    def test_multiply_floats(self):
        """Test multiplication of floating point numbers"""
        result = multiply(2.5, 4.0)
        self.assertEqual(result, 10.0)

```

#### Subtask 2.5: Write Test Cases for Division Function

Add test methods for the division function, including error handling:

```python
    def test_divide_positive_numbers(self):
        """Test division of positive numbers"""
        result = divide(15, 3)
        self.assertEqual(result, 5.0)
        
    def test_divide_negative_numbers(self):
        """Test division of negative numbers"""
        result = divide(-12, -4)
        self.assertEqual(result, 3.0)
        
    def test_divide_positive_and_negative(self):
        """Test division of positive and negative numbers"""
        result = divide(20, -4)
        self.assertEqual(result, -5.0)
        
    def test_divide_by_one(self):
        """Test division by one"""
        result = divide(8, 1)
        self.assertEqual(result, 8.0)
        
    def test_divide_floats(self):
        """Test division of floating point numbers"""
        result = divide(7.5, 2.5)
        self.assertEqual(result, 3.0)
        
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError"""
        with self.assertRaises(ValueError):
            divide(10, 0)
            
    def test_divide_by_zero_message(self):
        """Test division by zero error message"""
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            divide(5, 0)

```

#### Subtask 2.6: Write Test Cases for Power Function

Add test methods for the power function:

```python
    def test_power_positive_base_positive_exponent(self):
        """Test positive base with positive exponent"""
        result = power(2, 3)
        self.assertEqual(result, 8)
        
    def test_power_positive_base_zero_exponent(self):
        """Test positive base with zero exponent"""
        result = power(5, 0)
        self.assertEqual(result, 1)
        
    def test_power_positive_base_negative_exponent(self):
        """Test positive base with negative exponent"""
        result = power(2, -2)
        self.assertEqual(result, 0.25)
        
    def test_power_negative_base_even_exponent(self):
        """Test negative base with even exponent"""
        result = power(-3, 2)
        self.assertEqual(result, 9)
        
    def test_power_negative_base_odd_exponent(self):
        """Test negative base with odd exponent"""
        result = power(-2, 3)
        self.assertEqual(result, -8)
        
    def test_power_float_numbers(self):
        """Test power with floating point numbers"""
        result = power(2.5, 2)
        self.assertEqual(result, 6.25)

```

### Task 3: Run the Unit Tests

#### Subtask 3.1: Execute All Tests

Now let's run our comprehensive test suite to see the results.

1. Run all tests with verbose output:

```bash
python3 -m unittest test_arithmetic_operations.py -v

```

2. You should see output similar to:

```
test_add_floats (test_arithmetic_operations.TestArithmeticOperations) ... ok
test_add_negative_numbers (test_arithmetic_operations.TestArithmeticOperations) ... ok
test_add_positive_and_negative (test_arithmetic_operations.TestArithmeticOperations) ... ok
test_add_positive_numbers (test_arithmetic_operations.TestArithmeticOperations) ... ok
test_add_zero (test_arithmetic_operations.TestArithmeticOperations) ... ok
...
----------------------------------------------------------------------
Ran 23 tests in 0.001s

OK

```

#### Subtask 3.2: Run Specific Test Methods

You can also run specific test methods or test classes:

1. Run only addition tests:

```bash
python3 -m unittest test_arithmetic_operations.TestArithmeticOperations.test_add_positive_numbers -v

```

2. Run tests with different verbosity levels:

```bash
# Minimal output
python3 -m unittest test_arithmetic_operations.py

# Verbose output
python3 -m unittest test_arithmetic_operations.py -v

# Very verbose output with test discovery
python3 -m unittest discover -v

```

#### Subtask 3.3: Generate Test Coverage Report

Let's check how much of our code is covered by tests:

1. Install coverage tool (if not already available):

```bash
pip3 install coverage

```

2. Run tests with coverage:

```bash
coverage run -m unittest test_arithmetic_operations.py

```

3. Generate coverage report:

```bash
coverage report -m

```

4. Generate HTML coverage report:

```bash
coverage html

```

### Task 4: Understanding Test Results and Assertions

#### Subtask 4.1: Explore Different Assertion Methods

Let's create a separate file to demonstrate various assertion methods:

1. Create a new test file:

```bash
nano test_assertions_demo.py

```

2. Add comprehensive assertion examples:

```python
"""
Demonstration of various unittest assertion methods
"""

import unittest
from arithmetic_operations import add, divide

class TestAssertionMethods(unittest.TestCase):
    """Demonstrate different assertion methods"""
    
    def test_assertEqual_demo(self):
        """Demonstrate assertEqual"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual("hello", "hello")
        
    def test_assertNotEqual_demo(self):
        """Demonstrate assertNotEqual"""
        self.assertNotEqual(add(2, 3), 6)
        self.assertNotEqual("hello", "world")
        
    def test_assertTrue_demo(self):
        """Demonstrate assertTrue"""
        self.assertTrue(add(2, 3) > 0)
        self.assertTrue(isinstance(add(1, 2), int))
        
    def test_assertFalse_demo(self):
        """Demonstrate assertFalse"""
        self.assertFalse(add(2, 3) < 0)
        self.assertFalse(add(1, 1) == 3)
        
    def test_assertAlmostEqual_demo(self):
        """Demonstrate assertAlmostEqual for floating point comparisons"""
        result = divide(1, 3)
        self.assertAlmostEqual(result, 0.333333, places=5)
        
    def test_assertGreater_demo(self):
        """Demonstrate assertGreater and assertLess"""
        self.assertGreater(add(5, 3), 7)
        self.assertLess(add(2, 1), 5)
        
    def test_assertIn_demo(self):
        """Demonstrate assertIn and assertNotIn"""
        result_str = str(add(2, 3))
        self.assertIn('5', result_str)
        self.assertNotIn('6', result_str)
        
    def test_assertIsInstance_demo(self):
        """Demonstrate assertIsInstance"""
        result = add(2, 3)
        self.assertIsInstance(result, int)
        
        float_result = divide(5, 2)
        self.assertIsInstance(float_result, float)

if __name__ == '__main__':
    unittest.main()

```

3. Run the assertion demonstration:

```bash
python3 -m unittest test_assertions_demo.py -v

```

### Task 5: Refactor Functions and Maintain Test Integrity

#### Subtask 5.1: Refactor the Arithmetic Functions

Now we'll improve our original functions while ensuring tests still pass.

1. Create a backup of the original file:

```bash
cp arithmetic_operations.py arithmetic_operations_backup.py

```

2. Edit the arithmetic_operations.py file to add improvements:

```bash
nano arithmetic_operations.py

```

3. Replace the content with the refactored version:

```python
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

```

#### Subtask 5.2: Update Tests for Refactored Functions

Now we need to update our tests to work with the refactored functions:

1. Create an updated test file:

```bash
nano test_arithmetic_operations_refactored.py

```

2. Add updated tests that work with the new function signatures:

```python
"""
Unit Tests for Refactored Arithmetic Operations Module
"""

import unittest
from arithmetic_operations import add, subtract, multiply, divide, power

class TestRefactoredArithmeticOperations(unittest.TestCase):
    """Test case class for refactored arithmetic operations"""
    
    # Updated tests for add function (now supports multiple arguments)
    def test_add_two_positive_numbers(self):
        """Test addition of two positive numbers"""
        result = add(5, 3)
        self.assertEqual(result, 8)
        
    def test_add_multiple_numbers(self):
        """Test addition of multiple numbers"""
        result = add(1, 2, 3, 4, 5)
        self.assertEqual(result, 15)
        
    def test_add_no_arguments(self):
        """Test addition with no arguments"""
        result = add()
        self.assertEqual(result, 0)
        
    def test_add_single_argument(self):
        """Test addition with single argument"""
        result = add(7)
        self.assertEqual(result, 7)
        
    def test_add_type_error(self):
        """Test addition with invalid type"""
        with self.assertRaises(TypeError):
            add(5, "hello")
    
    # Updated tests for multiply function (now supports multiple arguments)
    def test_multiply_two_numbers(self):
        """Test multiplication of two numbers"""
        result = multiply(4, 5)
        self.assertEqual(result, 20)
        
    def test_multiply_multiple_numbers(self):
        """Test multiplication of multiple numbers"""
        result = multiply(2, 3, 4)
        self.assertEqual(result, 24)
        
    def test_multiply_no_arguments(self):
        """Test multiplication with no arguments"""
        result = multiply()
        self.assertEqual(result, 1)
        
    def test_multiply_type_error(self):
        """Test multiplication with invalid type"""
        with self.assertRaises(TypeError):
            multiply(5, "hello")
    
    # Updated tests for divide function (now supports precision)
    def test_divide_with_precision(self):
        """Test division with precision control"""
        result = divide(10, 3, precision=2)
        self.assertEqual(result, 3.33)
        
    def test_divide_type_error(self):
        """Test division with invalid types"""
        with self.assertRaises(TypeError):
            divide("10", 2)
            
    def test_divide_invalid_precision(self):
        """Test division with invalid precision"""
        with self.assertRaises(ValueError):
            divide(10, 2, precision=-1)
    
    # Tests for enhanced type checking
    def test_subtract_type_error(self):
        """Test subtraction with invalid types"""
        with self.assertRaises(TypeError):
            subtract(5, "hello")
            
    def test_power_type_error(self):
        """Test power with invalid types"""
        with self.assertRaises(TypeError):
            power("2", 3)

if __name__ == '__main__':
    unittest.main()

```

#### Subtask 5.3: Run Tests on Refactored Code

1. Run the updated tests:

```bash
python3 -m unittest test_arithmetic_operations_refactored.py -v

```

2. Run both old and new tests to see compatibility:

```bash
# This might show some failures due to function signature changes
python3 -m unittest test_arithmetic_operations.py -v

# This should pass with the refactored functions
python3 -m unittest test_arithmetic_operations_refactored.py -v

```

### Task 6: Advanced Testing Techniques

#### Subtask 6.1: Create Test Suites

Let's organize our tests into test suites for better management:

1. Create a test suite file:

```bash
nano test_suite.py

```

2. Add the following code:

```python
"""
Test Suite for Arithmetic Operations
Demonstrates how to organize and run multiple test classes
"""

import unittest
from test_arithmetic_operations_refactored import TestRefactoredArithmeticOperations
from test_assertions_demo import TestAssertionMethods

def create_test_suite():
    """Create a test suite containing all test cases"""
    suite = unittest.TestSuite()
    
    # Add specific test methods
    suite.addTest(TestRefactoredArithmeticOperations('test_add_two_positive_numbers'))
    suite.addTest(TestRefactoredArithmeticOperations('test_multiply_multiple_numbers'))
    suite.addTest(TestRefactoredArithmeticOperations('test_divide_with_precision'))
    
    # Add all tests from a test class
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAssertionMethods))
    
    return suite

def create_addition_test_suite():
    """Create a test suite for addition tests only"""
    suite = unittest.TestSuite()
    
    # Add only addition-related tests
    suite.addTest(TestRefactoredArithmeticOperations('test_add_two_positive_numbers'))
    suite.addTest(TestRefactoredArithmeticOperations('test_add_multiple_numbers'))
    suite.addTest(TestRefactoredArithmeticOperations('test_add_no_arguments'))
    suite.addTest(TestRefactoredArithmeticOperations('test_add_single_argument'))
    
    return suite

if __name__ == '__main__':
    # Run the full test suite
    runner = unittest.TextTestRunner(verbosity=2)
    
    print("Running Full Test Suite:")
    print("=" * 50)
    result = runner.run(create_test_suite())
    
    print("\nRunning Addition Test Suite:")
    print("=" * 50)
    result = runner.run(create_addition_test_suite())

```

3. Run the test suite:

```bash
python3 test_suite.py

```

#### Subtask 6.2: Create Parameterized Tests

Let's create tests that run with multiple sets of data:

1. Create a parameterized test file:

```bash
nano test_parameterized.py

```

2. Add parameterized test examples:

```python
"""
Parameterized Tests for Arithmetic Operations
Demonstrates testing with multiple data sets
"""

import unittest
from arithmetic_operations import add, subtract, multiply, divide

class TestParameterizedArithmetic(unittest.TestCase):
    """Test arithmetic operations with multiple parameter sets"""
    
    def test_add_multiple_cases(self):
        """Test addition with multiple test cases"""
        test_cases = [
            (2, 3, 5),      # (a, b, expected)
            (0, 0, 0),
            (-1, 1, 0),
            (10, -5, 5),
            (2.5, 3.5, 6.0)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = add(a, b)
                self.assertEqual(result, expected)
    
    def test_multiply_multiple_cases(self):
        """Test multiplication with multiple test cases"""
        test_cases = [
            (2, 3, 6),
            (0, 5, 0),
            (-2, 3, -6),
            (4, -2, -8),
            (-3, -4, 12)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = multiply(a, b)
                self.assertEqual(result, expected)
    
    def test_divide_multiple_cases(self):
        """Test division with multiple test cases"""
        test_cases = [
            (10, 2, 5.0),
            (15, 3, 5.0),
            (-12, 4, -3.0),
            (7, 2, 3.5)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = divide(a, b)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)

```

3. Run the parameterized tests:

```bash
python3 test_parameterized.py

```

### Task 7: Test-Driven Development (TDD) Example

#### Subtask 7.1: Write Tests First

Let's demonstrate TDD by writing tests for a function that doesn't exist yet:

1. Create a TDD example file:

```bash
nano test_tdd_example.py

```

2. Write tests for a factorial function that we haven't implemented yet:

```python
"""
Test-Driven Development Example
Writing tests first, then implementing the function
"""

import unittest

class TestFactorial(unittest.TestCase):
    """Test cases for factorial function (to be implemented)"""
    
    def test_factorial_zero(self):
        """Test factorial of 0"""
        from arithmetic_operations import factorial
        self.assertEqual(factorial(0), 1)
    
    def test_factorial_one(self):
        """Test factorial of 1"""
        from arithmetic_operations import factorial
        self.assertEqual(factorial(1), 1)
    
    def test_factorial_positive(self):
        """Test factorial of positive numbers"""
        from arithmetic_operations import factorial
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(3), 6)
    
    def test_factorial_negative(self):
        """Test factorial of negative number should raise error"""
        from arithmetic_operations import factorial
        with self.assertRaises(ValueError):
            factorial(-1)

if __name__ == '__main__':
    unittest.main()

```

3. Try running the test (it will fail because the function doesn't exist):

```bash
python3 test_tdd_example.py

```

#### Subtask 7.2: Implement the Function to Pass Tests

Now let's implement the factorial function to make our tests pass:

1. Add the factorial function to arithmetic_operations.py:

```bash
nano arithmetic_operations.py

```

2. Add the following function at the end of the file:

```python

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

```

3. Now run the TDD test again:

```bash
python3 test_tdd_example.py

```

The tests should now pass!

## Troubleshooting Common Issues

### Issue 1: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'arithmetic_operations'`

**Solution**:

- Ensure you're in the correct directory containing the Python files
- Check that the file name is spelled correctly
- Verify the file has a `.py` extension

### Issue 2: Test Discovery Problems

**Problem**: Tests not being discovered automatically

**Solution**:

- Ensure test files start with `test_`
- Use proper class names starting with `Test`
- Use method names starting with `test_`

### Issue 3: Tests fail after refactoring

If a test fails after changing the implementation, read its assertion and traceback.
Run both the original and the refactored tests to verify backwards compatibility:

```bash
python3 -m unittest discover -v -p 'test_*.py'
```

The runnable version included with this guide contains the final implementation;
the intermediate failing stages in the instructions are for TDD practice only.

### Issue 4: `coverage` command not found

The `coverage` tool is optional and is not part of Python's standard library.
The standard-library tests work without it. If you are allowed to install tools:

```bash
python3 -m pip install --user coverage
python3 -m coverage run -m unittest discover -p 'test_*.py'
python3 -m coverage report
```

## Final Verification

```bash
python3 -m unittest discover -v -p 'test_*.py'
python3 manual_test.py
python3 test_suite.py
```

**Expected result:** The tests finish with `OK`, the manual test prints arithmetic
results, and the suite runner reports no failures. The precise number and
execution time depend on the included tests and machine.

## Conclusion

You wrote unit tests for addition, subtraction, multiplication, division and
powers, explored assertions, tested type errors, refactored the functions, and
used a test-first workflow to add factorial. Every production function now has
tests that can be rerun before or after changes.
