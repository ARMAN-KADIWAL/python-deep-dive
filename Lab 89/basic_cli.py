#!/usr/bin/env python3
"""
Basic CLI script using argparse
This script demonstrates the fundamentals of command-line argument parsing
"""

import argparse

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='A basic CLI application')
    
    # Add a simple positional argument
    parser.add_argument('message', help='The message to display')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Use the parsed arguments
    print(f"Your message is: {args.message}")

if __name__ == '__main__':
    main()
