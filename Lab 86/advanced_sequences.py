import re

def advanced_sequence_patterns():
    """
    Demonstrate advanced combinations of special sequences
    """
    
    print("=== Advanced Special Sequence Combinations ===")
    
    # Sample data
    log_entries = [
        "2024-01-15 14:30:45 INFO User john_doe logged in from 192.168.1.100",
        "2024-01-15 14:31:02 ERROR Failed login attempt for user admin from 10.0.0.50",
        "2024-01-15 14:32:15 WARNING High CPU usage detected: 85%",
        "2024-01-15 14:33:30 INFO File uploaded: document_v2.pdf (2.5MB)",
        "2024-01-15 14:34:45 DEBUG Database query executed in 0.025s"
    ]
    
    # Pattern to extract log components
    log_pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)'
    
    print("Log Analysis:")
    print("-" * 60)
    
    for entry in log_entries:
        match = re.match(log_pattern, entry)
        if match:
            date, time, level, message = match.groups()
            print(f"Date: {date}")
            print(f"Time: {time}")
            print(f"Level: {level}")
            print(f"Message: {message}")
            print("-" * 30)
    
    # Extract specific information using special sequences
    print("\nSpecific Information Extraction:")
    print("-" * 40)
    
    # Extract IP addresses
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    
    # Extract usernames (word characters after "user ")
    username_pattern = r'user\s+(\w+)'
    
    # Extract file sizes
    filesize_pattern = r'(\d+\.?\d*)(MB|KB|GB)'
    
    # Extract percentages
    percentage_pattern = r'(\d+)%'
    
    all_text = ' '.join(log_entries)
    
    ip_addresses = re.findall(ip_pattern, all_text)
    usernames = re.findall(username_pattern, all_text)
    filesizes = re.findall(filesize_pattern, all_text)
    percentages = re.findall(percentage_pattern, all_text)
    
    print(f"IP Addresses found: {ip_addresses}")
    print(f"Usernames found: {usernames}")
    print(f"File sizes found: {filesizes}")
    print(f"Percentages found: {percentages}")

def validate_input_formats():
    """
    Use special sequences to validate different input formats
    """
    print("\n" + "=" * 50)
    print("=== Input Format Validation ===")
    
    # Validation patterns
    patterns = {
        'username': r'^\w{3,20}$',  # 3-20 word characters
        'password': r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$',  # Complex password
        'phone': r'^\d{3}-\d{3}-\d{4}$',  # XXX-XXX-XXXX format
        'email': r'^\w+@\w+\.\w+$',  # Simple email format
        'zipcode': r'^\d{5}(-\d{4})?$',  # 5 or 9 digit ZIP
        'ssn': r'^\d{3}-\d{2}-\d{4}$',  # XXX-XX-XXXX format
    }
    
    # Test data
    test_data = {
        'username': ['john_doe', 'user123', 'ab', 'this_username_is_too_long_to_be_valid'],
        'phone': ['555-123-4567', '5551234567', '555-12-34567'],
        'email': ['user@domain.com', 'invalid-email', 'user@domain'],
        'zipcode': ['12345', '12345-6789', '1234', '123456'],
    }
    
    for data_type, test_values in test_data.items():
        if data_type in patterns:
            pattern = patterns[data_type]
            print(f"\nValidating {data_type} (Pattern: {pattern}):")
            
            for value in test_values:
                is_valid = bool(re.match(pattern, value))
                status = "✓ Valid" if is_valid else "✗ Invalid"
                print(f"  {value:20} - {status}")

# Run the demonstrations
advanced_sequence_patterns()
validate_input_formats()
