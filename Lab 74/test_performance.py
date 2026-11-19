import unittest
import time
import random
from sorting import sort_numbers, sort_numbers_desc, flexible_sort

class TestSortingPerformance(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.small_list = [random.randint(1, 100) for _ in range(100)]
        self.medium_list = [random.randint(1, 1000) for _ in range(1000)]
        self.large_list = [random.randint(1, 10000) for _ in range(10000)]
    
    def test_small_list_performance(self):
        """Test performance with small list"""
        start_time = time.time()
        result = sort_numbers(self.small_list)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)  # Should complete in less than 1 second
        self.assertEqual(len(result), len(self.small_list))
    
    def test_medium_list_performance(self):
        """Test performance with medium list"""
        start_time = time.time()
        result = flexible_sort(self.medium_list)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertLess(execution_time, 2.0)  # Should complete in less than 2 seconds
        self.assertEqual(len(result), len(self.medium_list))
    
    def test_correctness_with_large_dataset(self):
        """Test correctness with large dataset"""
        result = sort_numbers(self.large_list)
        
        # Verify the result is actually sorted
        for i in range(1, len(result)):
            self.assertLessEqual(result[i-1], result[i])
        
        # Verify all elements are preserved
        self.assertEqual(len(result), len(self.large_list))
        self.assertEqual(sorted(self.large_list), result)

if __name__ == '__main__':
    unittest.main()
