import contextlib
import io
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

import advanced_threading
from advanced_locks import ResourcePool
import gil_demonstration
import thread_synchronization as synchronization


class ThreadingTests(unittest.TestCase):
    def test_worker_pool_processes_each_task_once(self):
        with contextlib.redirect_stdout(io.StringIO()):
            completed = advanced_threading.worker_pool_example()
        self.assertEqual(len(completed), 10)
        self.assertEqual(set(completed), {f"Task-{i}" for i in range(1, 11)})

    def test_locked_counter_has_no_lost_updates(self):
        synchronization.shared_counter = 0
        with contextlib.redirect_stdout(io.StringIO()):
            with ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(lambda i: synchronization.safe_increment(f"T{i}", 50), range(4)))
        self.assertEqual(synchronization.shared_counter, 200)

    def test_bank_transactions_preserve_balance(self):
        account = synchronization.BankAccount(1000)
        with contextlib.redirect_stdout(io.StringIO()):
            with ThreadPoolExecutor(max_workers=8) as pool:
                list(pool.map(lambda i: account.deposit(10, f"D{i}"), range(8)))
            with ThreadPoolExecutor(max_workers=8) as pool:
                accepted = list(pool.map(lambda i: account.withdraw(200, f"W{i}"), range(8)))
        self.assertEqual(account.get_balance(), 80)
        self.assertEqual(sum(accepted), 5)
        self.assertEqual(len(account.transaction_history), 13)

    def test_invalid_bank_amounts_rejected(self):
        account = synchronization.BankAccount()
        for amount in (0, -1):
            with self.assertRaises(ValueError):
                account.deposit(amount, "test")
            with self.assertRaises(ValueError):
                account.withdraw(amount, "test")

    def test_resource_capacity_and_double_release(self):
        with contextlib.redirect_stdout(io.StringIO()):
            pool = ResourcePool(2)
            first, second = pool.acquire_resource("A"), pool.acquire_resource("B")
            self.assertNotEqual(first, second)
            self.assertIsNone(pool.acquire_resource("C"))
            self.assertTrue(pool.release_resource(first, "A"))
            self.assertFalse(pool.release_resource(first, "A"))
            self.assertTrue(pool.release_resource(second, "B"))
        self.assertEqual(pool.get_status()["available"], 2)
        with self.assertRaises(ValueError):
            ResourcePool(0)

    def test_cpu_calculation_against_closed_form(self):
        with contextlib.redirect_stdout(io.StringIO()):
            actual = gil_demonstration.cpu_bound_task(1000, "test")
        self.assertEqual(actual, 999 * 1000 * 1999 // 6)


if __name__ == "__main__":
    unittest.main()
