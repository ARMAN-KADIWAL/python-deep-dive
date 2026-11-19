import unittest
from factorial import factorial

class TestFactorial(unittest.TestCase):
    
    def test_factorial_of_positive_number(self):
        """Test factorial calculation for positive numbers"""
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(2), 2)
    
    def test_factorial_of_one(self):
        """Test factorial of 1"""
        self.assertEqual(factorial(1), 1)
    
    def test_factorial_of_zero(self):
        """Test factorial of 0"""
        self.assertEqual(factorial(0), 1)
    
    def test_factorial_of_large_number(self):
        """Test factorial of larger numbers"""
        self.assertEqual(factorial(6), 720)
        self.assertEqual(factorial(7), 5040)
    
    def test_factorial_negative_number(self):
        """Test factorial of negative numbers should raise ValueError"""
        with self.assertRaises(ValueError):
            factorial(-1)
        with self.assertRaises(ValueError):
            factorial(-5)
    
    def test_factorial_non_integer(self):
        """Test factorial of non-integer should raise TypeError"""
        with self.assertRaises(TypeError):
            factorial(3.5)
        with self.assertRaises(TypeError):
            factorial("5")

if __name__ == '__main__':
    unittest.main()
