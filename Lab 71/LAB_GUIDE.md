# Lab 71: Debugging Techniques and Tools - Introduction to Debugging

## Objectives

By the end of this lab, students will be able to:

- Identify common Python error types including TypeError, NameError, and IndexError
- Use print() statements effectively to trace program execution flow
- Implement the Python Debugger (pdb) to set breakpoints and inspect code
- Navigate through code using pdb commands: continue, next, and step
- Apply systematic debugging techniques to locate and fix bugs in Python programs
- Understand the difference between manual debugging and automated debugging tools

## Prerequisites

Before starting this lab, students should have:

- Basic understanding of Python programming fundamentals
- Knowledge of Python data types (strings, integers, lists, dictionaries)
- Familiarity with Python functions and control structures
- Experience writing and running Python scripts
- Basic command-line navigation skills

## Lab Environment Setup

**Ready-to-Use Cloud Machines**: Al Nafi provides Linux-based cloud machines with Python pre-installed. Simply click **Start Lab** to access your environment - no need to build your own virtual machine or install additional software.

Your cloud machine includes:

- Python 3.8 or higher
- Built-in pdb debugger
- Text editor (nano/vim)
- Terminal access

## Task 1: Creating a Python Script with Intentional Bugs

### Subtask 1.1: Create the Buggy Script

First, we'll create a Python script that contains several common types of errors that developers frequently encounter.

1. Open your terminal in the cloud environment
2. Create a new Python file called `buggy_calculator.py`:

```bash
nano buggy_calculator.py

```

3. Copy and paste the following code into the file:

```python
# buggy_calculator.py - A calculator with intentional bugs
import math

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    total = 0
    for num in numbers:
        total += num
    # Bug 1: Division by zero potential
    average = total / len(numbers)
    return average

def get_square_root(number):
    """Get the square root of a number"""
    # Bug 2: NameError - undefined variable
    if numbr < 0:
        return "Cannot calculate square root of negative number"
    return math.sqrt(number)

def access_list_element(data_list, index):
    """Access an element from a list by index"""
    # Bug 3: IndexError potential
    return data_list[index]

def convert_to_integer(value):
    """Convert a value to integer"""
    # Bug 4: TypeError potential
    return int(value)

def main():
    print("=== Buggy Calculator ===")
    
    # Test case 1: Empty list for average calculation
    empty_list = []
    print("Calculating average of empty list...")
    avg = calculate_average(empty_list)
    print(f"Average: {avg}")
    
    # Test case 2: Square root with typo
    print("\nCalculating square root of 16...")
    sqrt_result = get_square_root(16)
    print(f"Square root: {sqrt_result}")
    
    # Test case 3: Accessing invalid index
    sample_list = [1, 2, 3, 4, 5]
    print(f"\nAccessing element at index 10 from list: {sample_list}")
    element = access_list_element(sample_list, 10)
    print(f"Element: {element}")
    
    # Test case 4: Converting invalid type
    print("\nConverting dictionary to integer...")
    invalid_value = {"key": "value"}
    integer_result = convert_to_integer(invalid_value)
    print(f"Integer result: {integer_result}")

if __name__ == "__main__":
    main()

```

4. Save the file by pressing `Ctrl + X`, then `Y`, then `Enter`

### Subtask 1.2: Run the Script to Observe Errors

1. Execute the script to see the first error:

```bash
python3 buggy_calculator.py

```

2. Observe the error output. You should see a **ZeroDivisionError** when trying to calculate the average of an empty list.

**Expected Output:**

```
=== Buggy Calculator ===
Calculating average of empty list...
Traceback (most recent call last):
  File "buggy_calculator.py", line 45, in main
    avg = calculate_average(empty_list)
  File "buggy_calculator.py", line 9, in calculate_average
    average = total / len(numbers)
ZeroDivisionError: division by zero

```

## Task 2: Using Print Statements for Manual Debugging

### Subtask 2.1: Add Debug Print Statements

Now we'll add print statements to trace the program's execution flow and understand what's happening at each step.

1. Create a new file called `debug_with_prints.py`:

```bash
nano debug_with_prints.py

```

2. Copy the following enhanced version with debug print statements:

