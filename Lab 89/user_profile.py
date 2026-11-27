#!/usr/bin/env python3
"""
User Profile CLI - Demonstrates required and optional arguments
"""

import argparse

def main():
    # Create the argument parser with a detailed description
    parser = argparse.ArgumentParser(
        description='Create and display user profiles',
        epilog='Example: python3 user_profile.py --name "John Doe" --age 25 --city "New York"'
    )
    
    # Add required arguments (using --required flag)
    parser.add_argument(
        '--name', 
        required=True,
        help='User full name (required)'
    )
    
    parser.add_argument(
        '--age',
        required=True,
        type=int,
        help='User age in years (required)'
    )
    
    # Add optional arguments
    parser.add_argument(
        '--city',
        default='Unknown',
        help='User city (optional, default: Unknown)'
    )
    
    parser.add_argument(
        '--email',
        help='User email address (optional)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Display user profile
    print("=" * 40)
    print("USER PROFILE")
    print("=" * 40)
    print(f"Name: {args.name}")
    print(f"Age: {args.age}")
    print(f"City: {args.city}")
    
    if args.email:
        print(f"Email: {args.email}")
    else:
        print("Email: Not provided")
    
    if args.verbose:
        print("\n--- VERBOSE INFORMATION ---")
        print(f"Arguments received: {vars(args)}")
        print(f"Total arguments: {len(vars(args))}")

if __name__ == '__main__':
    main()
