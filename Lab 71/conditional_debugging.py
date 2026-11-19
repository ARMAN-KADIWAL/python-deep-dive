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