```python
# debug_with_prints.py - Calculator with debug print statements
import math

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    print(f"DEBUG: calculate_average called with: {numbers}")
    print(f"DEBUG: Length of numbers list: {len(numbers)}")
    
    if len(numbers) == 0:
        print("DEBUG: Empty list detected, returning 0")
        return 0
    
    total = 0
    for num in numbers:
        print(f"DEBUG: Adding {num} to total. Current total: {total}")
        total += num
    
    print(f"DEBUG: Final total: {total}")
    average = total / len(numbers)
    print(f"DEBUG: Calculated average: {average}")
    return average

def get_square_root(number):
    """Get the square root of a number"""
    print(f"DEBUG: get_square_root called with: {number}")
    print(f"DEBUG: Checking if {number} < 0")
    
    # Fixed the typo: numbr -> number
    if number < 0:
        print("DEBUG: Negative number detected")
        return "Cannot calculate square root of negative number"
    
    result = math.sqrt(number)
    print(f"DEBUG: Square root calculated: {result}")
    return result

def access_list_element(data_list, index):
    """Access an element from a list by index"""
    print(f"DEBUG: access_list_element called with list: {data_list}")
    print(f"DEBUG: Requested index: {index}")
    print(f"DEBUG: List length: {len(data_list)}")
    print(f"DEBUG: Valid index range: 0 to {len(data_list)-1}")
    
    if index >= len(data_list) or index < 0:
        print("DEBUG: Index out of range detected")
        return "Index out of range"
    
    element = data_list[index]
    print(f"DEBUG: Retrieved element: {element}")
    return element

def convert_to_integer(value):
    """Convert a value to integer"""
    print(f"DEBUG: convert_to_integer called with: {value}")
    print(f"DEBUG: Type of value: {type(value)}")
    
    try:
        result = int(value)
        print(f"DEBUG: Conversion successful: {result}")
        return result
    except (TypeError, ValueError) as e:
        print(f"DEBUG: Conversion failed: {e}")
        return f"Cannot convert {type(value).__name__} to integer"

def main():
    print("=== Calculator with Debug Prints ===")
    
    # Test case 1: Empty list for average calculation
    print("\n--- Test Case 1: Empty List Average ---")
    empty_list = []
    print("Calculating average of empty list...")
    avg = calculate_average(empty_list)
    print(f"Average: {avg}")
    
    # Test case 2: Square root calculation
    print("\n--- Test Case 2: Square Root ---")
    print("Calculating square root of 16...")
    sqrt_result = get_square_root(16)
    print(f"Square root: {sqrt_result}")
    
    # Test case 3: Accessing valid and invalid indices
    print("\n--- Test Case 3: List Access ---")
    sample_list = [1, 2, 3, 4, 5]
    print(f"Accessing element at index 2 from list: {sample_list}")
    element = access_list_element(sample_list, 2)
    print(f"Element: {element}")
    
    print(f"\nAccessing element at index 10 from list: {sample_list}")
    element = access_list_element(sample_list, 10)
    print(f"Element: {element}")
    
    # Test case 4: Type conversion
    print("\n--- Test Case 4: Type Conversion ---")
    print("Converting string '42' to integer...")
    valid_conversion = convert_to_integer("42")
    print(f"Integer result: {valid_conversion}")
    
    print("\nConverting dictionary to integer...")
    invalid_value = {"key": "value"}
    integer_result = convert_to_integer(invalid_value)
    print(f"Integer result: {integer_result}")

if __name__ == "__main__":
    main()

```

3. Save the file and run it:

```bash
python3 debug_with_prints.py

```

### Subtask 2.2: Analyze Debug Output

Examine the output carefully. Notice how the debug print statements help you understand:

- **Function entry points**: When each function is called and with what parameters
- **Variable values**: The state of variables at different points in execution
- **Control flow**: Which branches of conditional statements are executed
- **Error conditions**: When and why errors might occur

## Task 3: Introduction to Python Debugger (pdb)

### Subtask 3.1: Basic pdb Setup

The Python Debugger (pdb) is a powerful interactive debugging tool that allows you to pause execution and inspect your program's state.

1. Create a new file called `pdb_example.py`:

```bash
nano pdb_example.py

```

2. Add the following code:

```python
# pdb_example.py - Introduction to Python Debugger
import pdb

def calculate_factorial(n):
    """Calculate factorial of a number"""
    print(f"Calculating factorial of {n}")
    
    # Set a breakpoint here
    pdb.set_trace()
    
    if n < 0:
        return "Factorial not defined for negative numbers"
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
            print(f"Step {i}: result = {result}")
        return result

def main():
    print("=== Factorial Calculator with pdb ===")
    
    # Test with different values
    test_values = [5, 0, -3]
    
    for value in test_values:
        print(f"\nTesting factorial({value}):")
        result = calculate_factorial(value)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()

```

3. Save the file and run it:

```bash
python3 pdb_example.py

```

When the program hits the `pdb.set_trace()` line, it will pause and show the pdb prompt: `(Pdb)`

