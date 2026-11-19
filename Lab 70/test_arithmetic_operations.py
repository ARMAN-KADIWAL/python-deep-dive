"""
Unit Tests for Arithmetic Operations Module
This module contains unit tests for testing arithmetic functions.
"""

import unittest
from arithmetic_operations import add, subtract, multiply, divide, power

class TestArithmeticOperations(unittest.TestCase):
    """Test case class for arithmetic operations"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        print(f"Running test: {self._testMethodName}")
    
    def tearDown(self):
        """Clean up after each test method."""
        print(f"Completed test: {self._testMethodName}")

    def test_add_positive_numbers(self):
        """Test addition of positive numbers"""
        result = add(5, 3)
        self.assertEqual(result, 8)
        
    def test_add_negative_numbers(self):
        """Test addition of negative numbers"""
        result = add(-5, -3)
        self.assertEqual(result, -8)
        
    def test_add_positive_and_negative(self):
        """Test addition of positive and negative numbers"""
        result = add(10, -3)
        self.assertEqual(result, 7)
        
    def test_add_zero(self):
        """Test addition with zero"""
        result = add(5, 0)
        self.assertEqual(result, 5)
        
    def test_add_floats(self):
        """Test addition of floating point numbers"""
        result = add(2.5, 3.7)
        self.assertAlmostEqual(result, 6.2, places=1)


    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers"""
        result = subtract(10, 3)
        self.assertEqual(result, 7)
        
    def test_subtract_negative_numbers(self):
        """Test subtraction of negative numbers"""
        result = subtract(-5, -3)
        self.assertEqual(result, -2)
        
    def test_subtract_larger_from_smaller(self):
        """Test subtracting larger number from smaller"""
        result = subtract(3, 10)
        self.assertEqual(result, -7)
        
    def test_subtract_zero(self):
        """Test subtraction with zero"""
        result = subtract(5, 0)
        self.assertEqual(result, 5)
        
    def test_subtract_floats(self):
        """Test subtraction of floating point numbers"""
        result = subtract(5.8, 2.3)
        self.assertAlmostEqual(result, 3.5, places=1)


    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers"""
        result = multiply(4, 5)
        self.assertEqual(result, 20)
        
    def test_multiply_negative_numbers(self):
        """Test multiplication of negative numbers"""
        result = multiply(-3, -4)
        self.assertEqual(result, 12)
        
    def test_multiply_positive_and_negative(self):
        """Test multiplication of positive and negative numbers"""
        result = multiply(6, -2)
        self.assertEqual(result, -12)
        
    def test_multiply_by_zero(self):
        """Test multiplication by zero"""
        result = multiply(5, 0)
        self.assertEqual(result, 0)
        
    def test_multiply_by_one(self):
        """Test multiplication by one"""
        result = multiply(7, 1)
        self.assertEqual(result, 7)
        
    def test_multiply_floats(self):
        """Test multiplication of floating point numbers"""
        result = multiply(2.5, 4.0)
        self.assertEqual(result, 10.0)


    def test_divide_positive_numbers(self):
        """Test division of positive numbers"""
        result = divide(15, 3)
        self.assertEqual(result, 5.0)
        
    def test_divide_negative_numbers(self):
        """Test division of negative numbers"""
        result = divide(-12, -4)
        self.assertEqual(result, 3.0)
        
    def test_divide_positive_and_negative(self):
        """Test division of positive and negative numbers"""
        result = divide(20, -4)
        self.assertEqual(result, -5.0)
        
    def test_divide_by_one(self):
        """Test division by one"""
        result = divide(8, 1)
        self.assertEqual(result, 8.0)
        
    def test_divide_floats(self):
        """Test division of floating point numbers"""
        result = divide(7.5, 2.5)
        self.assertEqual(result, 3.0)
        
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError"""
        with self.assertRaises(ValueError):
            divide(10, 0)
            
    def test_divide_by_zero_message(self):
        """Test division by zero error message"""
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            divide(5, 0)


    def test_power_positive_base_positive_exponent(self):
        """Test positive base with positive exponent"""
        result = power(2, 3)
        self.assertEqual(result, 8)
        
    def test_power_positive_base_zero_exponent(self):
        """Test positive base with zero exponent"""
        result = power(5, 0)
        self.assertEqual(result, 1)
        
    def test_power_positive_base_negative_exponent(self):
        """Test positive base with negative exponent"""
        result = power(2, -2)
        self.assertEqual(result, 0.25)
        
    def test_power_negative_base_even_exponent(self):
        """Test negative base with even exponent"""
        result = power(-3, 2)
        self.assertEqual(result, 9)
        
    def test_power_negative_base_odd_exponent(self):
        """Test negative base with odd exponent"""
        result = power(-2, 3)
        self.assertEqual(result, -8)
        
    def test_power_float_numbers(self):
        """Test power with floating point numbers"""
        result = power(2.5, 2)
        self.assertEqual(result, 6.25)


if __name__ == '__main__':
    unittest.main()
