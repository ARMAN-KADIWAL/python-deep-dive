# Lab 72: Advanced Debugging Techniques - Using IDE Debuggers

## Objectives

By the end of this lab, students will be able to:

- Set up and configure debugging environments in popular open-source IDEs
- Create complex Python scripts with intentional bugs for debugging practice
- Use breakpoints effectively to pause program execution at specific points
- Navigate and analyze the call stack to understand program flow
- Inspect variables and their values during runtime
- Utilize advanced debugging features like conditional breakpoints and variable watches
- Modify code interactively during debugging sessions
- Apply step-through execution techniques to trace program behavior
- Identify and resolve common programming issues using IDE debugging tools

## Prerequisites

Before starting this lab, students should have:

- Basic understanding of Python programming concepts (variables, functions, loops, conditionals)
- Familiarity with file operations and basic command-line usage
- Understanding of programming concepts like functions, recursion, and loops
- Basic knowledge of how programs execute and flow control
- Experience with text editors or basic IDE usage

## Ready-to-Use Cloud Machines

Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click **Start Lab** to access your environment - no need to build your own virtual machine or install software locally. Your cloud machine comes with:

- Ubuntu Linux operating system
- Python 3.8+ pre-installed
- Visual Studio Code with Python extension
- All necessary debugging tools configured

## Lab Tasks

### Task 1: Setting Up the Debugging Environment

#### Subtask 1.1: Verify Python Installation

First, let's ensure Python is properly installed and accessible.

1. Open the terminal in your cloud machine
2. Check Python version:

```bash
python3 --version

```

3. Verify pip is available:

```bash
pip3 --version

```

#### Subtask 1.2: Launch Visual Studio Code

1. Open Visual Studio Code from the applications menu or run:

```bash
code

```

2. Install the Python extension if not already installed:
   - Click on the Extensions icon in the left sidebar
   - Search for "Python"
   - Install the official Python extension by Microsoft
3. Create a new workspace folder:
   - Click **File** > **Open Folder**
   - Create a new folder called `debugging_lab`
   - Select this folder as your workspace

### Task 2: Creating Complex Scripts with Intentional Issues

#### Subtask 2.1: Create an Infinite Loop Script

Create a script that demonstrates an infinite loop issue.

1. In VS Code, create a new file called `infinite_loop_demo.py`
2. Add the following code:

```python
def count_down(n):
    """
    Function that should count down from n to 0
    but contains an infinite loop bug
    """
    print(f"Starting countdown from {n}")
    
    while n > 0:
        print(f"Current number: {n}")
        # Bug: forgot to decrement n, causing infinite loop
        # n -= 1  # This line is commented out to create the bug
        
        # Simulate some processing time
        import time
        time.sleep(0.5)
    
    print("Countdown complete!")

def main():
    print("=== Infinite Loop Debugging Demo ===")
    user_input = input("Enter a number to count down from: ")
    
    try:
        number = int(user_input)
        if number <= 0:
            print("Please enter a positive number")
            return
        
        count_down(number)
        
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()

```

#### Subtask 2.2: Create a Recursion Problem Script

Create a script with a recursion issue.

1. Create a new file called `recursion_demo.py`
2. Add the following code:

```python
def fibonacci_buggy(n, memo=None):
    """
    Buggy fibonacci function that causes stack overflow
    for larger numbers due to missing base cases
    """
    if memo is None:
        memo = {}
    
    print(f"Calculating fibonacci({n})")
    
    # Bug: Missing proper base cases
    if n in memo:
        return memo[n]
    
    # This will cause infinite recursion for n <= 0
    if n == 1:
        result = 1
    elif n == 2:
        result = 1
    else:
        # Bug: This will recurse infinitely for negative numbers
        result = fibonacci_buggy(n - 1, memo) + fibonacci_buggy(n - 2, memo)
    
    memo[n] = result
    return result

def factorial_with_issue(n):
    """
    Factorial function with logical error
    """
    print(f"Calculating factorial of {n}")
    
    if n < 0:
        # Bug: Should handle negative numbers properly
        return factorial_with_issue(n + 1)  # This creates infinite recursion
    
    if n == 0 or n == 1:
        return 1
    
    return n * factorial_with_issue(n - 1)

def main():
    print("=== Recursion Debugging Demo ===")
    
    while True:
        print("\nChoose an option:")
        print("1. Test Fibonacci (buggy)")
        print("2. Test Factorial (with issue)")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            try:
                n = int(input("Enter a number for Fibonacci: "))
                result = fibonacci_buggy(n)
                print(f"Fibonacci({n}) = {result}")
            except Exception as e:
                print(f"Error occurred: {e}")
                
        elif choice == "2":
            try:
                n = int(input("Enter a number for Factorial: "))
                result = factorial_with_issue(n)
                print(f"Factorial({n}) = {result}")
            except Exception as e:
                print(f"Error occurred: {e}")
                
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

```