### Subtask 3.2: Basic pdb Commands

When you see the `(Pdb)` prompt, try these essential commands:

1. **`l` (list)**: Show the current code around the breakpoint

```
(Pdb) l

```

2. **`p variable_name`**: Print the value of a variable

```
(Pdb) p n
(Pdb) p result

```

3. **`pp variable_name`**: Pretty-print a variable (useful for complex data structures)

```
(Pdb) pp locals()

```

4. **`n` (next)**: Execute the next line of code

```
(Pdb) n

```

5. **`c` (continue)**: Continue execution until the next breakpoint

```
(Pdb) c

```

6. **`q` (quit)**: Quit the debugger

```
(Pdb) q

```

## Task 4: Advanced pdb Usage - Stepping Through Code

### Subtask 4.1: Create a Complex Debugging Scenario

1. Create a new file called `advanced_debugging.py`:

```bash
nano advanced_debugging.py

```

2. Add the following code with multiple functions and potential issues:

```python
# advanced_debugging.py - Complex debugging scenario
import pdb

class StudentGradeCalculator:
    def __init__(self):
        self.students = {}
    
    def add_student(self, name, grades):
        """Add a student with their grades"""
        print(f"Adding student: {name}")
        pdb.set_trace()  # Breakpoint 1
        
        if not isinstance(grades, list):
            print("Error: Grades must be a list")
            return False
        
        self.students[name] = grades
        return True
    
    def calculate_average(self, name):
        """Calculate average grade for a student"""
        print(f"Calculating average for: {name}")
        pdb.set_trace()  # Breakpoint 2
        
        if name not in self.students:
            return None
        
        grades = self.students[name]
        if len(grades) == 0:
            return 0
        
        total = sum(grades)
        average = total / len(grades)
        return average
    
    def get_letter_grade(self, average):
        """Convert numerical average to letter grade"""
        print(f"Converting {average} to letter grade")
        pdb.set_trace()  # Breakpoint 3
        
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'
    
    def generate_report(self, name):
        """Generate a grade report for a student"""
        print(f"Generating report for: {name}")
        
        average = self.calculate_average(name)
        if average is None:
            return f"Student {name} not found"
        
        letter_grade = self.get_letter_grade(average)
        return f"Student: {name}, Average: {average:.2f}, Grade: {letter_grade}"

def main():
    print("=== Student Grade Calculator ===")
    
    calculator = StudentGradeCalculator()
    
    # Add some students
    calculator.add_student("Alice", [85, 92, 78, 96])
    calculator.add_student("Bob", [72, 68, 75, 80])
    calculator.add_student("Charlie", [])  # Empty grades list
    
    # Generate reports
    students = ["Alice", "Bob", "Charlie", "David"]  # David doesn't exist
    
    for student in students:
        print(f"\n--- Report for {student} ---")
        report = calculator.generate_report(student)
        print(report)

if __name__ == "__main__":
    main()

```

3. Save and run the file:

```bash
python3 advanced_debugging.py

```

### Subtask 4.2: Practice Advanced pdb Commands

When the debugger stops at each breakpoint, practice these commands:

1. **`s` (step)**: Step into function calls

```
(Pdb) s

```

2. **`r` (return)**: Continue until the current function returns

```
(Pdb) r

```

3. **`w` (where)**: Show the current call stack

```
(Pdb) w

```

4. **`u` (up)** and **`d` (down)**: Navigate up and down the call stack

```
(Pdb) u
(Pdb) d

```

5. **`a` (args)**: Show arguments of the current function

```
(Pdb) a

```

6. **`whatis variable_name`**: Show the type of a variable

```
(Pdb) whatis name
(Pdb) whatis grades

```

## Task 5: Mastering pdb Flow Control Commands

### Subtask 5.1: Understanding continue, next, and step

Create a comprehensive example to understand the differences between these commands:

1. Create `flow_control_demo.py`:

```bash
nano flow_control_demo.py

```

2. Add the following code:

```python
# flow_control_demo.py - Demonstrating pdb flow control
import pdb

def outer_function(x):
    """Outer function that calls inner functions"""
    print(f"Outer function called with x = {x}")
    pdb.set_trace()  # Main breakpoint
    
    result1 = inner_function_a(x)
    result2 = inner_function_b(x)
    
    final_result = combine_results(result1, result2)
    return final_result

def inner_function_a(value):
    """First inner function"""
    print(f"Inner function A: processing {value}")
    processed = value * 2
    return processed

def inner_function_b(value):
    """Second inner function"""
    print(f"Inner function B: processing {value}")
    processed = value + 10
    return processed

def combine_results(a, b):
    """Combine two results"""
    print(f"Combining {a} and {b}")
    return a + b

def main():
    print("=== Flow Control Demonstration ===")
    
    test_values = [5, 10]
    
    for value in test_values:
        print(f"\n--- Processing value: {value} ---")
        result = outer_function(value)
        print(f"Final result: {result}")

if __name__ == "__main__":
    main()

```

