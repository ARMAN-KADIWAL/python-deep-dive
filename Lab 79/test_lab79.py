import asyncio
import tempfile
import unittest
from pathlib import Path

from async_scraper import AsyncWebScraper
from enhanced_scraper import EnhancedAsyncScraper, Status
from http_fixture import local_site
from main import main
from page_parser import parse_page
from sync_scraper import SyncWebScraper


class ParserTests(unittest.TestCase):
    def test_missing_title_and_empty_anchor(self):
        result = parse_page("local", 200, "<p>Hello</p><a href='/a'>A</a><a href='/b'></a>")
        self.assertEqual(result["title"], "No title")
        self.assertEqual(result["paragraph_count"], 1)
        self.assertEqual(result["link_count"], 2)


class ScraperTests(unittest.IsolatedAsyncioTestCase):
    async def test_async_and_sync_extract_identical_fields(self):
        with local_site() as base:
            async with AsyncWebScraper() as scraper:
                asynchronous = await scraper.scrape_page(base + "/html")
            with SyncWebScraper() as scraper:
                synchronous = scraper.scrape_page(base + "/html")
        asynchronous.pop("scraped_at")
        synchronous.pop("scraped_at")
        self.assertEqual(asynchronous, synchronous)
        self.assertEqual(asynchronous["link_count"], 2)

    async def test_http_404_is_not_retried(self):
        with local_site() as base:
            async with EnhancedAsyncScraper(backoff=0.01) as scraper:
                result = await scraper.scrape_page(base + "/status/404")
        self.assertIs(result.status, Status.HTTP_ERROR)
        self.assertEqual(result.attempts, 1)

    async def test_transient_failure_is_retried(self):
        with local_site() as base:
            async with EnhancedAsyncScraper(backoff=0.01) as scraper:
                result = await scraper.scrape_page(base + "/flaky")
        self.assertIs(result.status, Status.SUCCESS)
        self.assertEqual(result.attempts, 2)
        self.assertIsNone(result.error_msg)

    async def test_timeout_status(self):
        with local_site() as base:
            async with EnhancedAsyncScraper(timeout=0.02) as scraper:
                result = await scraper.scrape_page(base + "/slow", retries=0)
        self.assertIs(result.status, Status.TIMEOUT)

    async def test_parse_error_status(self):
        def broken_parser(*args):
            raise ValueError("Intentional parser failure")
        with local_site() as base:
            async with EnhancedAsyncScraper() as scraper:
                scraper._parse = broken_parser
                result = await scraper.scrape_page(base + "/html")
        self.assertIs(result.status, Status.PARSE_ERR)

    async def test_context_manager_required(self):
        with self.assertRaises(RuntimeError):
            await AsyncWebScraper().scrape_page("http://127.0.0.1/")

    async def test_invalid_configuration(self):
        with self.assertRaises(ValueError):
            AsyncWebScraper(max_concurrent=0)
        with self.assertRaises(ValueError):
            SyncWebScraper(timeout=0)

    async def test_comparison_requires_full_url_coverage(self):
        with local_site() as base, tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(RuntimeError):
                await main([base + "/status/404"], str(Path(directory) / "report.json"))


if __name__ == "__main__":
    unittest.main()
