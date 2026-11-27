#!/usr/bin/env python3
"""
JSON Parsing Example
This script demonstrates parsing complex JSON responses
"""

import requests
import json

def fetch_user_data():
    """Fetch and parse user data with nested information"""
    
    url = "https://jsonplaceholder.typicode.com/users"
    
    print("Fetching user data...")
    print("-" * 40)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        users = response.json()
        
        print(f"✓ Found {len(users)} users")
        print("\nUser Information:")
        print("=" * 80)
        
        for user in users[:3]:  # Show first 3 users
            print(f"Name: {user['name']}")
            print(f"Username: {user['username']}")
            print(f"Email: {user['email']}")
            print(f"Phone: {user['phone']}")
            print(f"Website: {user['website']}")
            
            # Parse nested address information
            address = user['address']
            print(f"Address: {address['street']}, {address['city']}")
            print(f"Zipcode: {address['zipcode']}")
            
            # Parse nested company information
            company = user['company']
            print(f"Company: {company['name']}")
            print(f"Company Catchphrase: {company['catchPhrase']}")
            
            print("-" * 60)
    else:
        print(f"✗ Failed to fetch users. Status code: {response.status_code}")

def extract_specific_data():
    """Extract specific data points from API response"""
    
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    
    if response.status_code == 200:
        users = response.json()
        
        print("\nExtracting specific data...")
        print("=" * 50)
        
        # Extract only email addresses
        emails = [user['email'] for user in users]
        print("All email addresses:")
        for email in emails:
            print(f"  • {email}")
        
        # Extract companies and their locations
        print("\nCompanies and Cities:")
        for user in users:
            company_name = user['company']['name']
            city = user['address']['city']
            print(f"  • {company_name} in {city}")

if __name__ == "__main__":
    fetch_user_data()
    extract_specific_data()
