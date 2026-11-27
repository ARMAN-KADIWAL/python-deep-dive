#!/usr/bin/env python3
"""
Error Handling and Timeouts Example
This script demonstrates proper error handling for HTTP requests
"""

import requests
from requests.exceptions import (
    RequestException, 
    ConnectionError, 
    HTTPError, 
    Timeout, 
    TooManyRedirects
)
import time

def make_request_with_error_handling(url, timeout=5):
    """Make HTTP request with comprehensive error handling"""
    
    print(f"Making request to: {url}")
    print(f"Timeout set to: {timeout} seconds")
    print("-" * 50)
    
    try:
        # Make request with timeout
        response = requests.get(url, timeout=timeout)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        print("✓ Request successful!")
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f} seconds")
        print(f"Content Length: {len(response.content)} bytes")
        
        return response
        
    except ConnectionError as e:
        print("✗ Connection Error: Unable to connect to the server")
        print(f"Details: {e}")
        return None
        
    except Timeout as e:
        print(f"✗ Timeout Error: Request took longer than {timeout} seconds")
        print(f"Details: {e}")
        return None
        
    except HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        print(f"Status Code: {e.response.status_code}")
        return None
        
    except TooManyRedirects as e:
        print("✗ Too Many Redirects: The request exceeded the maximum number of redirects")
        print(f"Details: {e}")
        return None
        
    except RequestException as e:
        print(f"✗ Request Exception: An error occurred during the request")
        print(f"Details: {e}")
        return None

def test_different_scenarios():
    """Test error handling with different scenarios"""
    
    test_cases = [
        {
            "name": "Valid API endpoint",
            "url": "https://jsonplaceholder.typicode.com/posts/1",
            "timeout": 10
        },
        {
            "name": "Non-existent domain",
            "url": "https://this-domain-does-not-exist-12345.com",
            "timeout": 5
        },
        {
            "name": "Valid domain but invalid path",
            "url": "https://jsonplaceholder.typicode.com/invalid-endpoint",
            "timeout": 5
        },
        {
            "name": "Very short timeout (likely to timeout)",
            "url": "https://httpbin.org/delay/3",
            "timeout": 1
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print("=" * 60)
        
        response = make_request_with_error_handling(
            test_case['url'], 
            test_case['timeout']
        )
        
        if response:
            print("✓ Test passed - Request completed successfully")
        else:
            print("✗ Test completed - Error handled gracefully")
        
        # Add delay between tests
        time.sleep(1)

def retry_mechanism_example():
    """Demonstrate retry mechanism for failed requests"""
    
    def make_request_with_retry(url, max_retries=3, delay=1):
        """Make request with retry mechanism"""
        
        for attempt in range(1, max_retries + 1):
            print(f"\nAttempt {attempt}/{max_retries}")
            
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                
                print("✓ Request successful!")
                return response
                
            except RequestException as e:
                print(f"✗ Attempt {attempt} failed: {e}")
                
                if attempt < max_retries:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print("✗ All retry attempts failed")
                    return None
    
    print("\nTesting retry mechanism...")
    print("=" * 50)
    
    # Test with a URL that might be unreliable
    unreliable_url = "https://httpbin.org/status/500"  # Always returns 500 error
    
    response = make_request_with_retry(unreliable_url, max_retries=3)
    
    if not response:
        print("\nTrying with a reliable URL...")
        reliable_url = "https://jsonplaceholder.typicode.com/posts/1"
        response = make_request_with_retry(reliable_url, max_retries=3)

if __name__ == "__main__":
    test_different_scenarios()
    retry_mechanism_example()
