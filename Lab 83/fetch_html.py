#!/usr/bin/env python3
"""
HTML Content Fetching Example
This script demonstrates fetching HTML content from websites
"""

import requests
from urllib.parse import urljoin, urlparse

def fetch_website_html():
    """Fetch HTML content from a website"""
    
    url = "https://httpbin.org/html"  # A simple HTML test page
    
    print(f"Fetching HTML content from: {url}")
    print("-" * 60)
    
    # Add headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Ubuntu) Python-Requests/2.28'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("✓ Successfully fetched HTML content")
        print(f"Content Length: {len(response.text)} characters")
        print(f"Content Type: {response.headers.get('content-type')}")
        
        print("\nFirst 500 characters of HTML:")
        print("=" * 50)
        print(response.text[:500])
        print("...")
        
        # Count specific HTML elements
        html_content = response.text.lower()
        print(f"\nHTML Analysis:")
        print(f"  • <p> tags: {html_content.count('<p>')}")
        print(f"  • <div> tags: {html_content.count('<div>')}")
        print(f"  • <a> tags: {html_content.count('<a>')}")
        
    else:
        print(f"✗ Failed to fetch HTML. Status code: {response.status_code}")

def fetch_multiple_pages():
    """Fetch content from multiple pages"""
    
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://httpbin.org/xml"
    ]
    
    print("\nFetching content from multiple URLs...")
    print("=" * 60)
    
    for url in urls:
        print(f"\nProcessing: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', 'unknown')
                print(f"✓ Success - Content Type: {content_type}")
                print(f"  Content Length: {len(response.text)} characters")
                
                # Show first line of content
                first_line = response.text.split('\n')[0][:100]
                print(f"  First line: {first_line}...")
            else:
                print(f"✗ Failed - Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    fetch_website_html()
    fetch_multiple_pages()