3. Run the program and practice each command:

```bash
python3 flow_control_demo.py

```

### Subtask 5.2: Command Practice Guide

When the debugger stops, try this sequence to understand each command:

**Round 1: Using `next` (n)**

```
(Pdb) n    # Execute next line, don't step into functions
(Pdb) n    # Continue with next line
(Pdb) n    # Notice it doesn't enter inner_function_a

```

**Round 2: Using `step` (s)**

```
(Pdb) s    # Step into the function call
(Pdb) l    # List code to see where you are
(Pdb) s    # Continue stepping through the function

```

**Round 3: Using `continue` (c)**

```
(Pdb) c    # Continue until next breakpoint or end of program

```

### Subtask 5.3: Setting Conditional Breakpoints

1. Create `conditional_debugging.py`:

```bash
nano conditional_debugging.py

```

2. Add this code:

```python
# conditional_debugging.py - Conditional breakpoints example
import pdb

def process_numbers(numbers):
    """Process a list of numbers"""
    results = []
    
    for i, num in enumerate(numbers):
        print(f"Processing number {i}: {num}")
        
        # Conditional breakpoint - only stop when num > 50
        if num > 50:
            pdb.set_trace()
        
        # Simulate some processing
        if num % 2 == 0:
            processed = num * 2
        else:
            processed = num * 3
        
        results.append(processed)
    
    return results

def main():
    print("=== Conditional Breakpoint Demo ===")
    
    test_numbers = [10, 25, 60, 75, 30, 80, 15]
    
    print(f"Processing numbers: {test_numbers}")
    results = process_numbers(test_numbers)
    print(f"Results: {results}")

if __name__ == "__main__":
    main()

```

3. Run and observe that the debugger only stops when the condition is met:

```bash
python3 conditional_debugging.py

```

## Task 6: Debugging Real-World Scenarios

### Subtask 6.1: Fix the Original Buggy Calculator

Now let's go back to our original buggy calculator and fix all the issues using our debugging skills:

1. Create `fixed_calculator.py`:

```bash
nano fixed_calculator.py

```

2. Add the corrected version:

```python
# fixed_calculator.py - Debugged and corrected calculator
import math
import pdb

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    if len(numbers) == 0:
        print("Warning: Cannot calculate average of empty list")
        return 0
    
    total = sum(numbers)
    average = total / len(numbers)
    return average

def get_square_root(number):
    """Get the square root of a number"""
    # Fixed: numbr -> number
    if number < 0:
        return "Cannot calculate square root of negative number"
    return math.sqrt(number)

def access_list_element(data_list, index):
    """Access an element from a list by index"""
    # Fixed: Added bounds checking
    if index < 0 or index >= len(data_list):
        return f"Index {index} is out of range for list of length {len(data_list)}"
    return data_list[index]

def convert_to_integer(value):
    """Convert a value to integer"""
    # Fixed: Added proper error handling
    try:
        return int(value)
    except (TypeError, ValueError) as e:
        return f"Cannot convert {type(value).__name__} to integer: {str(e)}"

def main():
    print("=== Fixed Calculator ===")
    
    # Test case 1: Empty list for average calculation
    print("\n--- Test Case 1: Empty List Average ---")
    empty_list = []
    print("Calculating average of empty list...")
    avg = calculate_average(empty_list)
    print(f"Average: {avg}")
    
    # Test case 2: Square root calculation
    print("\n--- Test Case 2: Square Root ---")
    print("Calculating square root of 16...")
    sqrt_result = get_square_root(16)
    print(f"Square root: {sqrt_result}")
    
    print("Calculating square root of -4...")
    sqrt_result = get_square_root(-4)
    print(f"Square root: {sqrt_result}")
    
    # Test case 3: List access
    print("\n--- Test Case 3: List Access ---")
    sample_list = [1, 2, 3, 4, 5]
    print(f"Accessing element at index 2 from list: {sample_list}")
    element = access_list_element(sample_list, 2)
    print(f"Element: {element}")
    
    print(f"Accessing element at index 10 from list: {sample_list}")
    element = access_list_element(sample_list, 10)
    print(f"Element: {element}")
    
    # Test case 4: Type conversion
    print("\n--- Test Case 4: Type Conversion ---")
    print("Converting string '42' to integer...")
    valid_conversion = convert_to_integer("42")
    print(f"Integer result: {valid_conversion}")
    
    print("Converting dictionary to integer...")
    invalid_value = {"key": "value"}
    integer_result = convert_to_integer(invalid_value)
    print(f"Integer result: {integer_result}")

if __name__ == "__main__":
    main()

```

