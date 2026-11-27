import re

# Sample text for replacement operations
original_text = """
Dear Customer,

Thank you for contacting us at old-email@company.com. 
Our support team can be reached at support@old-domain.com.

Please update your records with our new information:
- Phone: 555-OLD-NUMB (555-653-6862)
- Website: http://old-website.com
- Address: 123 Old Street, Old City, OS 12345

We appreciate your business since 01/15/2020.
Your account number is ACC-2020-001.

Best regards,
Customer Service Team
Phone: (555) OLD-HELP
Email: help@old-domain.com
"""

print("Original Text:")
print(original_text)
print("=" * 60)

# Task 4.1: Basic pattern replacement
def basic_replacement_demo():
    print("Task 4.1: Basic Pattern Replacement")
    
    # Replace old domain with new domain
    updated_text = re.sub(r'old-domain\.com', 'new-company.org', original_text)
    print("After replacing old-domain.com with new-company.org:")
    print("-" * 50)
    print(updated_text[:200] + "...")
    print()
    
    return updated_text

# Task 4.2: Multiple replacements with different patterns
def multiple_replacements_demo(text):
    print("Task 4.2: Multiple Pattern Replacements")
    
    # Dictionary of replacements
    replacements = {
        r'old-email@company\.com': 'contact@new-company.org',
        r'http://old-website\.com': 'https://www.new-company.org',
        r'555-OLD-NUMB': '555-NEW-HELP',
        r'Old Street': 'New Avenue',
        r'Old City': 'New City',
        r'OS': 'NC'
    }
    
    updated_text = text
    for pattern, replacement in replacements.items():
        updated_text = re.sub(pattern, replacement, updated_text)
    
    print("After multiple replacements:")
    print("-" * 30)
    print(updated_text)
    print()
    
    return updated_text

# Task 4.3: Advanced replacement with capture groups
def advanced_replacement_demo():
    print("Task 4.3: Advanced Replacement with Capture Groups")
    
    # Replace date format from MM/DD/YYYY to YYYY-MM-DD
    date_text = "Important dates: 01/15/2020, 12/25/2023, 07/04/2024"
    
    # Pattern with capture groups
    date_pattern = r'(\d{2})/(\d{2})/(\d{4})'
    # Replacement using captured groups (group 3 = year, group 1 = month, group 2 = day)
    new_date_format = r'\3-\1-\2'
    
    updated_dates = re.sub(date_pattern, new_date_format, date_text)
    
    print("Original date format:", date_text)
    print("Updated date format:", updated_dates)
    print()

# Task 4.4: Conditional replacement using functions
def conditional_replacement_demo():
    print("Task 4.4: Conditional Replacement Using Functions")
    
    # Text with various phone number formats
    phone_text = """
    Contact numbers: 555-123-4567, (555) 987-6543, 555.456.7890
    Emergency: 911, International: +1-555-123-4567
    """
    
    def format_phone_number(match):
        """Function to format phone numbers consistently"""
        phone = match.group()
        # Remove all non-digit characters except +
        digits = re.sub(r'[^\d+]', '', phone)
        
        # Format based on length
        if digits.startswith('+1') and len(digits) == 12:
            return f"+1-{digits[2:5]}-{digits[5:8]}-{digits[8:]}"
        elif len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 3:  # Emergency numbers
            return digits
        else:
            return phone  # Return original if format not recognized
    
    # Pattern to match various phone number formats
    phone_pattern = r'(\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})|\b\d{3}\b'
    
    formatted_phones = re.sub(phone_pattern, format_phone_number, phone_text)
    
    print("Original phone formats:")
    print(phone_text)
    print("Standardized phone formats:")
    print(formatted_phones)
    print()

# Task 4.5: Case-sensitive and case-insensitive replacements
def case_replacement_demo():
    print("Task 4.5: Case-Sensitive vs Case-Insensitive Replacement")
    
    text_with_cases = """
    The COMPANY policy states that company employees must follow 
    Company guidelines. Each company division has specific Company rules.
    """
    
    print("Original text:")
    print(text_with_cases)
    
    # Case-sensitive replacement
    case_sensitive = re.sub(r'company', 'organization', text_with_cases)
    print("Case-sensitive replacement (company → organization):")
    print(case_sensitive)
    
    # Case-insensitive replacement
    case_insensitive = re.sub(r'company', 'organization', text_with_cases, flags=re.IGNORECASE)
    print("Case-insensitive replacement (company → organization):")
    print(case_insensitive)
    print()

# Run all replacement demonstrations
text_after_basic = basic_replacement_demo()
text_after_multiple = multiple_replacements_demo(text_after_basic)
advanced_replacement_demo()
conditional_replacement_demo()
case_replacement_demo()
