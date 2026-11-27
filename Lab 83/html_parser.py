#!/usr/bin/env python3
"""
HTML Parsing Example
This script demonstrates parsing HTML content to extract information
"""

import requests
from bs4 import BeautifulSoup

def parse_html_content():
    """Parse HTML content and extract specific elements"""
    
    url = "https://httpbin.org/html"
    
    print("Fetching and parsing HTML content...")
    print("-" * 50)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("✓ HTML parsed successfully")
        
        # Extract title
        title = soup.find('title')
        if title:
            print(f"Page Title: {title.text}")
        
        # Extract all headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if headings:
            print(f"\nFound {len(headings)} headings:")
            for heading in headings:
                print(f"  • {heading.name.upper()}: {heading.text.strip()}")
        
        # Extract all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            print(f"\nFound {len(paragraphs)} paragraphs:")
            for i, p in enumerate(paragraphs, 1):
                text = p.text.strip()[:100]  # First 100 characters
                print(f"  {i}. {text}...")
        
        # Extract all links
        links = soup.find_all('a', href=True)
        if links:
            print(f"\nFound {len(links)} links:")
            for link in links:
                print(f"  • {link.text.strip()} -> {link['href']}")
    
    else:
        print(f"✗ Failed to fetch HTML. Status code: {response.status_code}")

def extract_quotes_example():
    """Extract quotes from a quotes website (example)"""
    
    # Using a simple HTML test page
    html_content = """
    <html>
    <body>
        <div class="quote">
            <span class="text">"The way to get started is to quit talking and begin doing."</span>
            <span class="author">Walt Disney</span>
        </div>
        <div class="quote">
            <span class="text">"Life is what happens to you while you're busy making other plans."</span>
            <span class="author">John Lennon</span>
        </div>
    </body>
    </html>
    """
    
    print("\nParsing quotes from HTML...")
    print("-" * 40)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    quotes = soup.find_all('div', class_='quote')
    
    print(f"Found {len(quotes)} quotes:")
    
    for i, quote in enumerate(quotes, 1):
        text = quote.find('span', class_='text').text
        author = quote.find('span', class_='author').text
        print(f"\n{i}. {text}")
        print(f"   - {author}")

if __name__ == "__main__":
    parse_html_content()
    extract_quotes_example()
