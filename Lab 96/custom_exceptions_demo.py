#!/usr/bin/env python3
"""
Lab 96: Custom Exceptions with Enhanced Reporting
This script demonstrates how custom exceptions work with Python's enhanced error reporting
"""

class ValidationError(Exception):
    """Custom exception for data validation errors"""

    def __init__(self, field_name, value, expected_type, message=None):
        self.field_name = field_name
        self.value = value
        self.expected_type = expected_type

        if message is None:
            message = (f"Validation failed for field '{field_name}': "
                      f"expected {expected_type.__name__}, got {type(value).__name__} "
                      f"with value '{value}'")

        super().__init__(message)

class DatabaseConnectionError(Exception):
    """Custom exception for database connection issues"""

    def __init__(self, host, port, error_code, message=None):
        self.host = host
        self.port = port
        self.error_code = error_code

        if message is None:
            message = (f"Failed to connect to database at {host}:{port} "
                      f"(Error code: {error_code})")

        super().__init__(message)

class InsufficientFundsError(Exception):
    """Custom exception for financial transactions"""

    def __init__(self, account_id, requested_amount, available_balance):
        self.account_id = account_id
        self.requested_amount = requested_amount
        self.available_balance = available_balance

        message = (f"Insufficient funds in account {account_id}: "
                  f"Requested ${requested_amount:.2f}, "
                  f"Available ${available_balance:.2f} "
                  f"(Shortfall: ${requested_amount - available_balance:.2f})")

        super().__init__(message)

def demonstrate_validation_error():
    """Demonstrate custom ValidationError"""
    print("=== Custom ValidationError Demonstration ===")

    def validate_user_age(age):
        """Validate user age input"""
        if type(age) is not int:
            raise ValidationError("age", age, int)

        if age < 0:
            raise ValidationError("age", age, int,
                                "Age cannot be negative")

        if age > 150:
            raise ValidationError("age", age, int,
                                "Age seems unrealistic (over 150)")

        return True

    # Test cases
    test_ages = ["25", -5, 200, 25]

    for test_age in test_ages:
        try:
            print(f"Validating age: {test_age}")
            validate_user_age(test_age)
            print("✓ Validation passed!")
        except ValidationError as e:
            print(f"✗ {e}")
        print("-" * 40)

def demonstrate_database_error():
    """Demonstrate custom DatabaseConnectionError"""
    print("\n=== Custom DatabaseConnectionError Demonstration ===")

    def connect_to_database(host, port):
        """Simulate database connection"""
        # Simulate connection failure
        if port != 5432:
            raise DatabaseConnectionError(host, port, "CONN_REFUSED",
                                        f"Connection refused on non-standard port {port}")

        if host == "invalid-host":
            raise DatabaseConnectionError(host, port, "HOST_NOT_FOUND",
                                        f"Host '{host}' could not be resolved")

        return f"Simulated connection to {host}:{port}"

    # Test database connections
    test_connections = [
        ("localhost", 3306),
        ("invalid-host", 5432),
        ("localhost", 5432)
    ]

    for host, port in test_connections:
        try:
            print(f"Connecting to {host}:{port}...")
            result = connect_to_database(host, port)
            print(f"✓ {result}")
        except DatabaseConnectionError as e:
            print(f"✗ {e}")
            print(f"   Error details: Host={e.host}, Port={e.port}, Code={e.error_code}")
        print("-" * 50)

def demonstrate_financial_error():
    """Demonstrate custom InsufficientFundsError"""
    print("\n=== Custom InsufficientFundsError Demonstration ===")

    class BankAccount:
        def __init__(self, account_id, balance):
            self.account_id = account_id
            self.balance = balance

        def withdraw(self, amount):
            """Withdraw money from account"""
            if amount <= 0:
                raise ValueError("Withdrawal must be positive")
            if amount > self.balance:
                raise InsufficientFundsError(self.account_id, amount, self.balance)

            self.balance -= amount
            return f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"

    # Create test account
    account = BankAccount("ACC-12345", 100.00)

    # Test withdrawals
    test_withdrawals = [50.00, 75.00, 25.00]

    for amount in test_withdrawals:
        try:
            print(f"Attempting to withdraw ${amount:.2f}...")
            result = account.withdraw(amount)
            print(f"✓ {result}")
        except InsufficientFundsError as e:
            print(f"✗ {e}")
            print(f"   Account: {e.account_id}")
            print(f"   Current balance: ${e.available_balance:.2f}")
        print("-" * 50)

if __name__ == "__main__":
    print("Python Custom Exceptions with Enhanced Reporting")
    print("=" * 60)

    demonstrate_validation_error()
    demonstrate_database_error()
    demonstrate_financial_error()

    print("\n" + "="*60)
    print("Custom exceptions provide detailed, context-specific error information!")
    print("Python's enhanced reporting makes debugging much easier.")
