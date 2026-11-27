import re

def demonstrate_group_numbering():
    """
    Demonstrate how groups are numbered in regular expressions
    """
    text = "Phone: (555) 123-4567, Date: 2024-01-15"
    
    # Pattern with multiple groups
    pattern = r'Phone: \((\d{3})\) (\d{3})-(\d{4}), Date: (\d{4})-(\d{2})-(\d{2})'
    
    match = re.search(pattern, text)
    
    if match:
        print("=== Group Numbering Demonstration ===")
        print(f"Full match (group 0): {match.group(0)}")
        print(f"Area code (group 1): {match.group(1)}")
        print(f"Phone prefix (group 2): {match.group(2)}")
        print(f"Phone suffix (group 3): {match.group(3)}")
        print(f"Year (group 4): {match.group(4)}")
        print(f"Month (group 5): {match.group(5)}")
        print(f"Day (group 6): {match.group(6)}")
        print(f"All groups: {match.groups()}")

demonstrate_group_numbering()
