"""Correct base cases and input validation for Fibonacci/factorial."""


def fibonacci(n, memo=None):
    if type(n) is not int:
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if memo is None:
        memo = {0: 0, 1: 1}
    if n not in memo:
        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


def factorial(n):
    if type(n) is not int:
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for value in range(2, n + 1):
        result *= value
    return result


if __name__ == "__main__":
    print("Fibonacci(10):", fibonacci(10))
    print("Factorial(5):", factorial(5))