#### Subtask 2.3: Create a Complex Data Processing Script

Create a script with multiple types of bugs.

1. Create a new file called `data_processor.py`
2. Add the following code:

```python
class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed_count = 0
        self.error_count = 0
    
    def load_data(self, filename=None):
        """Load data from various sources"""
        if filename:
            try:
                with open(filename, 'r') as file:
                    # Bug: Not handling file format properly
                    self.data = file.read().split('\n')
            except FileNotFoundError:
                print(f"File {filename} not found")
                # Bug: Should return or handle this case
                pass
        else:
            # Generate sample data with intentional issues
            self.data = [
                "100", "200", "invalid", "300", "", "400",
                "500", None, "600", "700", "abc", "800"
            ]
    
    def process_item(self, item):
        """Process individual data item"""
        print(f"Processing item: {item}")
        
        if item is None:
            # Bug: This will cause issues downstream
            return item * 2
        
        if isinstance(item, str) and item.strip() == "":
            # Bug: Should handle empty strings
            return int(item)
        
        try:
            # Convert to number and double it
            number = int(item)
            result = number * 2
            self.processed_count += 1
            return result
        except (ValueError, TypeError) as e:
            print(f"Error processing {item}: {e}")
            self.error_count += 1
            # Bug: Returning None without proper handling
            return None
    
    def calculate_statistics(self):
        """Calculate statistics from processed data"""
        processed_data = []
        
        for item in self.data:
            result = self.process_item(item)
            if result is not None:
                processed_data.append(result)
        
        if not processed_data:
            print("No valid data to process")
            return None
        
        # Bug: Division by zero potential
        average = sum(processed_data) / len(processed_data)
        maximum = max(processed_data)
        minimum = min(processed_data)
        
        # Bug: This might cause issues with None values
        total_items = len(self.data)
        success_rate = (self.processed_count / total_items) * 100
        
        return {
            'average': average,
            'maximum': maximum,
            'minimum': minimum,
            'total_processed': self.processed_count,
            'total_errors': self.error_count,
            'success_rate': success_rate,
            'processed_data': processed_data
        }
    
    def generate_report(self):
        """Generate processing report"""
        print("=== Data Processing Report ===")
        
        stats = self.calculate_statistics()
        
        if stats:
            print(f"Total items processed: {stats['total_processed']}")
            print(f"Total errors: {stats['total_errors']}")
            print(f"Success rate: {stats['success_rate']:.2f}%")
            print(f"Average value: {stats['average']:.2f}")
            print(f"Maximum value: {stats['maximum']}")
            print(f"Minimum value: {stats['minimum']}")
            print(f"Processed data: {stats['processed_data']}")
        else:
            print("No statistics available")

def main():
    print("=== Complex Data Processing Demo ===")
    
    processor = DataProcessor()
    
    # Load sample data
    processor.load_data()
    
    print(f"Loaded {len(processor.data)} items")
    print("Starting processing...")
    
    # Generate report
    processor.generate_report()

if __name__ == "__main__":
    main()

```

### Task 3: Setting Up Breakpoints and Visual Debugging

#### Subtask 3.1: Configure VS Code for Debugging

1. In VS Code, open the `infinite_loop_demo.py` file
2. Click on the **Run and Debug** icon in the left sidebar (or press `Ctrl+Shift+D`)
3. Click **"create a launch.json file"** if prompted
4. Select **Python File** as the debug configuration
5. This creates a `.vscode/launch.json` file with debug settings

