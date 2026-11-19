"""
Test-Driven Development Example
Writing tests first, then implementing the function
"""

import unittest

class TestFactorial(unittest.TestCase):
    """Test cases for factorial function (to be implemented)"""
    
    def test_factorial_zero(self):
        """Test factorial of 0"""
        from arithmetic_operations import factorial
        self.assertEqual(factorial(0), 1)
    
    def test_factorial_one(self):
        """Test factorial of 1"""
        from arithmetic_operations import factorial
        self.assertEqual(factorial(1), 1)
    
    def test_factorial_positive(self):
        """Test factorial of positive numbers"""
        from arithmetic_operations import factorial
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(3), 6)
    
    def test_factorial_negative(self):
        """Test factorial of negative number should raise error"""
        from arithmetic_operations import factorial
        with self.assertRaises(ValueError):
            factorial(-1)

if __name__ == '__main__':
    unittest.main()
