import contextlib
import io
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

import counter_with_lock
from deadlock_prevention import worker_timeout_approach, worker_try_lock_approach
from producer_consumer import SafeBuffer


class SynchronizationTests(unittest.TestCase):
    def test_both_counter_lock_styles(self):
        for function in (counter_with_lock.increment_counter_safe, counter_with_lock.increment_counter_manual_lock):
            with self.subTest(function=function.__name__):
                counter_with_lock.counter = 0
                with contextlib.redirect_stdout(io.StringIO()):
                    with ThreadPoolExecutor(max_workers=3) as executor:
                        list(executor.map(lambda i: function(f"T{i}", 50), range(3)))
                self.assertEqual(counter_with_lock.counter, 150)

    def test_bounded_buffer_transfers_every_item_once(self):
        buffer = SafeBuffer(max_size=2)
        def produce():
            for item in range(20):
                buffer.put(item)
        def consume():
            return [buffer.get() for _ in range(10)]
        with contextlib.redirect_stdout(io.StringIO()):
            with ThreadPoolExecutor(max_workers=3) as executor:
                producer = executor.submit(produce)
                first, second = executor.submit(consume), executor.submit(consume)
                actual = first.result(timeout=5) + second.result(timeout=5)
                producer.result(timeout=5)
        self.assertEqual(sorted(actual), list(range(20)))
        self.assertEqual(buffer.size(), 0)

    def test_invalid_buffer_capacity(self):
        with self.assertRaises(ValueError):
            SafeBuffer(0)

    def test_timeout_releases_first_lock(self):
        first, second = threading.Lock(), threading.Lock()
        with second:
            self.assertFalse(worker_timeout_approach(first, second))
        self.assertFalse(first.locked())
        self.assertFalse(second.locked())

    def test_try_lock_exhaustion_is_reported(self):
        first, second = threading.Lock(), threading.Lock()
        with second:
            self.assertFalse(worker_try_lock_approach(first, second))
        self.assertFalse(first.locked())


if __name__ == "__main__":
    unittest.main()
