"""Average of non-negative numbers, including zero; handle no matches."""


def non_negative_average(numbers):
    non_negative = [number for number in numbers if number >= 0]
    return sum(non_negative) / len(non_negative) if non_negative else 0


if __name__ == "__main__":
    for values in ([1, 2, 3], [-1, -2], [0, 0], []):
        print(values, "=>", non_negative_average(values))
