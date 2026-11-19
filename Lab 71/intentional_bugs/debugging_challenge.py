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
