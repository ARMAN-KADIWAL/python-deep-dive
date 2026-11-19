"""A linear-time search replaces the unnecessary nested loops."""


def efficient_search(data, target):
    return [index for index, value in enumerate(data) if value == target]


if __name__ == "__main__":
    print("Matching indices:", efficient_search([1, 2, 1, 4], 1))
