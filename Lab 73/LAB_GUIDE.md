# Lab 73: Test-Driven Development (TDD) - Writing Tests Before Code

## Objectives

By the end of this lab, students will be able to:

- Understand the fundamental principles of Test-Driven Development (TDD)
- Write unit tests before implementing the actual code functionality
- Follow the Red-Green-Refactor cycle of TDD
- Create comprehensive test cases including edge cases
- Use Python's built-in unittest framework for testing
- Refactor code while maintaining test coverage
- Appreciate the benefits of TDD in software development

## Prerequisites

Before starting this lab, students should have:

- Basic understanding of Python programming language
- Familiarity with functions and control structures in Python
- Understanding of basic mathematical concepts (factorial)
- Knowledge of command-line operations in Linux
- Basic understanding of software testing concepts

## Lab Environment Setup

**Ready-to-Use Cloud Machines**: Al Nafi provides Linux-based cloud machines with Python pre-installed. Simply click **Start Lab** to access your environment - no need to build your own VM or install additional software.

Your cloud machine comes with:

- Python 3.8 or higher
- Built-in unittest framework
- Text editor (nano/vim)
- Terminal access

## Lab Overview

Test-Driven Development (TDD) is a software development methodology where you write tests before writing the actual code. The process follows a simple cycle:

1. **Red**: Write a failing test
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve the code while keeping tests passing

In this lab, we'll implement a factorial function using TDD principles.

## Task 1: Setting Up the Project Structure

### Step 1.1: Create Project Directory

First, let's create a directory structure for our TDD project.

```bash
mkdir tdd_factorial_lab
cd tdd_factorial_lab

```

### Step 1.2: Create Project Files

Create the necessary files for our project:

```bash
touch factorial.py
touch test_factorial.py

```

Verify the files were created:

```bash
ls -la

```

You should see:

- `factorial.py` - This will contain our factorial function
- `test_factorial.py` - This will contain our unit tests

## Task 2: Writing Initial Unit Tests (Red Phase)

### Step 2.1: Create Basic Test Structure

Open the test file using nano editor:

```bash
nano test_factorial.py

```

Write the initial test structure:

```python
import unittest
from factorial import factorial

class TestFactorial(unittest.TestCase):
    
    def test_factorial_of_positive_number(self):
        """Test factorial calculation for positive numbers"""
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(2), 2)
    
    def test_factorial_of_one(self):
        """Test factorial of 1"""
        self.assertEqual(factorial(1), 1)
    
    def test_factorial_of_zero(self):
        """Test factorial of 0"""
        self.assertEqual(factorial(0), 1)

if __name__ == '__main__':
    unittest.main()

```

Save and exit (Ctrl+X, then Y, then Enter).

### Step 2.2: Run the Tests and Watch Them Fail

Now let's run our tests to see them fail (this is the **Red** phase):

```bash
python3 test_factorial.py

```

You should see an error similar to:

```
ImportError: cannot import name 'factorial' from 'factorial'

```

This is expected! We haven't written the factorial function yet. This demonstrates the first principle of TDD: **write tests first**.

## Task 3: Writing Minimal Code to Pass Tests (Green Phase)

### Step 3.1: Create Empty Function

Open the factorial.py file:

```bash
nano factorial.py

```

Create a minimal function that will allow our tests to run:

```python
def factorial(n):
    """Calculate the factorial of a number"""
    pass

```

Save and exit.

### Step 3.2: Run Tests Again

```bash
python3 test_factorial.py

```

Now you should see test failures instead of import errors:

```
FAIL: test_factorial_of_one (__main__.TestFactorial)
FAIL: test_factorial_of_positive_number (__main__.TestFactorial)
FAIL: test_factorial_of_zero (__main__.TestFactorial)

```

### Step 3.3: Implement Minimal Working Code

Now let's implement the minimal code to make our tests pass:

```bash
nano factorial.py

```

Replace the content with:

```python
def factorial(n):
    """Calculate the factorial of a number"""
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result

```

Save and exit.

### Step 3.4: Run Tests to Verify They Pass

```bash
python3 test_factorial.py

```

You should now see:

```
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK

```

Congratulations! You've completed the **Green** phase - all tests are now passing.

## Task 4: Refactoring Code While Maintaining Tests (Refactor Phase)

### Step 4.1: Analyze Current Implementation

Our current implementation works, but let's consider if we can improve it. We could implement it recursively for better readability.

### Step 4.2: Refactor to Recursive Implementation

Open the factorial.py file:

```bash
nano factorial.py

```

Refactor the code to use recursion:

```python
def factorial(n):
    """Calculate the factorial of a number using recursion"""
    # Base cases
    if n == 0 or n == 1:
        return 1
    
    # Recursive case
    return n * factorial(n - 1)

```

Save and exit.

### Step 4.3: Verify Tests Still Pass After Refactoring

```bash
python3 test_factorial.py

```

The tests should still pass:

```
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK

```

This demonstrates the power of TDD - we can refactor confidently knowing our tests will catch any regressions.

## Task 5: Adding Edge Cases and Additional Tests

### Step 5.1: Add Tests for Edge Cases

Let's add more comprehensive tests including edge cases:

```bash
nano test_factorial.py

```

Expand the test file with additional test cases:

```python
import unittest
from factorial import factorial

class TestFactorial(unittest.TestCase):
    
    def test_factorial_of_positive_number(self):
        """Test factorial calculation for positive numbers"""
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(2), 2)
    
    def test_factorial_of_one(self):
        """Test factorial of 1"""
        self.assertEqual(factorial(1), 1)
    
    def test_factorial_of_zero(self):
        """Test factorial of 0"""
        self.assertEqual(factorial(0), 1)
    
    def test_factorial_of_large_number(self):
        """Test factorial of larger numbers"""
        self.assertEqual(factorial(6), 720)
        self.assertEqual(factorial(7), 5040)
    
    def test_factorial_negative_number(self):
        """Test factorial of negative numbers should raise ValueError"""
        with self.assertRaises(ValueError):
            factorial(-1)
        with self.assertRaises(ValueError):
            factorial(-5)
    
    def test_factorial_non_integer(self):
        """Test factorial of non-integer should raise TypeError"""
        with self.assertRaises(TypeError):
            factorial(3.5)
        with self.assertRaises(TypeError):
            factorial("5")

if __name__ == '__main__':
    unittest.main()

```

Save and exit.

### Step 5.2: Run Tests to See New Failures

```bash
python3 test_factorial.py

```

You should see some tests failing because our function doesn't handle negative numbers or non-integers properly.

### Step 5.3: Update Implementation to Handle Edge Cases

```bash
nano factorial.py

```

Update the factorial function to handle edge cases:

```python
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

```

Save and exit.

### Step 5.4: Run Final Tests

```bash
python3 test_factorial.py

```

All tests should now pass:

```
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK

```

## Task 6: Running Tests with Verbose Output

### Step 6.1: Run Tests with Detailed Output

To see more details about which tests are running:

```bash
python3 test_factorial.py -v

```

You should see output like:

```
test_factorial_negative_number (__main__.TestFactorial) ... ok
test_factorial_non_integer (__main__.TestFactorial) ... ok
test_factorial_of_large_number (__main__.TestFactorial) ... ok
test_factorial_of_one (__main__.TestFactorial) ... ok
test_factorial_of_positive_number (__main__.TestFactorial) ... ok
test_factorial_of_zero (__main__.TestFactorial) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK

```

### Step 6.2: Test the Function Manually

Let's also test our function interactively:

```bash
python3 -c "from factorial import factorial; print('5! =', factorial(5)); print('0! =', factorial(0)); print('1! =', factorial(1))"

```

Expected output:

```
5! = 120
0! = 1
1! = 1

```

## Task 7: Understanding the TDD Cycle