#### Subtask 3.2: Set Basic Breakpoints

1. Open `infinite_loop_demo.py`
2. Set breakpoints by clicking in the left margin (gutter) next to line numbers:
   - Set a breakpoint on line 8: `print(f"Starting countdown from {n}")`
   - Set a breakpoint on line 11: `print(f"Current number: {n}")`
   - Set a breakpoint on line 18: `print("Countdown complete!")`
3. The breakpoints should appear as red dots in the gutter

#### Subtask 3.3: Start Debugging Session

1. With `infinite_loop_demo.py` open, press `F5` or click the **Start Debugging** button
2. The program will start and pause at the first breakpoint
3. Notice the debugging toolbar that appears at the top
4. Observe the **Debug Console** at the bottom showing program output

### Task 4: Inspecting Call Stack and Variables

#### Subtask 4.1: Explore the Debug Interface

When the debugger pauses at a breakpoint, examine the debug panels:

1. **Variables Panel** (left side):
   - Expand **Local** to see local variables
   - Expand **Global** to see global variables
   - Notice how variable values are displayed
2. **Call Stack Panel**:
   - Shows the current function call hierarchy
   - Click on different stack frames to navigate
3. **Watch Panel**:
   - Used to monitor specific expressions
   - We'll add watches in the next subtask

#### Subtask 4.2: Add Variable Watches

1. In the **Watch** panel, click the **+** button
2. Add the following expressions to watch:
   - `n`
   - `user_input`
   - `type(n)`
3. Observe how these values change as you step through the code

#### Subtask 4.3: Navigate Through Code Execution

Use the debugging toolbar buttons to control execution:

1. **Continue (F5)**: Resume execution until next breakpoint
2. **Step Over (F10)**: Execute current line and move to next
3. **Step Into (F11)**: Enter function calls
4. **Step Out (Shift+F11)**: Exit current function
5. **Restart (Ctrl+Shift+F5)**: Restart debugging session
6. **Stop (Shift+F5)**: Stop debugging

Practice using these controls:

1. Press **F10** (Step Over) several times to see how the program flows
2. When you reach the `while` loop, notice how `n` never changes
3. This demonstrates the infinite loop bug

### Task 5: Using Advanced Debugging Features

#### Subtask 5.1: Set Conditional Breakpoints

1. Right-click on an existing breakpoint in `infinite_loop_demo.py`
2. Select **Edit Breakpoint**
3. Add a condition: `n == 3`
4. The breakpoint will now only trigger when `n` equals 3

To test this:

1. Remove the comment from line 13: `# n -= 1`
2. Restart debugging (Ctrl+Shift+F5)
3. Enter a number greater than 3
4. Notice the breakpoint only triggers when `n` reaches 3

#### Subtask 5.2: Debug the Recursion Script

1. Open `recursion_demo.py`
2. Set breakpoints at:
   - Line 9: `print(f"Calculating fibonacci({n})")`
   - Line 25: `print(f"Calculating factorial of {n}")`
3. Start debugging and choose option 1 (Fibonacci)
4. Enter a negative number like `-1`
5. Observe the call stack growing infinitely
6. Stop the debugger before it crashes

#### Subtask 5.3: Use Logpoints

Logpoints allow you to log information without stopping execution:

1. Right-click in the gutter where you'd normally set a breakpoint
2. Select **Add Logpoint**
3. Enter a message like: `n is currently {n}`
4. Run the program and observe the output in the Debug Console

### Task 6: Interactive Code Modification

#### Subtask 6.1: Debug Console Interaction

1. While debugging `infinite_loop_demo.py`, pause at a breakpoint
2. In the **Debug Console**, you can execute Python code:
   - Type `n` and press Enter to see the current value
   - Type `n = n - 1` to modify the variable
   - Type `print(f"Modified n to: {n}")` to confirm the change

#### Subtask 6.2: Fix Bugs During Debugging

1. While debugging the infinite loop:
   - Pause at the breakpoint inside the while loop
   - In the Debug Console, type: `n -= 1`
   - Continue execution and see how the loop now terminates
