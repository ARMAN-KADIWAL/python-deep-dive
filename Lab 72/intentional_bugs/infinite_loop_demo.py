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
