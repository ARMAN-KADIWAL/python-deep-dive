"""Finite countdown with validation; corrected infinite-loop exercise."""

def count_down(n):
    if type(n) is not int:
        raise TypeError("Count must be an integer")
    if n < 0:
        raise ValueError("Count must be non-negative")
    return list(range(n, -1, -1))


if __name__ == "__main__":
    print("Countdown:", count_down(5))
