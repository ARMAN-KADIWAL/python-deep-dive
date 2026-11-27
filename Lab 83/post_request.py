#!/usr/bin/env python3
"""
HTTP POST Request Example
This script demonstrates sending data via POST request
"""

import requests
import json

def create_new_post():
    """Create a new post using POST request"""
    
    url = "https://jsonplaceholder.typicode.com/posts"
    
    # Data to send in the POST request
    post_data = {
        "title": "My First API Post",
        "body": "This is the content of my post created via Python!",
        "userId": 1
    }
    
    print("Creating new post...")
    print("Data to send:")
    print(json.dumps(post_data, indent=2))
    print("-" * 50)
    
    # Send POST request with JSON data
    response = requests.post(url, json=post_data)
    
    if response.status_code == 201:  # 201 = Created
        print("✓ Post created successfully!")
        print(f"Status Code: {response.status_code}")
        print("\nServer Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Failed to create post. Status code: {response.status_code}")

def update_existing_post():
    """Update an existing post using PUT request"""
    
    post_id = 1
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    
    updated_data = {
        "id": post_id,
        "title": "Updated Post Title",
        "body": "This post has been updated via Python PUT request!",
        "userId": 1
    }
    
    print(f"\nUpdating post {post_id}...")
    print("Updated data:")
    print(json.dumps(updated_data, indent=2))
    print("-" * 50)
    
    response = requests.put(url, json=updated_data)
    
    if response.status_code == 200:
        print("✓ Post updated successfully!")
        print("\nServer Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Failed to update post. Status code: {response.status_code}")

if __name__ == "__main__":
    create_new_post()
    update_existing_post()
