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
