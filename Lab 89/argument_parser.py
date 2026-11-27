#!/usr/bin/env python3
"""
Comprehensive Argument Parser - Demonstrates various argument types and parsing techniques
"""

import argparse
import sys

def display_arguments(args):
    """Display parsed arguments in a formatted way"""
    print("\n" + "=" * 50)
    print("PARSED COMMAND-LINE ARGUMENTS")
    print("=" * 50)
    
    # Convert args to dictionary for easier handling
    args_dict = vars(args)
    
    for key, value in args_dict.items():
        if value is not None:
            print(f"{key.upper().replace('_', ' ')}: {value}")
        else:
            print(f"{key.upper().replace('_', ' ')}: Not provided")
    
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive argument parsing demonstration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 argument_parser.py process --input file.txt --output result.txt --threads 4
  python3 argument_parser.py analyze --data dataset.csv --format json --verbose
        '''
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process files')
    process_parser.add_argument('--input', required=True, help='Input file path')
    process_parser.add_argument('--output', required=True, help='Output file path')
    process_parser.add_argument('--threads', type=int, default=1, help='Number of threads')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze data')
    analyze_parser.add_argument('--data', required=True, help='Data file path')
    analyze_parser.add_argument('--format', choices=['json', 'csv', 'xml'], default='json')
    analyze_parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if a command was provided
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Display parsed arguments
    display_arguments(args)
    
    # Execute based on command
    if args.command == 'process':
        print(f"\nExecuting PROCESS command...")
        print(f"Processing {args.input} -> {args.output} using {args.threads} threads")
    
    elif args.command == 'analyze':
        print(f"\nExecuting ANALYZE command...")
        print(f"Analyzing {args.data} in {args.format} format")
        if args.verbose:
            print("Verbose mode enabled - showing detailed analysis")

if __name__ == '__main__':
    main()
