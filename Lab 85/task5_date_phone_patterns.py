import re
from datetime import datetime

# Sample text with various date and phone formats
mixed_data = """
Important dates and contact information:

Dates in various formats:
- American format: 12/25/2023, 01/01/2024, 07/04/2024
- European format: 25/12/2023, 01/01/2024, 04/07/2024  
- ISO format: 2023-12-25, 2024-01-01, 2024-07-04
- Written format: December 25, 2023; January 1st, 2024; July 4th, 2024
- Short format: Dec 25, 2023; Jan 1, 2024; Jul 4, 2024

Phone numbers in various formats:
- Standard: 555-123-4567, 555-987-6543
- Parentheses: (555) 123-4567, (555) 987-6543
- Dots: 555.123.4567, 555.987.6543
- International: +1-555-123-4567, +1 (555) 987-6543
- Toll-free: 1-800-555-0199, 800-FLOWERS (800-356-9377)
- Extensions: 555-123-4567 ext. 123, (555) 987-6543 x456
"""

print("Sample Data with Mixed Formats:")
print(mixed_data)
print("=" * 70)

# Task 5.1: Comprehensive date pattern matching
def extract_dates():
    print("Task 5.1: Extracting Dates in Various Formats")
    print("-" * 50)
    
    # Different date patterns
    date_patterns = {
        'MM/DD/YYYY': r'\b(0?[1-9]|1[0-2])/(0?[1-9]|[12]\d|3[01])/(\d{4})\b',
        'DD/MM/YYYY': r'\b(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/(\d{4})\b',
        'YYYY-MM-DD': r'\b(\d{4})-(0?[1-9]|1[0-2])-(0?[1-9]|[12]\d|3[01])\b',
        'Month DD, YYYY': r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?,\s+(\d{4})\b',
        'Mon DD, YYYY': r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),\s+(\d{4})\b'
    }
    
    all_dates = {}
    
    for format_name, pattern in date_patterns.items():
        matches = re.findall(pattern, mixed_data, re.IGNORECASE)
        if matches:
            all_dates[format_name] = matches
            print(f"{format_name}:")
            for match in matches:
                if isinstance(match, tuple):
                    print(f"  - {' / '.join(match)}")
                else:
                    print(f"  - {match}")
            print()
    
    return all_dates

# Task 5.2: Date validation and conversion
def validate_and_convert_dates():
    print("Task 5.2: Date Validation and Conversion")
    print("-" * 40)
    
    test_dates = [
        "12/25/2023",  # Valid
        "13/25/2023",  # Invalid month
        "12/32/2023",  # Invalid day
        "02/29/2024",  # Valid leap year
        "02/29/2023",  # Invalid leap year
        "2024-02-29",  # Valid ISO format
        "2024-13-01",  # Invalid month in ISO
    ]
    
    def validate_date(date_str, format_pattern, date_format):
        """Validate a date string against a pattern and format"""
        match = re.match(format_pattern, date_str)
        if not match:
            return False, "Format doesn't match"
        
        try:
            # Try to create a datetime object to validate the date
            datetime.strptime(date_str, date_format)
            return True, "Valid date"
        except ValueError as e:
            return False, str(e)
    
    # Test different date formats
    formats_to_test = [
        (r'^\d{2}/\d{2}/\d{4}$', '%m/%d/%Y', 'MM/DD/YYYY'),
        (r'^\d{4}-\d{2}-\d{2}$', '%Y-%m-%d', 'YYYY-MM-DD'),
    ]
    
    for date_str in test_dates:
        print(f"Testing: {date_str}")
        for pattern, date_format, format_name in formats_to_test:
            if re.match(pattern, date_str):
                is_valid, message = validate_date(date_str, pattern, date_format)
                status = "✓ VALID" if is_valid else "✗ INVALID"
                print(f"  {format_name}: {status} - {message}")
        print()

