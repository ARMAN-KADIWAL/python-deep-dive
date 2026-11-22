# Lab 79: Advanced Asyncio -- Building an Async Web Scraper — Complete Guide

Fetch pages with asyncio/aiohttp and a synchronous requests baseline, parse identical HTML fields, retry transient failures and report per-URL outcomes.

Async aur sync versions same URLs aur same parser use karte hain. 404 ko baar-baar retry nahi karte; 429 aur server errors par bounded backoff hai. Offline mode bhi actual HTTP sockets use karta hai, bas server local controlled fixture hota hai. Incomplete results par speedup claim nahi hota.

Follow [README.md](README.md) for setup, commands, ports and validation. These are the complete final modules, not the intermediate/truncated snippets from the supplied handout.

## async_scraper.py

```python
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
```

## enhanced_scraper.py

```python
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
```

## http_fixture.py

```python
import threading
import time
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


@contextmanager
def local_site(delay=0.03):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            path = urlparse(self.path).path
            status = 200
            if path.startswith("/delay/"):
                time.sleep(float(path.rsplit("/", 1)[1]))
            elif path == "/slow":
                time.sleep(0.2)
            else:
                time.sleep(delay)
            if path == "/flaky":
                with self.server.counter_lock:
                    self.server.flaky_count += 1
                    status = 503 if self.server.flaky_count == 1 else 200
            elif path.startswith("/status/"):
                status = int(path.rsplit("/", 1)[1])
            body = (
                f"<html><head><title>Fixture {path}</title></head><body>"
                "<h1>Local lab fixture</h1><p>First paragraph.</p>"
                "<p>Second paragraph.</p><a href='/next'>Next</a>"
                "<a href='/empty'></a><img src='/image.png'></body></html>"
            ).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    server.counter_lock = threading.Lock()
    server.flaky_count = 0
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.05), daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
```

## main.py

```python
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
```

## page_parser.py

```python
import time
from bs4 import BeautifulSoup


def parse_page(url, status, html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")
    paragraphs = [tag.get_text(strip=True) for tag in soup.find_all("p") if tag.get_text(strip=True)]
    links = [{"text": tag.get_text(strip=True), "href": tag["href"]} for tag in soup.find_all("a", href=True)]
    headings = len(soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]))
    images = len(soup.find_all("img"))
    return {
        "url": url, "status": status,
        "title": title.get_text(strip=True) if title else "No title",
        "content_length": len(html), "paragraph_count": len(paragraphs),
        "first_paragraphs": paragraphs[:3], "link_count": len(links),
        "sample_links": links[:5], "scraped_at": time.time(),
        "element_counts": {"headings": headings, "images": images,
                           "links": len(links), "paragraphs": len(paragraphs)},
    }
```

## sync_scraper.py

```python
import time

import requests
from page_parser import parse_page


class SyncWebScraper:
    def __init__(self, timeout=30, backoff=1):
        if timeout <= 0 or backoff < 0:
            raise ValueError("Use positive timeout and non-negative backoff")
        self.timeout = timeout
        self.backoff = backoff
        self.session = requests.Session()
        self.scraped_data = []
        self.failures = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.session.close()

    def scrape_page(self, url, retries=3):
        if retries < 0:
            raise ValueError("retries must be non-negative")
        for attempt in range(retries + 1):
            retryable = True
            try:
                with self.session.get(url, timeout=self.timeout) as response:
                    if response.status_code == 200:
                        return parse_page(url, response.status_code, response.text)
                    retryable = response.status_code == 429 or response.status_code >= 500
            except requests.RequestException:
                pass
            if not retryable or attempt == retries:
                break
            time.sleep(self.backoff * 2 ** attempt)
        return None

    def scrape_many(self, urls):
        self.scraped_data = []
        self.failures = []
        for url in urls:
            result = self.scrape_page(url)
            if result is None:
                self.failures.append(url)
            else:
                self.scraped_data.append(result)
        return self.scraped_data

    def print_summary(self):
        print(f"Sync: {len(self.scraped_data)} succeeded; {len(self.failures)} failed")
        for page in self.scraped_data:
            print(f"{page['title']} | {page['link_count']} links | {page['content_length']} characters")
```

