#!/usr/bin/env python3
"""
JSON Error Handling Example
This script demonstrates handling invalid JSON responses
"""

import requests
import json
from requests.exceptions import RequestException

def safe_json_parse(response):
    """Safely parse JSON response with error handling"""
    
    try:
        return response.json(), None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"
    except Exception as e:
        return None, f"Unexpected error: {e}"

def test_json_responses():
    """Test different types of responses and JSON parsing"""
    
    test_urls = [
        {
            "name": "Valid JSON API",
            "url": "https://jsonplaceholder.typicode.com/posts/1",
            "expected": "Valid JSON"
        },
        {
            "name": "HTML page (not JSON)",
            "url": "https://httpbin.org/html",
            "expected": "Invalid JSON"
        },
        {
            "name": "Plain text response",
            "url": "https://httpbin.org/robots.txt",
            "expected": "Invalid JSON"
        },
        {
            "name": "XML response",
            "url": "https://httpbin.org/xml",
            "expected": "Invalid JSON"
        }
    ]
    
    for i, test in enumerate(test_urls, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 50)
        print(f"URL: {test['url']}")
        print(f"Expected: {test['expected']}")
        
        try:
            response = requests.get(test['url'], timeout=10)
            response.raise_for_status()
            
            print(f"✓ HTTP Request successful (Status: {response.status_code})")
            print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            # Try to parse JSON
            json_data, error = safe_json_parse(response)
            
            if json_data is not None:
                print("✓ JSON parsing successful")
                print(f"Data type: {type(json_data)}")
                
                if isinstance(json_data, dict):
                    print(f"JSON keys: {list(json_data.keys())}")
                elif isinstance(json_data, list):
                    print(f"JSON list length: {len(json_data)}")
                    
            else:
                print(f"✗ JSON parsing failed: {error}")
                print(f"Response content preview: {response.text[:100]}...")
                
        except RequestException as e:
            print(f"✗ HTTP Request failed: {e}")

def robust_api_client():
    """Example of a robust API client with comprehensive error handling"""
    
    class APIClient:
        def __init__(self, base_url, timeout=10):
            self.base_url = base_url.rstrip('/')
            self.timeout = timeout
            self.session = requests.Session()
            
            # Set default headers
            self.session.headers.update({
                'User-Agent': 'Python-API-Client/1.0',
                'Accept': 'application/json'
            })
        
        def get(self, endpoint):
            """Make GET request with comprehensive error handling"""
            
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            
            try:
                print(f"Making GET request to: {url}")
                
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # Check if response is JSON
                content_type = response.headers.get('content-type', '')
                
                if 'application/json' in content_type:
                    json_data, error = safe_json_parse(response)
                    
                    if json_data is not None:
                        return {
                            'success': True,
                            'data': json_data,
                            'status_code': response.status_code,
                            'content_type': content_type
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"JSON parsing failed: {error}",
                            'status_code': response.status_code,
                            'raw_content': response.text[:200]
                        }
                else:
                    return {
                        'success': False,
                        'error': f"Expected JSON but got {content_type}",
                        'status_code': response.status_code,
                        'raw_content': response.text[:200]
                    }
                    
            except RequestException as e:
                return {
                    'success': False,
                    'error': f"Request failed: {e}",
                    'status_code': None
                }
    
    # Test the robust API client
    print("\nTesting Robust API Client...")
    print("=" * 50)
    
    client = APIClient("https://jsonplaceholder.typicode.com")
    
    # Test valid endpoint
    result = client.get("/posts/1")
    print(f"Valid endpoint result: {result['success']}")
    if result['success']:
        print(f"Data keys: {list(result['data'].keys())}")
    else:
        print(f"Error: {result['error']}")
    
    # Test invalid endpoint
    result = client.get("/invalid-endpoint")
    print(f"\nInvalid endpoint result: {result['success']}")
    print(f"Status code: {result['status_code']}")
    print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_json_responses()
    robust_api_client()
