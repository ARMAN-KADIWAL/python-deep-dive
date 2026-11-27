import re

def demonstrate_special_sequences():
    """
    Demonstrate the use of special sequences in regular expressions
    """
    
    # Sample text for testing
    sample_text = """
    Contact Info:
    Phone: 555-123-4567
    Email: john.doe@example.com
    Address: 123 Main St, Apt 4B
    ZIP: 12345
    Date: 2024-01-15
    Time: 14:30:45
    Notes: Call between 9 AM - 5 PM
    """
    
    print("=== Special Sequences Demonstration ===")
    print(f"Sample text:\n{sample_text}")
    print("=" * 50)
    
    # \d - matches any digit (0-9)
    print("\n1. Using \\d (digits):")
    digit_pattern = r'\d+'
    digits = re.findall(digit_pattern, sample_text)
    print(f"Pattern: {digit_pattern}")
    print(f"Found digits: {digits}")
    
    # \w - matches any word character (letters, digits, underscore)
    print("\n2. Using \\w (word characters):")
    word_pattern = r'\w+'
    words = re.findall(word_pattern, sample_text)
    print(f"Pattern: {word_pattern}")
    print(f"Found words: {words[:10]}...")  # Show first 10 words
    
    # \s - matches any whitespace character
    print("\n3. Using \\s (whitespace):")
    # Find sequences of whitespace
    whitespace_pattern = r'\s+'
    whitespaces = re.findall(whitespace_pattern, sample_text)
    print(f"Pattern: {whitespace_pattern}")
    print(f"Found whitespace sequences: {len(whitespaces)} sequences")
    
    # \D - matches any non-digit
    print("\n4. Using \\D (non-digits):")
    non_digit_pattern = r'\D+'
    non_digits = re.findall(non_digit_pattern, sample_text)
    print(f"Pattern: {non_digit_pattern}")
    print(f"Found non-digit sequences: {len(non_digits)} sequences")
    
    # \W - matches any non-word character
    print("\n5. Using \\W (non-word characters):")
    non_word_pattern = r'\W+'
    non_words = re.findall(non_word_pattern, sample_text)
    print(f"Pattern: {non_word_pattern}")
    print(f"Found non-word sequences: {non_words[:5]}...")  # Show first 5
    
    # \S - matches any non-whitespace character
    print("\n6. Using \\S (non-whitespace):")
    non_whitespace_pattern = r'\S+'
    non_whitespaces = re.findall(non_whitespace_pattern, sample_text)
    print(f"Pattern: {non_whitespace_pattern}")
    print(f"Found non-whitespace sequences: {len(non_whitespaces)} sequences")

def create_practical_patterns():
    """
    Create practical patterns using special sequences
    """
    print("\n" + "=" * 50)
    print("=== Practical Patterns with Special Sequences ===")
    
    # Phone number pattern
    phone_pattern = r'\d{3}-\d{3}-\d{4}'
    
    # Email pattern
    email_pattern = r'\w+@\w+\.\w+'
    
    # Date pattern (YYYY-MM-DD)
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    
    # Time pattern (HH:MM:SS)
    time_pattern = r'\d{1,2}:\d{2}:\d{2}'
    
    # ZIP code pattern
    zip_pattern = r'\d{5}'
    
    test_text = """
    John's info: 555-123-4567, john@email.com
    Date: 2024-01-15, Time: 14:30:45
    ZIP: 12345
    """
    
    patterns = {
        'Phone': phone_pattern,
        'Email': email_pattern,
        'Date': date_pattern,
        'Time': time_pattern,
        'ZIP': zip_pattern
    }
    
    print(f"Test text: {test_text.strip()}")
    print("\nPattern matching results:")
    
    for name, pattern in patterns.items():
        matches = re.findall(pattern, test_text)
        print(f"{name:8} ({pattern:15}): {matches}")

# Run demonstrations
demonstrate_special_sequences()
create_practical_patterns()
