import unittest
from sorting import sort_numbers

class TestSortNumbers(unittest.TestCase):
    
    def test_sort_basic_list(self):
        """Test sorting a basic list of numbers"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [1, 1, 2, 3, 4, 5, 6, 9]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_single_element(self):
        """Test sorting a list with single element"""
        input_list = [42]
        expected = [42]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_two_elements(self):
        """Test sorting a list with two elements"""
        input_list = [5, 2]
        expected = [2, 5]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)

    def test_sort_empty_list(self):
        """Test sorting an empty list"""
        input_list = []
        expected = []
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_already_sorted(self):
        """Test sorting an already sorted list"""
        input_list = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_reverse_sorted(self):
        """Test sorting a reverse sorted list"""
        input_list = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_with_duplicates(self):
        """Test sorting a list with duplicate values"""
        input_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_sort_with_negative_numbers(self):
        """Test sorting a list with negative numbers"""
        input_list = [-3, 1, -4, 0, 5, -2]
        expected = [-4, -3, -2, 0, 1, 5]
        result = sort_numbers(input_list)
        self.assertEqual(result, expected)
    
    def test_original_list_unchanged(self):
        """Test that the original list is not modified"""
        input_list = [3, 1, 4, 1, 5]
        original_copy = input_list.copy()
        sort_numbers(input_list)
        self.assertEqual(input_list, original_copy)


    def test_sort_non_list_input(self):
        """Test that non-list input raises TypeError"""
        with self.assertRaises(TypeError):
            sort_numbers("not a list")
    
    def test_sort_non_numeric_elements(self):
        """Test that non-numeric elements raise TypeError"""
        with self.assertRaises(TypeError):
            sort_numbers([1, 2, "three", 4])


if __name__ == '__main__':
    unittest.main()
