import sys
import os
import math
import random


def calculate_area(length, width):
    """Calculate the area of a rectangle."""
    return length * width


def process_user_data(user_data):
    """Process user data and return formatted full name."""
    first_name = user_data['first_name']
    last_name = user_data['last_name']
    full_name = first_name + ' ' + last_name
    
    if len(full_name) > 20:
        return full_name[:20] + '...'
    else:
        return full_name


class UserAccount:
    """A class to represent a user account with basic banking operations."""
    
    def __init__(self, user_name, user_email):
        """Initialize a new user account."""
        self.user_name = user_name
        self.user_email = user_email
        self.account_balance = 0.0
    
    def deposit_money(self, amount):
        """Deposit money into the account."""
        if amount > 0:
            self.account_balance += amount
            return True
        else:
            return False
    
    def withdraw_money(self, amount):
        """Withdraw money from the account."""
        if amount <= self.account_balance and amount > 0:
            self.account_balance -= amount
            return True
        else:
            return False


def main():
    """Main function to demonstrate the refactored code."""
    test_user = {'first_name': 'John', 'last_name': 'Doe'}
    processed_name = process_user_data(test_user)
    print('Processed name:', processed_name)
    
    area = calculate_area(10, 5)
    print('Area:', area)
    
    account = UserAccount('johndoe', 'john@example.com')
    account.deposit_money(100.50)
    print('Balance:', account.account_balance)


if __name__ == '__main__':
    main()
