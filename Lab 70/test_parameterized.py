"""
Parameterized Tests for Arithmetic Operations
Demonstrates testing with multiple data sets
"""

import unittest
from arithmetic_operations import add, subtract, multiply, divide

class TestParameterizedArithmetic(unittest.TestCase):
    """Test arithmetic operations with multiple parameter sets"""
    
    def test_add_multiple_cases(self):
        """Test addition with multiple test cases"""
        test_cases = [
            (2, 3, 5),      # (a, b, expected)
            (0, 0, 0),
            (-1, 1, 0),
            (10, -5, 5),
            (2.5, 3.5, 6.0)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = add(a, b)
                self.assertEqual(result, expected)
    
    def test_multiply_multiple_cases(self):
        """Test multiplication with multiple test cases"""
        test_cases = [
            (2, 3, 6),
            (0, 5, 0),
            (-2, 3, -6),
            (4, -2, -8),
            (-3, -4, 12)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = multiply(a, b)
                self.assertEqual(result, expected)
    
    def test_divide_multiple_cases(self):
        """Test division with multiple test cases"""
        test_cases = [
            (10, 2, 5.0),
            (15, 3, 5.0),
            (-12, 4, -3.0),
            (7, 2, 3.5)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = divide(a, b)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)
