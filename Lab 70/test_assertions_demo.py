"""
Demonstration of various unittest assertion methods
"""

import unittest
from arithmetic_operations import add, divide

class TestAssertionMethods(unittest.TestCase):
    """Demonstrate different assertion methods"""
    
    def test_assertEqual_demo(self):
        """Demonstrate assertEqual"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual("hello", "hello")
        
    def test_assertNotEqual_demo(self):
        """Demonstrate assertNotEqual"""
        self.assertNotEqual(add(2, 3), 6)
        self.assertNotEqual("hello", "world")
        
    def test_assertTrue_demo(self):
        """Demonstrate assertTrue"""
        self.assertTrue(add(2, 3) > 0)
        self.assertTrue(isinstance(add(1, 2), int))
        
    def test_assertFalse_demo(self):
        """Demonstrate assertFalse"""
        self.assertFalse(add(2, 3) < 0)
        self.assertFalse(add(1, 1) == 3)
        
    def test_assertAlmostEqual_demo(self):
        """Demonstrate assertAlmostEqual for floating point comparisons"""
        result = divide(1, 3)
        self.assertAlmostEqual(result, 0.333333, places=5)
        
    def test_assertGreater_demo(self):
        """Demonstrate assertGreater and assertLess"""
        self.assertGreater(add(5, 3), 7)
        self.assertLess(add(2, 1), 5)
        
    def test_assertIn_demo(self):
        """Demonstrate assertIn and assertNotIn"""
        result_str = str(add(2, 3))
        self.assertIn('5', result_str)
        self.assertNotIn('6', result_str)
        
    def test_assertIsInstance_demo(self):
        """Demonstrate assertIsInstance"""
        result = add(2, 3)
        self.assertIsInstance(result, int)
        
        float_result = divide(5, 2)
        self.assertIsInstance(float_result, float)

if __name__ == '__main__':
    unittest.main()
