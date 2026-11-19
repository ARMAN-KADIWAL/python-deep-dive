"""
Unit Tests for Refactored Arithmetic Operations Module
"""

import unittest
from arithmetic_operations import add, subtract, multiply, divide, power

class TestRefactoredArithmeticOperations(unittest.TestCase):
    """Test case class for refactored arithmetic operations"""
    
    # Updated tests for add function (now supports multiple arguments)
    def test_add_two_positive_numbers(self):
        """Test addition of two positive numbers"""
        result = add(5, 3)
        self.assertEqual(result, 8)
        
    def test_add_multiple_numbers(self):
        """Test addition of multiple numbers"""
        result = add(1, 2, 3, 4, 5)
        self.assertEqual(result, 15)
        
    def test_add_no_arguments(self):
        """Test addition with no arguments"""
        result = add()
        self.assertEqual(result, 0)
        
    def test_add_single_argument(self):
        """Test addition with single argument"""
        result = add(7)
        self.assertEqual(result, 7)
        
    def test_add_type_error(self):
        """Test addition with invalid type"""
        with self.assertRaises(TypeError):
            add(5, "hello")
    
    # Updated tests for multiply function (now supports multiple arguments)
    def test_multiply_two_numbers(self):
        """Test multiplication of two numbers"""
        result = multiply(4, 5)
        self.assertEqual(result, 20)
        
    def test_multiply_multiple_numbers(self):
        """Test multiplication of multiple numbers"""
        result = multiply(2, 3, 4)
        self.assertEqual(result, 24)
        
    def test_multiply_no_arguments(self):
        """Test multiplication with no arguments"""
        result = multiply()
        self.assertEqual(result, 1)
        
    def test_multiply_type_error(self):
        """Test multiplication with invalid type"""
        with self.assertRaises(TypeError):
            multiply(5, "hello")
    
    # Updated tests for divide function (now supports precision)
    def test_divide_with_precision(self):
        """Test division with precision control"""
        result = divide(10, 3, precision=2)
        self.assertEqual(result, 3.33)
        
    def test_divide_type_error(self):
        """Test division with invalid types"""
        with self.assertRaises(TypeError):
            divide("10", 2)
            
    def test_divide_invalid_precision(self):
        """Test division with invalid precision"""
        with self.assertRaises(ValueError):
            divide(10, 2, precision=-1)
    
    # Tests for enhanced type checking
    def test_subtract_type_error(self):
        """Test subtraction with invalid types"""
        with self.assertRaises(TypeError):
            subtract(5, "hello")
            
    def test_power_type_error(self):
        """Test power with invalid types"""
        with self.assertRaises(TypeError):
            power("2", 3)

if __name__ == '__main__':
    unittest.main()
