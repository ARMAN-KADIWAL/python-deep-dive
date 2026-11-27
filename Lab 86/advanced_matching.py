import re

class PatternMatcher:
    def __init__(self):
        self.patterns = {
            'phone': r'(\d{3})-(\d{3})-(\d{4})',
            'date': r'(\d{4})-(\d{2})-(\d{2})',
            'time': r'(\d{1,2}):(\d{2}):(\d{2})',
            'ip_address': r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})',
            'credit_card': r'(\d{4})-(\d{4})-(\d{4})-(\d{4})'
        }
    
    def match_phone(self, text):
        """Match and extract phone number components"""
        match = re.match(self.patterns['phone'], text)
        if match:
            area_code, prefix, suffix = match.groups()
            return {
                'area_code': area_code,
                'prefix': prefix,
                'suffix': suffix,
                'formatted': f"({area_code}) {prefix}-{suffix}"
            }
        return None
    
    def match_date(self, text):
        """Match and extract date components"""
        match = re.match(self.patterns['date'], text)
        if match:
            year, month, day = match.groups()
            return {
                'year': year,
                'month': month,
                'day': day,
                'formatted': f"{month}/{day}/{year}"
            }
        return None
    
    def match_time(self, text):
        """Match and extract time components"""
        match = re.match(self.patterns['time'], text)
        if match:
            hour, minute, second = match.groups()
            return {
                'hour': hour,
                'minute': minute,
                'second': second,
                'formatted': f"{hour}:{minute}:{second}"
            }
        return None
    
    def match_ip_address(self, text):
        """Match and extract IP address components"""
        match = re.match(self.patterns['ip_address'], text)
        if match:
            octets = match.groups()
            return {
                'octets': octets,
                'valid': all(0 <= int(octet) <= 255 for octet in octets),
                'formatted': '.'.join(octets)
            }
        return None

# Test the pattern matcher
def test_pattern_matcher():
    matcher = PatternMatcher()
    
    test_data = [
        ('phone', '555-123-4567'),
        ('date', '2024-01-15'),
        ('time', '14:30:45'),
        ('ip_address', '192.168.1.1'),
        ('ip_address', '300.400.500.600'),  # Invalid IP
    ]
    
    print("=== Advanced Pattern Matching Demo ===")
    
    for pattern_type, test_string in test_data:
        print(f"\nTesting {pattern_type}: {test_string}")
        
        if pattern_type == 'phone':
            result = matcher.match_phone(test_string)
        elif pattern_type == 'date':
            result = matcher.match_date(test_string)
        elif pattern_type == 'time':
            result = matcher.match_time(test_string)
        elif pattern_type == 'ip_address':
            result = matcher.match_ip_address(test_string)
        
        if result:
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("  No match found")

test_pattern_matcher()
