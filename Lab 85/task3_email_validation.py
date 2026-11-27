import re

# Task 3.1: Email validation function
def validate_email_basic(email):
    """
    Basic email validation using regular expressions
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None

# Task 3.2: Advanced email validation
def validate_email_advanced(email):
    """
    More comprehensive email validation
    """
    # More detailed pattern with additional constraints
    pattern = r'^[A-Za-z0-9]([A-Za-z0-9._%-]*[A-Za-z0-9])?@[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,}$'
    
    # Additional checks
    if len(email) > 254:  # RFC 5321 limit
        return False
    
    if '..' in email:  # No consecutive dots
        return False
    
    return re.match(pattern, email) is not None

# Task 3.3: Email validation with detailed feedback
def validate_email_detailed(email):
    """
    Email validation with detailed error reporting
    """
    errors = []
    
    # Check basic format
    if '@' not in email:
        errors.append("Missing @ symbol")
        return False, errors
    
    if email.count('@') != 1:
        errors.append("Multiple @ symbols found")
        return False, errors
    
    local_part, domain_part = email.split('@')
    
    # Validate local part (before @)
    if len(local_part) == 0:
        errors.append("Empty local part (before @)")
    elif len(local_part) > 64:
        errors.append("Local part too long (max 64 characters)")
    
    if local_part.startswith('.') or local_part.endswith('.'):
        errors.append("Local part cannot start or end with a dot")
    
    if '..' in local_part:
        errors.append("Local part cannot contain consecutive dots")
    
    # Validate domain part (after @)
    if len(domain_part) == 0:
        errors.append("Empty domain part (after @)")
    elif len(domain_part) > 253:
        errors.append("Domain part too long (max 253 characters)")
    
    if '.' not in domain_part:
        errors.append("Domain must contain at least one dot")
    
    if domain_part.startswith('.') or domain_part.endswith('.'):
        errors.append("Domain cannot start or end with a dot")
    
    # Check for valid characters
    local_pattern = r'^[A-Za-z0-9._%-]+$'
    if not re.match(local_pattern, local_part):
        errors.append("Invalid characters in local part")
    
    domain_pattern = r'^[A-Za-z0-9.-]+$'
    if not re.match(domain_pattern, domain_part):
        errors.append("Invalid characters in domain part")
    
    # Check top-level domain
    if '.' in domain_part:
        tld = domain_part.split('.')[-1]
        if len(tld) < 2:
            errors.append("Top-level domain too short")
    
    return len(errors) == 0, errors

# Test cases for email validation
def test_email_validation():
    print("Task 3: Email Address Validation Testing")
    print("=" * 50)
    
    test_emails = [
        "valid@example.com",
        "user.name@domain.org",
        "test123@subdomain.example.net",
        "invalid.email",  # Missing @
        "@domain.com",    # Missing local part
        "user@",          # Missing domain
        "user@@domain.com",  # Double @
        "user@domain",    # Missing TLD
        ".user@domain.com",  # Starts with dot
        "user.@domain.com",  # Ends with dot
        "us..er@domain.com", # Consecutive dots
        "very-long-email-address-that-exceeds-normal-limits@very-long-domain-name-that-might-cause-issues.com",
        "user@domain..com",  # Consecutive dots in domain
        "user@.domain.com",  # Domain starts with dot
        "user@domain.com.",  # Domain ends with dot
        "special!@domain.com",  # Special character
        "user@domain.c",     # Short TLD
    ]
    
    print("Basic Validation Results:")
    print("-" * 30)
    for email in test_emails:
        is_valid = validate_email_basic(email)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status:10} | {email}")
    
    print("\nAdvanced Validation Results:")
    print("-" * 30)
    for email in test_emails:
        is_valid = validate_email_advanced(email)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status:10} | {email}")
    
    print("\nDetailed Validation Results:")
    print("-" * 30)
    for email in test_emails[:8]:  # Test first 8 for detailed feedback
        is_valid, errors = validate_email_detailed(email)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status:10} | {email}")
        if errors:
            for error in errors:
                print(f"           └─ {error}")

# Run the email validation tests
test_email_validation()
