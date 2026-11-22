import asyncio
import time

import aiohttp
from page_parser import parse_page


class AsyncWebScraper:
    _parse = staticmethod(parse_page)

    def __init__(self, max_concurrent=10, timeout=30, backoff=1):
        if max_concurrent < 1 or timeout <= 0 or backoff < 0:
            raise ValueError("Use positive concurrency/timeout and non-negative backoff")
        self.max_concurrent = max_concurrent
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.backoff = backoff
        self.session = None
        self.scraped_data = []
        self.failures = []

    async def __aenter__(self):
        if self.session is not None:
            raise RuntimeError("Scraper is already open")
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        self.session = aiohttp.ClientSession(connector=connector, timeout=self.timeout)
        return self

    async def __aexit__(self, *args):
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def _fetch_result(self, url, retries=3):
        if self.session is None or self.session.closed:
            raise RuntimeError("Use 'async with AsyncWebScraper() as scraper'")
        if retries < 0:
            raise ValueError("retries must be non-negative")
        started = time.perf_counter()
        result = {"url": url, "status": "failed", "data": None,
                  "error_msg": None, "attempts": 0, "elapsed": 0.0}
        for attempt in range(retries + 1):
            result["attempts"] = attempt + 1
            retryable = True
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        try:
                            result["data"] = self._parse(url, response.status, html)
                            result["status"] = "success"
                            result["error_msg"] = None
                        except Exception as error:
                            result["status"] = "parse_error"
                            result["error_msg"] = str(error)
                        break
                    result["status"] = "http_error"
                    result["error_msg"] = f"HTTP {response.status}"
                    retryable = response.status == 429 or response.status >= 500
            except asyncio.TimeoutError:
                result["status"], result["error_msg"] = "timeout", "Request timed out"
            except aiohttp.ClientError as error:
                result["status"], result["error_msg"] = "failed", str(error)
            if not retryable or attempt == retries:
                break
            await asyncio.sleep(self.backoff * 2 ** attempt)
        result["elapsed"] = time.perf_counter() - started
        return result

    async def scrape_page(self, url, retries=3):
        result = await self._fetch_result(url, retries)
        return result["data"] if result["status"] == "success" else None

    async def scrape_many(self, urls):
        records = await asyncio.gather(*(self._fetch_result(url) for url in urls))
        self.scraped_data = [record["data"] for record in records if record["status"] == "success"]
        self.failures = [record for record in records if record["status"] != "success"]
        return self.scraped_data

    def print_summary(self):
        print(f"Async: {len(self.scraped_data)} succeeded; {len(self.failures)} failed")
        for page in self.scraped_data:
            print(f"{page['title']} | {page['link_count']} links | {page['content_length']} characters")
