import argparse
import asyncio
from dataclasses import dataclass
from enum import Enum

from async_scraper import AsyncWebScraper


class Status(Enum):
    SUCCESS = "success"
    HTTP_ERROR = "http_error"
    TIMEOUT = "timeout"
    PARSE_ERR = "parse_error"
    FAILED = "failed"


@dataclass
class ScrapingResult:
    url: str
    status: Status = Status.FAILED
    data: object = None
    error_msg: object = None
    attempts: int = 0
    elapsed: float = 0.0


class EnhancedAsyncScraper(AsyncWebScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results = []

    async def scrape_page(self, url, retries=3):
        result = await self._fetch_result(url, retries)
        result["status"] = Status(result["status"])
        return ScrapingResult(**result)

    async def scrape_many(self, urls):
        self.results = await asyncio.gather(*(self.scrape_page(url) for url in urls))
        return self.results

    def print_stats(self):
        succeeded = sum(result.status is Status.SUCCESS for result in self.results)
        print(f"Total: {len(self.results)}; succeeded: {succeeded}; failed: {len(self.results) - succeeded}")
        for result in self.results:
            print(f"{result.status.value}: {result.url}; attempts={result.attempts}; {result.elapsed:.3f}s; {result.error_msg or 'OK'}")


async def demo(base_url):
    urls = [f"{base_url}/html", f"{base_url}/json", f"{base_url}/xml", f"{base_url}/status/404", f"{base_url}/uuid"]
    async with EnhancedAsyncScraper(max_concurrent=5) as scraper:
        results = await scraper.scrape_many(urls)
        scraper.print_stats()
    if [result.status for result in results] != [Status.SUCCESS] * 3 + [Status.HTTP_ERROR, Status.SUCCESS]:
        raise RuntimeError("Unexpected demo outcomes; check server/network availability")
    print("PASS: Four successful requests and the intentional HTTP 404 were identified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--base-url", default="https://httpbin.org")
    args = parser.parse_args()
    if args.offline:
        from http_fixture import local_site
        with local_site() as base_url:
            asyncio.run(demo(base_url))
    else:
        asyncio.run(demo(args.base_url.rstrip("/")))
