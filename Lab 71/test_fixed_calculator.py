import unittest

from fixed_calculator import (
    access_list_element,
    calculate_average,
    convert_to_integer,
    get_square_root,
)


class TestFixedCalculator(unittest.TestCase):
    def test_average(self):
        self.assertEqual(calculate_average([2, 4, 6]), 4)
        self.assertEqual(calculate_average([]), 0)

    def test_square_root(self):
        self.assertEqual(get_square_root(16), 4)
        self.assertIn("negative", get_square_root(-4).lower())

    def test_list_access(self):
        self.assertEqual(access_list_element([1, 2, 3], 1), 2)
        self.assertIn("out of range", access_list_element([1, 2], 10))

    def test_convert(self):
        self.assertEqual(convert_to_integer("42"), 42)
        self.assertIn("Cannot convert", convert_to_integer({"x": 1}))


if __name__ == "__main__":
    unittest.main()
