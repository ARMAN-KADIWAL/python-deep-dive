# Comparison script to show improvements
import os

def count_lines_in_file(filename):
    """Count lines in a file."""
    try:
        with open(filename, 'r') as file:
            return len(file.readlines())
    except FileNotFoundError:
        return 0

def analyze_code_quality():
    """Analyze and compare different versions."""
    files = [
        ("messy_calculator.py", "Original Messy Code"),
        ("clean_calculator.py", "Step 1: Broken into Functions"),
        ("dry_calculator.py", "Step 2: Applied DRY Principle"),
        ("final_clean_calculator.py", "Final: Clean and Simple")
    ]
    
    print("Code Quality Comparison:")
    print("-" * 50)
    
    for filename, description in files:
        line_count = count_lines_in_file(filename)
        print(f"{description}: {line_count} lines")
    
    print("\nKey Improvements Made:")
    print("1. Broke large functions into smaller, focused functions")
    print("2. Eliminated code duplication using DRY principle")
    print("3. Simplified conditionals and loops")
    print("4. Used meaningful names for variables and functions")
    print("5. Added proper error handling")
    print("6. Organized code into classes for better structure")

if __name__ == "__main__":
    analyze_code_quality()