2. For the recursion script:
   - When debugging the factorial function with a negative number
   - Modify the variable in the Debug Console: `n = abs(n)`
   - Continue execution to see the corrected behavior

#### Subtask 6.3: Hot Code Replacement

Some changes can be made directly in the editor during debugging:

1. While debugging, try modifying comments or print statements
2. Save the file (Ctrl+S)
3. Some IDEs support hot reloading of certain changes

### Task 7: Debugging the Complex Data Processor

#### Subtask 7.1: Set Strategic Breakpoints

1. Open `data_processor.py`
2. Set breakpoints at key locations:
   - Line 35: `return item * 2` (None handling bug)
   - Line 39: `return int(item)` (empty string bug)
   - Line 44: Inside the try block
   - Line 70: `average = sum(processed_data) / len(processed_data)`

#### Subtask 7.2: Debug Data Processing Issues

1. Start debugging `data_processor.py`
2. Step through the `process_item` method
3. Watch how different data types are handled:
   - Valid strings: "100", "200"
   - Invalid strings: "invalid", "abc"
   - None values
   - Empty strings
4. In the **Variables** panel, expand objects to see their properties:
   - Expand `self` to see the DataProcessor instance
   - Watch `self.processed_count` and `self.error_count`

#### Subtask 7.3: Analyze Exception Handling

1. When the debugger hits the None multiplication bug:
   - Examine the exception in the call stack
   - Use the Debug Console to test fixes: `item = 0 if item is None else item`
2. For the empty string conversion bug:
   - Test the fix: `item = "0" if item.strip() == "" else item`

### Task 8: Advanced Debugging Scenarios

#### Subtask 8.1: Multi-threaded Debugging Simulation

Create a simple script to demonstrate debugging with multiple execution paths:

1. Create `threading_demo.py`:

```python
import threading
import time
import random

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self, thread_name):
        for i in range(5):
            # Bug: Race condition without proper locking
            current = self.value
            time.sleep(random.uniform(0.01, 0.1))  # Simulate processing
            self.value = current + 1
            print(f"{thread_name}: incremented to {self.value}")

def worker_thread(counter, thread_name):
    print(f"Starting {thread_name}")
    counter.increment(thread_name)
    print(f"Finished {thread_name}")

def main():
    counter = Counter()
    threads = []
    
    # Create multiple threads
    for i in range(3):
        thread_name = f"Thread-{i+1}"
        thread = threading.Thread(target=worker_thread, args=(counter, thread_name))
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"Final counter value: {counter.value}")
    print("Expected value: 15")

if __name__ == "__main__":
    main()

```

2. Debug this script to observe race conditions
3. Set breakpoints in the `increment` method
4. Notice how the debugger handles multiple threads

#### Subtask 8.2: Performance Debugging

Create a script with performance issues:

1. Create `performance_demo.py`:

```python
import time

def inefficient_search(data, target):
    """Inefficient search with debugging points"""
    print(f"Searching for {target} in {len(data)} items")
    
    found_indices = []
    
    # Bug: Inefficient nested loops
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j and data[i] == target:
                found_indices.append(i)
                print(f"Found {target} at index {i}")
    
    return found_indices

def generate_large_dataset(size):
    """Generate test data"""
    import random
    data = []
    for i in range(size):
        data.append(random.randint(1, 100))
    return data

def main():
    print("=== Performance Debugging Demo ===")
    
    # Generate test data
    data_size = 1000
    test_data = generate_large_dataset(data_size)
    target_value = 50
    
    start_time = time.time()
    results = inefficient_search(test_data, target_value)
    end_time = time.time()
    
    print(f"Search completed in {end_time - start_time:.4f} seconds")
    print(f"Found {len(results)} occurrences")

if __name__ == "__main__":
    main()

```

2. Use the debugger to identify the performance bottleneck
3. Set conditional breakpoints to monitor specific iterations

### Task 9: Debugging Best Practices

#### Subtask 9.1: Create a Debugging Checklist

Based on your experience, create a debugging strategy:

