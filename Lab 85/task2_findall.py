import re

# Extended sample text with multiple patterns
extended_text = """
Our company has multiple contact points:
Email addresses: john.doe@company.com, jane.smith@organization.org, 
support@helpdesk.net, admin@system.gov

Phone numbers include: 555-123-4567, (555) 987-6543, 555.456.7890,
1-800-555-0199, +1-555-123-4567

Important dates: 2024-01-15, 2024-12-25, 2023-07-04, 2024-03-17

Website URLs: https://www.example.com, http://subdomain.site.org,
https://secure.banking.com/login, http://blog.company.com/posts
"""

print("Extended Sample Text:")
print(extended_text)
print("-" * 60)

# Task 2.1: Extract all email addresses
def find_all_emails():
    print("Task 2.1: Finding All Email Addresses")
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    all_emails = re.findall(email_pattern, extended_text)
    
    print(f"Total emails found: {len(all_emails)}")
    for i, email in enumerate(all_emails, 1):
        print(f"  {i}. {email}")
    
    print()

# Task 2.2: Extract all phone numbers
def find_all_phones():
    print("Task 2.2: Finding All Phone Numbers")
    
    # Multiple phone number patterns
    phone_patterns = [
        r'\d{3}-\d{3}-\d{4}',           # 555-123-4567
        r'\(\d{3}\)\s\d{3}-\d{4}',      # (555) 123-4567
        r'\d{3}\.\d{3}\.\d{4}',         # 555.123.4567
        r'1-\d{3}-\d{3}-\d{4}',         # 1-555-123-4567
        r'\+1-\d{3}-\d{3}-\d{4}'        # +1-555-123-4567
    ]
    
    all_phones = []
    for pattern in phone_patterns:
        phones = re.findall(pattern, extended_text)
        all_phones.extend(phones)
    
    print(f"Total phone numbers found: {len(all_phones)}")
    for i, phone in enumerate(all_phones, 1):
        print(f"  {i}. {phone}")
    
    print()

# Task 2.3: Extract all dates
def find_all_dates():
    print("Task 2.3: Finding All Dates")
    
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    all_dates = re.findall(date_pattern, extended_text)
    
    print(f"Total dates found: {len(all_dates)}")
    for i, date in enumerate(all_dates, 1):
        print(f"  {i}. {date}")
    
    print()

# Task 2.4: Extract all URLs
def find_all_urls():
    print("Task 2.4: Finding All URLs")
    
    url_pattern = r'https?://[^\s,]+'
    all_urls = re.findall(url_pattern, extended_text)
    
    print(f"Total URLs found: {len(all_urls)}")
    for i, url in enumerate(all_urls, 1):
        print(f"  {i}. {url}")
    
    print()

# Run all findall demonstrations
find_all_emails()
find_all_phones()
find_all_dates()
find_all_urls()
