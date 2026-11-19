"""
Test Suite for Arithmetic Operations
Demonstrates how to organize and run multiple test classes
"""

import unittest
from test_arithmetic_operations_refactored import TestRefactoredArithmeticOperations
from test_assertions_demo import TestAssertionMethods

def create_test_suite():
    """Create a test suite containing all test cases"""
    suite = unittest.TestSuite()
    
    # Add specific test methods
    suite.addTest(TestRefactoredArithmeticOperations('test_add_two_positive_numbers'))
    suite.addTest(TestRefactoredArithmeticOperations('test_multiply_multiple_numbers'))
    suite.addTest(TestRefactoredArithmeticOperations('test_divide_with_precision'))
    
    # Add all tests from a test class
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAssertionMethods))
    
    return suite

def create_addition_test_suite():
    """Create a test suite for addition tests only"""
    suite = unittest.TestSuite()
    
    # Add only addition-related tests
    suite.addTest(TestRefactoredArithmeticOperations('test_add_two_positive_numbers'))
    suite.addTest(TestRefactoredArithmeticOperations('test_add_multiple_numbers'))
    suite.addTest(TestRefactoredArithmeticOperations('test_add_no_arguments'))
    suite.addTest(TestRefactoredArithmeticOperations('test_add_single_argument'))
    
    return suite

if __name__ == '__main__':
    # Run the full test suite
    runner = unittest.TextTestRunner(verbosity=2)
    
    print("Running Full Test Suite:")
    print("=" * 50)
    result = runner.run(create_test_suite())
    
    print("\nRunning Addition Test Suite:")
    print("=" * 50)
    result = runner.run(create_addition_test_suite())