# Task 5.3: Comprehensive phone number extraction
def extract_phone_numbers():
    print("Task 5.3: Extracting Phone Numbers in Various Formats")
    print("-" * 55)
    
    # Different phone number patterns
    phone_patterns = {
        'Standard (XXX-XXX-XXXX)': r'\b\d{3}-\d{3}-\d{4}\b',
        'Parentheses ((XXX) XXX-XXXX)': r'\(\d{3}\)\s\d{3}-\d{4}',
        'Dots (XXX.XXX.XXXX)': r'\b\d{3}\.\d{3}\.\d{4}\b',
        'International (+1-XXX-XXX-XXXX)': r'\+1-\d{3}-\d{3}-\d{4}',
        'International with space (+1 (XXX) XXX-XXXX)': r'\+1\s\(\d{3}\)\s\d{3}-\d{4}',
        'Toll-free (1-800-XXX-XXXX)': r'1-800-\d{3}-\d{4}',
        'With extension (XXX-XXX-XXXX ext. XXX)': r'\d{3}-\d{3}-\d{4}\s+ext\.\s+\d+',
        'With x extension ((XXX) XXX-XXXX x XXX)': r'\(\d{3}\)\s\d{3}-\d{4}\s+x\d+'
    }
    
    all_phones = {}
    
    for format_name, pattern in phone_patterns.items():
        matches = re.findall(pattern, mixed_data)
        if matches:
            all_phones[format_name] = matches
            print(f"{format_name}:")
            for match in matches:
                print(f"  - {match}")
            print()
    
    return all_phones

# Task 5.4: Phone number validation and formatting
def validate_and_format_phones():
    print("Task 5.4: Phone Number Validation and Formatting")
    print("-" * 50)
    
    test_phones = [
        "555-123-4567",      # Valid standard
        "(555) 123-4567",    # Valid with parentheses
        "555.123.4567",      # Valid with dots
        "+1-555-123-4567",   # Valid international
        "123-456-789",       # Invalid - too short
        "555-123-45678",     # Invalid - too long
        "abc-def-ghij",      # Invalid - letters
        "1-800-555-0199",    # Valid toll-free
        "555-123-4567 ext. 123"  # Valid with extension
    ]
    
    def validate_phone(phone_str):
        """Validate and format phone number"""
        # Remove all non-digit characters except +
        digits_only = re.sub(r'[^\d+]', '', re.split(r'(?:ext\.?\s*|x\s*)\d+', phone_str, flags=re.IGNORECASE)[0])
        
        # Check for extension
        ext_match = re.search(r'(ext\.?\s*|x\s*)(\d+)', phone_str, re.IGNORECASE)
        extension = ext_match.group(2) if ext_match else None
        
        # Validate based on digit count
        if digits_only.startswith('+1') and len(digits_only) == 12:
            # International format
            formatted = f"+1 ({digits_only[2:5]}) {digits_only[5:8]}-{digits_only[8:]}"
            if extension:
                formatted += f" ext. {extension}"
            return True, formatted
        elif digits_only.startswith('1') and len(digits_only) == 11:
            # US format with country code
            formatted = f"1-{digits_only[1:4]}-{digits_only[4:7]}-{digits_only[7:]}"
            if extension:
                formatted += f" ext. {extension}"
            return True, formatted
        elif len(digits_only) == 10:
            # Standard US format
            formatted = f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
            if extension:
                formatted += f" ext. {extension}"
            return True, formatted
        else:
            return False, "Invalid phone number format"
    
    print("Phone Number Validation Results:")
    print("-" * 35)
    
    for phone in test_phones:
        is_valid, result = validate_phone(phone)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status:10} | {phone:20} → {result}")
    print()

# Task 5.5: Combined pattern extraction
def extract_all_patterns():
    print("Task 5.5: Combined Pattern Extraction Summary")
    print("-" * 45)
    
    # Extract all patterns in one go
    text = "Contact info@example.com on 2024-01-15 at 555-123-4567."
    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "date": r"\b\d{4}-\d{2}-\d{2}\b",
        "phone": r"\b\d{3}-\d{3}-\d{4}\b",
    }
    for name, pattern in patterns.items():
        print(f"{name}: {re.findall(pattern, text)}")


if __name__ == "__main__":
    extract_dates()
    validate_and_convert_dates()
    extract_phone_numbers()
    validate_and_format_phones()
    extract_all_patterns()
