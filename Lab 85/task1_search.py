import re

# Sample text for pattern matching
sample_text = """
Welcome to our programming course! 
Contact us at info@example.com or support@company.org
Phone numbers: 555-123-4567, (555) 987-6543
Visit our website at https://www.example.com
Today's date is 2024-01-15
"""

print("Sample Text:")
print(sample_text)
print("-" * 50)

# Task 1.1: Basic pattern search using re.search()
def basic_search_demo():
    print("Task 1.1: Basic Pattern Search with re.search()")
    
    # Search for email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    email_match = re.search(email_pattern, sample_text)
    
    if email_match:
        print(f"First email found: {email_match.group()}")
        print(f"Position: {email_match.start()} to {email_match.end()}")
    else:
        print("No email found")
    
    # Search for phone number pattern
    phone_pattern = r'\d{3}-\d{3}-\d{4}'
    phone_match = re.search(phone_pattern, sample_text)
    
    if phone_match:
        print(f"First phone number found: {phone_match.group()}")
        print(f"Position: {phone_match.start()} to {phone_match.end()}")
    else:
        print("No phone number found")
    
    print()

# Run the basic search demo
basic_search_demo()

# Task 1.2: Advanced pattern searching
def advanced_search_demo():
    print("Task 1.2: Advanced Pattern Search")
    
    # Search for URLs
    url_pattern = r'https?://[^\s]+'
    url_match = re.search(url_pattern, sample_text)
    
    if url_match:
        print(f"URL found: {url_match.group()}")
    
    # Search for dates in YYYY-MM-DD format
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    date_match = re.search(date_pattern, sample_text)
    
    if date_match:
        print(f"Date found: {date_match.group()}")
    
    # Case-insensitive search
    word_pattern = r'programming'
    case_sensitive = re.search(word_pattern, sample_text)
    case_insensitive = re.search(word_pattern, sample_text, re.IGNORECASE)
    
    print(f"Case-sensitive search for 'programming': {case_sensitive.group() if case_sensitive else 'Not found'}")
    print(f"Case-insensitive search for 'programming': {case_insensitive.group() if case_insensitive else 'Not found'}")
    
    print()

# Run the advanced search demo
advanced_search_demo()
