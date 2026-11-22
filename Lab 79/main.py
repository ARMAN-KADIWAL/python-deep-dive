import argparse
import asyncio
import json
import time
from collections import Counter
from pathlib import Path

from async_scraper import AsyncWebScraper
from sync_scraper import SyncWebScraper


ENDPOINTS = ("html", "json", "xml", "robots.txt", "headers", "ip", "user-agent", "uuid")


async def run_async(urls):
    started = time.perf_counter()
    async with AsyncWebScraper(max_concurrent=8) as scraper:
        results = await scraper.scrape_many(urls)
        scraper.print_summary()
    return results, time.perf_counter() - started


def run_sync(urls):
    started = time.perf_counter()
    with SyncWebScraper() as scraper:
        results = scraper.scrape_many(urls)
        scraper.print_summary()
    return results, time.perf_counter() - started


async def main(urls, output="scraping_results.json"):
    async_results, async_time = await run_async(urls)
    loop = asyncio.get_running_loop()
    sync_results, sync_time = await loop.run_in_executor(None, run_sync, urls)
    expected = Counter(urls)
    comparable = bool(urls) and Counter(page["url"] for page in async_results) == expected and Counter(page["url"] for page in sync_results) == expected
    report = {"async_seconds": async_time, "sync_seconds": sync_time,
              "async_pages": len(async_results), "sync_pages": len(sync_results),
              "comparable": comparable, "async_results": async_results,
              "sync_results": sync_results}
    Path(output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    if not comparable:
        raise RuntimeError("Incomplete URL coverage; timing comparison is not valid. Inspect the report.")
    ratio = sync_time / async_time
    print(f"Sync: {sync_time:.3f}s; async: {async_time:.3f}s; sync/async ratio: {ratio:.2f}x")
    print("A ratio above 1 means async was faster in this run; performance depends on workload and server.")
    print("PASS: Both approaches fetched the complete identical URL list.")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--base-url", default="https://httpbin.org")
    parser.add_argument("--output", default="scraping_results.json")
    args = parser.parse_args()
    if args.offline:
        from http_fixture import local_site
        with local_site() as base_url:
            asyncio.run(main([f"{base_url}/{name}" for name in ENDPOINTS], args.output))
    else:
        asyncio.run(main([f"{args.base_url.rstrip('/')}/{name}" for name in ENDPOINTS], args.output))
