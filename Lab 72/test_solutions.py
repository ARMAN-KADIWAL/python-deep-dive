import unittest

from solutions.data_processor_fixed import DataProcessor
from solutions.debugging_checklist_fixed import non_negative_average
from solutions.infinite_loop_fixed import count_down
from solutions.performance_fixed import efficient_search
from solutions.recursion_fixed import factorial, fibonacci
from solutions.threading_fixed import run_demo


class TestDebuggingSolutions(unittest.TestCase):
    def test_countdown(self):
        self.assertEqual(count_down(3), [3, 2, 1, 0])
        with self.assertRaises(ValueError):
            count_down(-1)

    def test_recursion(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(factorial(5), 120)
        with self.assertRaises(ValueError):
            fibonacci(-1)
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_data_processor(self):
        processor = DataProcessor()
        processor.load_data()
        stats = processor.calculate_statistics()
        self.assertEqual(stats["total_processed"], 8)
        self.assertEqual(stats["total_errors"], 4)
        self.assertEqual(stats, processor.calculate_statistics())
        processor.data = []
        self.assertEqual(processor.calculate_statistics()["success_rate"], 0)

    def test_counter(self):
        self.assertEqual(run_demo(), 15)
        self.assertEqual(run_demo(workers=4, iterations=20), 80)

    def test_search(self):
        self.assertEqual(efficient_search([2, 1, 2, 2], 2), [0, 2, 3])

    def test_average(self):
        self.assertEqual(non_negative_average([0, 2, -10]), 1)
        self.assertEqual(non_negative_average([-3, -1]), 0)


if __name__ == "__main__":
    unittest.main()