### Step 7.1: Review What We Accomplished

Let's review the complete TDD cycle we just completed:

1. **Red Phase**: We wrote failing tests first
2. **Green Phase**: We wrote minimal code to make tests pass
3. **Refactor Phase**: We improved the code while keeping tests green
4. **Repeat**: We added more tests and enhanced our implementation

### Step 7.2: Create a Summary Script

Create a demonstration script to show our final implementation:

```bash
nano demo.py

```

Add the following content:

```python
#!/usr/bin/env python3
"""
Demonstration of TDD Factorial Implementation
"""

from factorial import factorial

def main():
    print("=== TDD Factorial Function Demo ===")
    print()
    
    # Test normal cases
    test_cases = [0, 1, 2, 3, 4, 5, 6, 7]
    
    print("Normal test cases:")
    for n in test_cases:
        result = factorial(n)
        print(f"factorial({n}) = {result}")
    
    print()
    print("Edge case handling:")
    
    # Test error cases
    try:
        factorial(-1)
    except ValueError as e:
        print(f"factorial(-1) raises ValueError: {e}")
    
    try:
        factorial(3.5)
    except TypeError as e:
        print(f"factorial(3.5) raises TypeError: {e}")
    
    try:
        factorial("5")
    except TypeError as e:
        print(f"factorial('5') raises TypeError: {e}")

if __name__ == "__main__":
    main()

```

Save and exit.

### Step 7.3: Run the Demo

```bash
python3 demo.py

```

## Troubleshooting Common Issues

### Issue 1: Import Errors

If you get import errors, ensure:

- Both files are in the same directory
- File names are spelled correctly
- Python files have the `.py` extension

### Issue 2: Indentation Errors

Python is sensitive to indentation. Ensure:

- Use consistent indentation (4 spaces recommended)
- Don't mix tabs and spaces
- All code blocks are properly indented

### Issue 3: Test Failures

If tests fail unexpectedly:

- Check your function logic carefully
- Ensure you're handling all edge cases
- Verify test expectations match your implementation

### Issue 4: Recursion Depth

For very large numbers, you might hit Python's recursion limit. This is expected behavior and demonstrates why iterative solutions might be preferred for large inputs.

## Key Concepts Learned

### TDD Principles

- **Red-Green-Refactor**: The core cycle of TDD
- **Test First**: Always write tests before implementation
- **Minimal Code**: Write only enough code to make tests pass
- **Continuous Refactoring**: Improve code while maintaining test coverage

### Testing Best Practices

- **Descriptive Test Names**: Use clear, descriptive test method names
- **Test Documentation**: Include docstrings explaining what each test does
- **Edge Case Testing**: Test boundary conditions and error cases
- **Assertion Methods**: Use appropriate unittest assertion methods

### Code Quality Benefits

- **Confidence in Changes**: Tests provide safety net for refactoring
- **Documentation**: Tests serve as living documentation
- **Design Improvement**: TDD often leads to better code design
- **Bug Prevention**: Catch issues early in development cycle

## Conclusion

In this lab, you successfully implemented Test-Driven Development (TDD) by:

1. **Writing tests first** before any implementation code
2. **Following the Red-Green-Refactor cycle** to develop a factorial function
3. **Creating comprehensive test coverage** including edge cases and error conditions
4. **Refactoring code** while maintaining test integrity
5. **Understanding TDD benefits** such as confidence in code changes and better design

TDD is a powerful development methodology that helps create more reliable, maintainable, and well-designed software. The discipline of writing tests first forces you to think about your code's interface and behavior before implementation, often resulting in cleaner, more focused code.

The factorial function you developed demonstrates how TDD can guide you through the complete development process, from initial implementation to handling complex edge cases. This approach scales well to larger, more complex software projects where maintaining code quality and preventing regressions becomes increasingly important.

Remember: **Red** (write failing test), **Green** (make it pass), **Refactor** (improve the code) - this simple cycle is the foundation of effective test-driven development.
