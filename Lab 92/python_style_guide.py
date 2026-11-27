# Python Style Guide - Examples from Refactoring Lab

# 1. NAMING CONVENTIONS

# Variables: Use descriptive names in snake_case
user_age = 25  # Good
a = 25  # Bad

# Functions: Use verbs that describe what the function does
def calculate_total_price(items):  # Good
    pass

def calc(items):  # Bad
    pass

# Classes: Use PascalCase with descriptive nouns
class ShoppingCart:  # Good
    pass

class SC:  # Bad
    pass

# Constants: Use UPPER_CASE with underscores
MAX_RETRY_ATTEMPTS = 3  # Good
max_retries = 3  # Bad for constants

# 2. FUNCTION DESIGN

# Single Responsibility: Each function should do one thing
def validate_email(email):
    """Check if email format is valid."""
    # Only validates email format
    pass

def process_user_registration(email, password):
    """Handle complete user registration process."""
    # Coordinates multiple steps but doesn't do everything itself
    if not validate_email(email):
        return False
    # ... other steps
    pass

# 3. ERROR HANDLING

# Use specific exception types
class ValidationError(Exception):
    """Raised when data validation fails."""
    pass

def divide_safely(dividend, divisor):
    """Divide two numbers with proper error handling."""
    if divisor == 0:
        raise ValueError("Cannot divide by zero")
    return dividend / divisor

# 4. DOCUMENTATION

def calculate_compound_interest(principal, rate, time, compound_frequency):
    """
    Calculate compound interest.
    
    Args:
        principal (float): Initial amount of money
        rate (float): Annual interest rate (as decimal)
        time (float): Time period in years
        compound_frequency (int): Number of times interest compounds per year
    
    Returns:
        float: Final amount after compound interest
    
    Raises:
        ValueError: If any parameter is negative
    """
    if any(param < 0 for param in [principal, rate, time, compound_frequency]):
        raise ValueError("All parameters must be non-negative")
    
    return principal * (1 + rate / compound_frequency) ** (compound_frequency * time)

# 5. CODE ORGANIZATION

# Group related functionality together
class BankAccount:
    """Represents a bank account with basic operations."""
    
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = []
    
    def deposit(self, amount):
        """Add money to the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self._record_transaction("deposit", amount)
    
    def withdraw(self, amount):
        """Remove money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self._record_transaction("withdrawal", amount)
    
    def _record_transaction(self, transaction_type, amount):
        """Private method to record transactions."""
        self.transaction_history.append({
            'type': transaction_type,
            'amount': amount,
            'balance_after': self.balance
        })

if __name__ == "__main__":
    # Example usage
    account = BankAccount("12345", 1000)
    account.deposit(500)
    account.withdraw(200)
    print(f"Final balance: ${account.balance}")
