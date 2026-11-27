import re

class URLValidator:
    def __init__(self):
        # Define patterns for different URL components
        self.protocol_pattern = r'(https?|ftp|ftps|file|ssh|telnet)'
        self.domain_pattern = r'([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
        self.port_pattern = r'(:\d{1,5})?'
        self.path_pattern = r'(/[a-zA-Z0-9\-._~:/?#[\]@!$&\'()*+,;=%]*)?'
        
        # Complete URL pattern
        self.url_pattern = f'^{self.protocol_pattern}://{self.domain_pattern}{self.port_pattern}{self.path_pattern}$'
        
        # Compile the pattern for better performance
        self.compiled_pattern = re.compile(self.url_pattern, re.IGNORECASE)
    
    def validate_url(self, url):
        """
        Validate a URL and extract its components
        """
        from urllib.parse import urlsplit
        if not self.compiled_pattern.fullmatch(url):
            return {'valid': False, 'url': url, 'error': 'Invalid URL format'}
        try:
            parts = urlsplit(url)
            port = parts.port
            if port is not None and not 1 <= port <= 65535:
                raise ValueError("Invalid port")
            return {
                'valid': True, 'protocol': parts.scheme,
                'domain': parts.hostname, 'port': str(port) if port else 'default',
                'path': parts.path or '/', 'full_url': url,
            }
        except ValueError as error:
            return {'valid': False, 'url': url, 'error': str(error)}

    def validate_specific_protocol(self, url, required_protocol):
        """
        Validate URL with a specific protocol requirement
        """
        result = self.validate_url(url)
        
        if result['valid']:
            if result['protocol'].lower() == required_protocol.lower():
                result['protocol_match'] = True
            else:
                result['protocol_match'] = False
                result['error'] = f"Expected {required_protocol}, got {result['protocol']}"
        
        return result
    
    def extract_url_components(self, url):
        """
        Extract detailed components from a URL
        """
        from urllib.parse import urlsplit
        if not self.validate_url(url)['valid']:
            return None
        parts = urlsplit(url)
        return {
            'protocol': parts.scheme, 'domain': parts.hostname,
            'port': str(parts.port) if parts.port is not None else None,
            'path': parts.path or '/', 'query': parts.query or None,
            'fragment': parts.fragment or None,
        }

def test_url_validator():
    """
    Test the URL validator with various URLs
    """
    validator = URLValidator()
    
    # Test URLs
    test_urls = [
        # Valid URLs
        "https://www.example.com",
        "http://example.com",
        "https://subdomain.example.com:8080",
        "ftp://files.example.com/path/to/file.txt",
        "https://api.example.com/v1/users?id=123&name=john",
        "https://example.com/path/to/page#section1",
        "file://localhost/path/to/file.txt",
        
        # Invalid URLs
        "not-a-url",
        "http://",
        "https://",
        "ftp://invalid..domain.com",
        "https://example.com:99999",  # Invalid port
    ]
    
    print("=== URL Validation Test ===")
    print("-" * 50)
    
    for url in test_urls:
        result = validator.validate_url(url)
        
        print(f"URL: {url}")
        if result['valid']:
            print(f"  ✓ Valid")
            print(f"  Protocol: {result['protocol']}")
            print(f"  Domain: {result['domain']}")
            print(f"  Port: {result['port']}")
            print(f"  Path: {result['path']}")
        else:
            print(f"  ✗ Invalid - {result['error']}")
        print("-" * 30)

def test_protocol_specific_validation():
    """
    Test protocol-specific validation
    """
    validator = URLValidator()
    
    print("\n=== Protocol-Specific Validation ===")
    print("-" * 40)
    
    test_cases = [
        ("https://secure.example.com", "https"),
        ("http://example.com", "https"),  # Should fail
        ("ftp://files.example.com", "ftp"),
        ("https://api.example.com", "http"),  # Should fail
    ]
    
    for url, required_protocol in test_cases:
        result = validator.validate_specific_protocol(url, required_protocol)
        
        print(f"URL: {url}")
        print(f"Required Protocol: {required_protocol}")
        
        if result['valid']:
            if result.get('protocol_match', False):
                print(f"  ✓ Valid and protocol matches")
            else:
                print(f"  ✗ Valid URL but wrong protocol - {result['error']}")
        else:
            print(f"  ✗ Invalid URL")


if __name__ == "__main__":
    test_url_validator()
    test_protocol_specific_validation()
    validator = URLValidator()
    print(validator.extract_url_components("https://example.com:443/path?q=1#top"))
