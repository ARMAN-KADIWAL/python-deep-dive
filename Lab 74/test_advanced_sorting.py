import unittest
from sorting import sort_numbers, sort_numbers_desc, flexible_sort

class TestAdvancedSorting(unittest.TestCase):
    
    def test_sort_descending_basic(self):
        """Test sorting in descending order"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [9, 6, 5, 4, 3, 2, 1, 1]
        result = sort_numbers_desc(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_descending_empty(self):
        """Test sorting empty list in descending order"""
        input_list = []
        expected = []
        result = sort_numbers_desc(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_descending_single(self):
        """Test sorting single element in descending order"""
        input_list = [42]
        expected = [42]
        result = sort_numbers_desc(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_descending_with_negatives(self):
        """Test sorting with negative numbers in descending order"""
        input_list = [-3, 1, -4, 0, 5, -2]
        expected = [5, 1, 0, -2, -3, -4]
        result = sort_numbers_desc(input_list)
        self.assertEqual(result, expected)

    def test_flexible_sort_ascending(self):
        """Test flexible sort function with ascending order"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [1, 1, 2, 3, 4, 5, 6, 9]
        result = flexible_sort(input_list, ascending=True)
        self.assertEqual(result, expected)
    
    def test_flexible_sort_descending(self):
        """Test flexible sort function with descending order"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [9, 6, 5, 4, 3, 2, 1, 1]
        result = flexible_sort(input_list, ascending=False)
        self.assertEqual(result, expected)
    
    def test_flexible_sort_default_ascending(self):
        """Test flexible sort function with default ascending order"""
        input_list = [3, 1, 4, 1, 5]
        expected = [1, 1, 3, 4, 5]
        result = flexible_sort(input_list)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
