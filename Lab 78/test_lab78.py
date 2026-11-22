import asyncio
import unittest

import aiohttp
from async_example import slow_operation_async
from async_error_handling import safe_operation
from gather_demo import download_url, gather_example_4
from http_fixture import local_site
from performance_comparison import run_async_cpu, run_async_io


class AsyncioTests(unittest.IsolatedAsyncioTestCase):
    async def test_gather_returns_input_order(self):
        result = await asyncio.gather(slow_operation_async("A", 0.03), slow_operation_async("B", 0.01))
        self.assertEqual(result, ["Result from A", "Result from B"])

    async def test_errors_are_isolated(self):
        result = await asyncio.gather(safe_operation(1), safe_operation(2))
        self.assertEqual([item["status"] for item in result], ["success", "failed"])

    async def test_real_http_success_and_error(self):
        with local_site() as base:
            async with aiohttp.ClientSession() as session:
                ok, failure = await asyncio.gather(download_url(session, base + "/json", "ok"), download_url(session, base + "/status/503", "bad"))
        self.assertEqual(ok["status"], 200)
        self.assertGreater(ok["bytes"], 0)
        self.assertEqual(failure["status"], "error")

    async def test_http_timeout(self):
        with local_site() as base:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=0.02)) as session:
                result = await download_url(session, base + "/slow", "slow")
        self.assertEqual(result["status"], "error")

    async def test_actual_file_read_write(self):
        await gather_example_4()

    async def test_io_benchmark_returns_each_task(self):
        self.assertEqual(await run_async_io(5, 0.01), [0, 1, 2, 3, 4])

    async def test_cpu_executor_returns_correct_sums(self):
        result = await run_async_cpu(2, 1000)
        total = 999 * 1000 * 1999 // 6
        self.assertEqual(result, [(0, total), (1, total)])


if __name__ == "__main__":
    unittest.main()
