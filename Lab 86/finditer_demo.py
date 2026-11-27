import re

def demonstrate_finditer():
    """
    Demonstrate re.finditer() to find all matches and extract groups
    """
    
    print("=== re.finditer() Demonstration ===")
    
    # Sample text with multiple patterns
    text = """
    Contact List:
    1. John Doe - Phone: 555-123-4567, Email: john.doe@company.com
    2. Jane Smith - Phone: 555-987-6543, Email: jane.smith@company.com  
    3. Bob Johnson - Phone: 555-456-7890, Email: bob.johnson@company.com
    4. Alice Brown - Phone: 555-321-0987, Email: alice.brown@company.com
    """
    
    print(f"Sample text:\n{text}")
    print("=" * 60)
    
    # Pattern to match contact information
    contact_pattern = r'(\w+)\s+(\w+)\s+-\s+Phone:\s+(\d{3}-\d{3}-\d{4}),\s+Email:\s+(\w+\.\w+@\w+\.\w+)'
    
    print("Finding all contacts using re.finditer():")
    print("-" * 40)
    
    # Use finditer to find all matches
    matches = re.finditer(contact_pattern, text)
    
    contact_count = 0
    for match in matches:
        contact_count += 1
        first_name = match.group(1)
        last_name = match.group(2)
        phone = match.group(3)
        email = match.group(4)
        
        print(f"Contact #{contact_count}:")
        print(f"  Name: {first_name} {last_name}")
        print(f"  Phone: {phone}")
        print(f"  Email: {email}")
        print(f"  Match span: {match.span()}")
        print(f"  Full match: {match.group(0)}")
        print("-" * 30)

def extract_all_emails():
    """
    Extract all email addresses from text using finditer
    """
    print("\n=== Email Extraction with finditer ===")
    
    email_text = """
    Please contact our team:
    - Support: support@company.com
    - Sales: sales@company.com  
    - HR: hr@company.com
    - Admin: admin@company.com
    - Info: info@company.com
    
    External contacts:
    - Partner: partner@external.org
    - Vendor: vendor@supplier.net
    """
    
    # Email pattern with groups for username and domain
    email_pattern = r'(\w+)@(\w+\.\w+)'
    
    print("Extracting all emails:")
    print("-" * 30)
    
    email_matches = re.finditer(email_pattern, email_text)
    
    email_count = 0
    for match in email_matches:
        email_count += 1
        username = match.group(1)
        domain = match.group(2)
        full_email = match.group(0)
        
        print(f"Email #{email_count}:")
        print(f"  Full email: {full_email}")
        print(f"  Username: {username}")
        print(f"  Domain: {domain}")
        print(f"  Position: {match.start()}-{match.end()}")
        print()

def find_all_dates_and_times():
    """
    Find all dates and times in text using finditer
    """
    print("=== Date and Time Extraction ===")
    
    schedule_text = """
    Meeting Schedule:
    - Team meeting: 2024-01-15 at 09:30:00
    - Client call: 2024-01-16 at 14:00:00
    - Project review: 2024-01-17 at 16:30:00
    - Training session: 2024-01-18 at 10:00:00
    - Weekly standup: 2024-01-19 at 09:00:00
    """
    
    # Pattern to match date and time
    datetime_pattern = r'(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2}:\d{2})'
    
    print("Schedule extraction:")
    print("-" * 25)
    
    datetime_matches = re.finditer(datetime_pattern, schedule_text)
    
    for i, match in enumerate(datetime_matches, 1):
        date = match.group(1)
        time = match.group(2)
        
        print(f"Event #{i}:")
        print(f"  Date: {date}")
        print(f"  Time: {time}")
        print(f"  Full match: {match.group(0)}")
        print()

def advanced_finditer_example():
    """
    Advanced example using finditer with complex patterns
    """
    print("=== Advanced finditer Example ===")
    
    log_data = """
    [2024-01-15 10:30:45] INFO: User alice (ID: 1001) logged in from 192.168.1.100
    [2024-01-15 10:31:02] WARNING: Failed login attempt for user bob (ID: 1002) from 10.0.0.50
    [2024-01-15 10:32:15] ERROR: Database connection failed for user charlie (ID: 1003)
    [2024-01-15 10:33:30] INFO: File upload completed for user diana (ID: 1004) - file: report.pdf
    [2024-01-15 10:34:45] DEBUG: Cache cleared by user eve (ID: 1005)
    """
    
    # Complex pattern to extract log information
    log_pattern = r'\[(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\]\s+(\w+):\s+.*user\s+(\w+)\s+\(ID:\s+(\d+)\)'
    
    print("Log analysis:")
    print("-" * 20)
    
    log_matches = re.finditer(log_pattern, log_data)
    
    for match in log_matches:
        date = match.group(1)
        time = match.group(2)
        level = match.group(3)
        username = match.group(4)
        user_id = match.group(5)
        
        print(f"Log Entry:")
        print(f"  Date: {date}")
        print(f"  Time: {time}")
        print(f"  Level: {level}")
        print(f"  User: {username}")
        print(f"  User ID: {user_id}")
        print("-" * 15)

# Run all demonstrations
demonstrate_finditer()
extract_all_emails()
find_all_dates_and_times()
advanced_finditer_example()
