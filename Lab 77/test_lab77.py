import math
import multiprocessing as mp
import unittest
from unittest.mock import patch

import advanced_multiprocessing
import parallel_factorial
import process_pool_demo
import queue_communication


class MultiprocessingTests(unittest.TestCase):
    def tearDown(self):
        self.assertEqual(mp.active_children(), [])

    def test_factorial_methods_match_math(self):
        for n in (0, 1, 2, 10, 100, 1000):
            with self.subTest(n=n):
                expected = math.factorial(n)
                self.assertEqual(parallel_factorial.parallel_factorial(n, 3), expected)
                self.assertEqual(parallel_factorial.optimized_parallel_factorial(n, 3), expected)

    def test_factorial_invalid_arguments(self):
        for function in (parallel_factorial.parallel_factorial, parallel_factorial.optimized_parallel_factorial):
            with self.assertRaises(ValueError):
                function(-1)
            with self.assertRaises(ValueError):
                function(10, 0)
            with self.assertRaises(TypeError):
                function(2.5)

    def test_starmap_worker_is_spawn_picklable(self):
        with mp.get_context("spawn").Pool(2) as pool:
            result = pool.starmap(process_pool_demo.multiply_task, [(2, 3, "A"), (4, 5, "B")])
        self.assertEqual(result, [6, 20])

    def test_queue_items_are_not_lost_or_duplicated(self):
        result = queue_communication.demonstrate_basic_queue()
        self.assertEqual(sorted(result), [(i, j) for i in range(2) for j in range(3)])

    def test_bidirectional_queue_returns_all_squares(self):
        result = queue_communication.demonstrate_bidirectional_queue()
        self.assertEqual(sorted(result), [(i, n * n) for i, n in enumerate((5, 10, 15, 20, 25))])

    def test_shared_memory_result_and_cleanup(self):
        names = []
        original = advanced_multiprocessing.shared_memory.SharedMemory
        def record(*args, **kwargs):
            memory = original(*args, **kwargs)
            if kwargs.get("create"):
                names.append(memory.name)
            return memory
        with patch.object(advanced_multiprocessing.shared_memory, "SharedMemory", side_effect=record):
            result = advanced_multiprocessing.demonstrate_shared_memory()
        self.assertEqual(result, [i * i for i in range(1, 11)])
        self.assertEqual(len(names), 1)
        with self.assertRaises(FileNotFoundError):
            original(name=names[0])


if __name__ == "__main__":
    unittest.main()
