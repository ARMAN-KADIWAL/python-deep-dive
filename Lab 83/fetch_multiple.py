#!/usr/bin/env python3
"""
Fetching Multiple Records Example
This script demonstrates fetching and processing multiple API records
"""

import requests

def fetch_multiple_posts():
    """Fetch multiple posts and display specific information"""
    
    url = "https://jsonplaceholder.typicode.com/posts"
    
    print("Fetching all posts from API...")
    print("-" * 40)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        posts = response.json()
        print(f"✓ Successfully fetched {len(posts)} posts")
        
        # Display first 5 posts with specific information
        print("\nFirst 5 Posts:")
        print("=" * 60)
        
        for post in posts[:5]:
            print(f"Post ID: {post['id']}")
            print(f"User ID: {post['userId']}")
            print(f"Title: {post['title'][:50]}...")
            print(f"Body: {post['body'][:100]}...")
            print("-" * 40)
    else:
        print(f"✗ Failed to fetch posts. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_multiple_posts()
