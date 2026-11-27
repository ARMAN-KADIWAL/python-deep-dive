#!/usr/bin/env python3
"""
Headers and Authentication Example
This script demonstrates working with HTTP headers and authentication
"""

import requests
import base64
import json

def demonstrate_headers():
    """Demonstrate working with HTTP headers"""
    
    print("Working with HTTP Headers")
    print("=" * 50)
    
    # URL that echoes back request information
    url = "https://httpbin.org/headers"
    
    # Custom headers
    custom_headers = {
        'User-Agent': 'MyPythonApp/1.0 (Educational Purpose)',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Custom-Header': 'This is a custom header value',
        'X-API-Version': '2.0'
    }
    
    print("Sending request with custom headers...")
    print("Custom headers:")
    for key, value in custom_headers.items():
        print(f"  {key}: {value}")
    
    response = requests.get(url, headers=custom_headers)
    
    if response.status_code == 200:
        print("\n✓ Request successful!")
        data = response.json()
        
        print("\nHeaders received by server:")
        received_headers = data['headers']
        for key, value in received_headers.items():
            print(f"  {key}: {value}")
    else:
        print(f"✗ Request failed: {response.status_code}")

def demonstrate_user_agents():
    """Demonstrate different User-Agent strings"""
    
    print("\n\nTesting Different User-Agent Strings")
    print("=" * 50)
    
    user_agents = [
        "Python-requests/2.28.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "MyBot/1.0 (+http://example.com/bot)",
        "curl/7.68.0"
    ]
    
    url = "https://httpbin.org/user-agent"
    
    for i, ua in enumerate(user_agents, 1):
        print(f"\nTest {i}: {ua}")
        
        headers = {'User-Agent': ua}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Server detected User-Agent: {data['user-agent']}")
        else:
            print(f"✗ Request failed: {response.status_code}")

def demonstrate_basic_auth():
    """Demonstrate HTTP Basic Authentication"""
    
    print("\n\nHTTP Basic Authentication")
    print("=" * 50)
    
    # httpbin.org provides a basic auth test endpoint
    url = "https://httpbin.org/basic-auth/testuser/testpass"
    
    print("Testing Basic Authentication...")
    print("Username: testuser")
    print("Password: testpass")
    
    # Method 1: Using requests.auth.HTTPBasicAuth
    from requests.auth import HTTPBasicAuth
    
    print("\nMethod 1: Using HTTPBasicAuth")
    response = requests.get(url, auth=HTTPBasicAuth('testuser', 'testpass'), timeout=10)
    print("HTTPBasicAuth status:", response.status_code)
    response = requests.get(url, auth=('testuser', 'testpass'), timeout=10)
    print("Tuple authentication status:", response.status_code)
    response = requests.get(url, auth=('testuser', 'wrong'), timeout=10)
    print("Invalid credentials status:", response.status_code)


if __name__ == "__main__":
    for demo in (demonstrate_headers, demonstrate_user_agents, demonstrate_basic_auth):
        try:
            demo()
        except requests.RequestException as error:
            print(f"Network request failed: {error}")
