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