1. Create `debugging_checklist.py`:

```python
"""
Debugging Best Practices Checklist

1. Reproduce the Issue
   - Can you consistently reproduce the bug?
   - What are the exact steps to trigger it?

2. Understand the Expected Behavior
   - What should the code do?
   - What is it actually doing?

3. Use Systematic Debugging
   - Start with breakpoints at key locations
   - Use step-through execution to follow the flow
   - Check variable values at each step

4. Isolate the Problem
   - Narrow down the problematic code section
   - Use binary search approach with breakpoints

5. Test Your Fixes
   - Verify the fix resolves the issue
   - Ensure no new bugs are introduced
   - Test edge cases
"""

def demonstrate_debugging_approach():
    """Example of systematic debugging approach"""
    
    # Step 1: Identify the problem area
    def problematic_function(numbers):
        total = 0
        count = 0
        
        for num in numbers:
            if num > 0:  # Bug: Should this be >= 0?
                total += num
                count += 1
        
        # Bug: Division by zero potential
        average = total / count
        return average
    
    # Step 2: Create test cases
    test_cases = [
        [1, 2, 3, 4, 5],      # Normal case
        [-1, -2, -3],         # All negative
        [0, 0, 0],            # All zeros
        [],                   # Empty list
        [0, 1, 2, -1]         # Mixed values
    ]
    
    # Step 3: Debug each test case
    for i, test_case in enumerate(test_cases):
        print(f"\nTest case {i+1}: {test_case}")
        try:
            result = problematic_function(test_case)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
            # This is where you'd set breakpoints and debug

if __name__ == "__main__":
    demonstrate_debugging_approach()

```

#### Subtask 9.2: Practice Debugging Workflow

1. Run the debugging checklist script
2. For each test case that fails:
   - Set appropriate breakpoints
   - Step through the execution
   - Identify the root cause
   - Implement and test the fix

## Troubleshooting Common Issues

### Issue 1: Debugger Not Starting

**Problem**: VS Code debugger doesn't start or shows errors

**Solutions**:

- Ensure Python extension is installed and enabled
- Check that `launch.json` is properly configured
- Verify Python interpreter is correctly selected (Ctrl+Shift+P, then "Python: Select Interpreter")

### Issue 2: Breakpoints Not Working

**Problem**: Breakpoints are ignored during execution

**Solutions**:

- Ensure you're running in debug mode (F5), not normal run mode
- Check that breakpoints are set on executable lines (not comments or empty lines)
- Verify the correct file is being debugged

### Issue 3: Variables Not Showing Values

**Problem**: Variable panel shows no information or incorrect values

**Solutions**:

- Ensure execution is paused at a breakpoint
- Check variable scope (local vs global)
- Try refreshing the debug session

### Issue 4: Performance Issues During Debugging

**Problem**: Debugging is very slow or unresponsive

**Solutions**:

- Remove unnecessary breakpoints
- Use conditional breakpoints instead of stopping at every iteration
- Consider using logpoints for high-frequency code sections

## Conclusion

In this comprehensive lab, you have mastered advanced debugging techniques using open-source IDE tools. You've learned to:

- **Set up professional debugging environments** using VS Code with proper configuration
- **Create and analyze complex bugs** including infinite loops, recursion issues, and data processing errors
- **Use breakpoints strategically** to pause execution at critical points in your code
- **Navigate call stacks and inspect variables** to understand program state and flow
- **Apply advanced debugging features** like conditional breakpoints, variable watches, and logpoints
- **Modify code interactively** during debugging sessions to test fixes in real-time
- **Debug complex scenarios** including multi-threaded applications and performance issues

These debugging skills are essential for professional software development. The ability to systematically identify, isolate, and resolve bugs using IDE debugging tools will significantly improve your programming efficiency and code quality. The techniques you've practiced - from basic breakpoint usage to advanced interactive debugging - form the foundation of professional debugging workflows used in software development teams worldwide.

Remember that effective debugging is both an art and a science. It requires patience, systematic thinking, and the right tools. The IDE debugging features you've mastered in this lab will serve you well throughout your programming career, helping you build more reliable and maintainable software applications.
