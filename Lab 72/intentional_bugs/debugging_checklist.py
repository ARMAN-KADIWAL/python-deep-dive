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
