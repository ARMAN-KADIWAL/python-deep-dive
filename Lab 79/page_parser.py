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
