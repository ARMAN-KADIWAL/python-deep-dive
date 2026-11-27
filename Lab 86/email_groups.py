import re

def extract_email_parts(email):
    """
    Extract username and domain from email using groups
    """
    # Pattern explanation:
    # ([a-zA-Z0-9._-]+) - Group 1: username (letters, numbers, dots, underscores, hyphens)
    # @                 - literal @ symbol
    # ([a-zA-Z0-9.-]+)  - Group 2: domain (letters, numbers, dots, hyphens)
    # \.                - literal dot
    # ([a-zA-Z]{2,})    - Group 3: top-level domain (2+ letters)
    
    pattern = r'([a-zA-Z0-9._-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})'
    
    match = re.match(pattern, email)
    
    if match:
        username = match.group(1)
        domain = match.group(2)
        tld = match.group(3)
        
        print(f"Email: {email}")
        print(f"Username: {username}")
        print(f"Domain: {domain}")
        print(f"Top-level domain: {tld}")
        print(f"All groups: {match.groups()}")
        print("-" * 40)
        return True
    else:
        print(f"Invalid email format: {email}")
        return False

# Test with various email addresses
test_emails = [
    "john.doe@example.com",
    "user123@gmail.com",
    "admin@company.co.uk",
    "test_user@subdomain.example.org",
    "invalid-email"  # This should fail
]

print("=== Email Group Extraction Demo ===")
for email in test_emails:
    extract_email_parts(email)
