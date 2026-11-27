#!/usr/bin/env python3
"""
Basic HTTP GET Request Example
This script demonstrates how to make a simple GET request to a public API
"""

import requests
import json

def make_basic_get_request():
    """Make a basic GET request to JSONPlaceholder API"""
    
    # JSONPlaceholder is a free fake API for testing
    url = "https://jsonplaceholder.typicode.com/posts/1"
    
    print("Making GET request to:", url)
    print("-" * 50)
    
    # Send GET request
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        print("✓ Request successful!")
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type')}")
        print("\nResponse Data:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Request failed with status code: {response.status_code}")

if __name__ == "__main__":
    make_basic_get_request()
