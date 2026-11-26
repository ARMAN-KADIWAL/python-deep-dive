import unittest
from repl_examples import (
    greet, calculate_area, factorial_bug, calculate_factorial,
    process_list, analyze_data, find_errors,
)


class TestReplExamples(unittest.TestCase):
    def test_greeting(self):
        self.assertEqual(greet("Alex"), "Hello, Alex!")

    def test_area(self):
        self.assertEqual(calculate_area(10, 5), "Area: 50 square units")
        self.assertEqual(calculate_area(-5, 10), "Invalid dimensions")

    def test_factorial(self):
        self.assertEqual(factorial_bug(5), 24)
        self.assertEqual(calculate_factorial(5), 120)
        self.assertEqual(calculate_factorial(0), 1)

    def test_list(self):
        self.assertEqual(process_list([1, -2, 3, -4, 5]), 3)

    def test_analysis(self):
        result = analyze_data([5, 15, 8, 22, 3, 18, 12, 7, 25, 11])
        self.assertAlmostEqual(result["average"], 103 / 6)
        self.assertEqual(result["count"], 6)

    def test_errors(self):
        self.assertEqual(len(find_errors([50, -5, 75, 150, 25, -10, 200])), 4)


if __name__ == "__main__":
    unittest.main()