3. Run the fixed version:

```bash
python3 fixed_calculator.py

```

### Subtask 6.2: Create Your Own Debugging Challenge

1. Create `debugging_challenge.py`:

```bash
nano debugging_challenge.py

```

2. Add this code with intentional bugs for practice:

```python
# debugging_challenge.py - Find and fix the bugs!
import pdb

def fibonacci_sequence(n):
    """Generate fibonacci sequence up to n terms"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        # Bug: Check this calculation
        next_num = sequence[i-1] + sequence[i-2]
        sequence.append(next_num)
    
    return sequence

def find_prime_numbers(limit):
    """Find all prime numbers up to limit"""
    if limit < 2:
        return []
    
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        # Bug: Check the range here
        for divisor in range(2, num):
            if num % divisor == 0:
                is_prime = False
                break
        
        if is_prime:
            primes.append(num)
    
    return primes

def word_frequency(text):
    """Count frequency of words in text"""
    # Bug: What about case sensitivity and punctuation?
    words = text.split()
    frequency = {}
    
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    
    return frequency

def main():
    print("=== Debugging Challenge ===")
    
    # Test fibonacci
    print("\n--- Fibonacci Test ---")
    fib_result = fibonacci_sequence(10)
    print(f"Fibonacci(10): {fib_result}")
    
    # Test prime numbers
    print("\n--- Prime Numbers Test ---")
    primes = find_prime_numbers(20)
    print(f"Primes up to 20: {primes}")
    
    # Test word frequency
    print("\n--- Word Frequency Test ---")
    sample_text = "Hello world! Hello Python. Python is great, Python is fun."
    freq = word_frequency(sample_text)
    print(f"Word frequency: {freq}")

if __name__ == "__main__":
    main()

```

3. Run the challenge and use pdb to identify and fix the bugs:

```bash
python3 debugging_challenge.py

```

**Debugging Exercise**: Use `pdb.set_trace()` to add breakpoints and identify these issues:

- Fibonacci calculation logic
- Prime number algorithm efficiency
- Word frequency case sensitivity and punctuation handling

## Troubleshooting Common Issues

### Issue 1: pdb Commands Not Working

**Problem**: pdb commands don't seem to respond **Solution**: Make sure you're typing commands at the `(Pdb)` prompt, not in a regular Python shell

### Issue 2: Can't Exit pdb

**Problem**: Stuck in pdb debugger **Solution**: Use `q` to quit, or `c` to continue execution

### Issue 3: Lost in the Code

**Problem**: Don't know where you are in the program **Solution**: Use `l` to list current code, `w` to see the call stack

### Issue 4: Variables Not Showing Expected Values

**Problem**: Variables have unexpected values **Solution**: Use `pp locals()` to see all local variables, or `p variable_name` for specific variables

## Conclusion

In this lab, you have successfully learned essential debugging techniques and tools for Python development. Here's what you accomplished:

**Key Skills Developed:**

- **Error Identification**: You learned to recognize common Python errors (TypeError, NameError, IndexError, ZeroDivisionError)
- **Manual Debugging**: You practiced using print statements to trace program execution and understand code flow
- **Automated Debugging**: You mastered the Python Debugger (pdb) for interactive debugging sessions
- **Flow Control**: You learned to use continue, next, and step commands to control debugging execution
- **Problem Solving**: You applied systematic debugging approaches to identify and fix real code issues

**Why This Matters:** Debugging is one of the most critical skills for any programmer. The techniques you learned today will help you:

- **Save Time**: Quickly identify and fix bugs instead of guessing what's wrong
- **Understand Code Better**: See exactly how your programs execute step by step
- **Build Confidence**: Approach complex problems with systematic debugging strategies
- **Professional Development**: Use industry-standard tools and practices used by professional developers

**Next Steps:**

- Practice these debugging techniques on your own projects
- Explore advanced pdb features like conditional breakpoints
- Learn about IDE debugging tools that build on these concepts
- Apply these skills to larger, more complex programs

Remember: Good debugging skills separate novice programmers from experienced developers. The time you invest in mastering these tools will pay dividends throughout your programming career.
