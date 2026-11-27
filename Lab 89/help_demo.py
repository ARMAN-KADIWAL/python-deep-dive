#!/usr/bin/env python3
"""
Help System Demonstration - Best practices for CLI documentation
"""

import argparse
import textwrap

class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom formatter for better help display"""
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append(f'{option_string} {args_string}')
            return ', '.join(parts)

def main():
    parser = argparse.ArgumentParser(
        prog='help_demo',
        description=textwrap.dedent('''
            Advanced CLI Help System Demonstration
            
            This script showcases best practices for creating comprehensive
            help systems in command-line applications using argparse.
            
            Features demonstrated:
            • Custom help formatting
            • Detailed argument descriptions
            • Usage examples
            • Error handling with helpful messages
        '''),
        epilog=textwrap.dedent('''
            Examples:
              %(prog)s process --input data.csv --format json --verbose
              %(prog)s analyze --data results.txt --threshold 0.95
              %(prog)s export --output report.pdf --template modern
            
            For more information, visit: https://docs.python.org/3/library/argparse.html
        '''),
        formatter_class=CustomHelpFormatter
    )
    
    # Global options
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    parser.add_argument(
        '--config',
        metavar='FILE',
        help='configuration file path (default: ~/.config/help_demo.conf)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='increase verbosity level (use -v, -vv, or -vvv)'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        title='available commands',
        description='Choose one of the following commands',
        help='command help'
    )
    
    # Process command
    process_cmd = subparsers.add_parser(
        'process',
        help='process input data files',
        description='Process various types of data files with customizable options',
        epilog='Example: %(prog)s process --input data.csv --format json'
    )
    
    process_cmd.add_argument(
        '--input', '-i',
        required=True,
        metavar='FILE',
        help='input file path (required)'
    )
    
    process_cmd.add_argument(
        '--format', '-f',
        choices=['json', 'csv', 'xml', 'yaml'],
        default='json',
        help='output format (default: %(default)s)'
    )
    
    process_cmd.add_argument(
        '--threads',
        type=int,
        default=1,
        metavar='N',
        help='number of processing threads (default: %(default)s)'
    )
    
    # Analyze command
    analyze_cmd = subparsers.add_parser(
        'analyze',
        help='analyze processed data',
        description='Perform statistical analysis on processed data files'
    )
    
    analyze_cmd.add_argument(
        '--data',
        required=True,
        metavar='FILE',
        help='data file to analyze (required)'
    )
    
    analyze_cmd.add_argument(
        '--threshold',
        type=float,
        default=0.5,
        metavar='FLOAT',
        help='analysis threshold value (default: %(default)s)'
    )
    
    analyze_cmd.add_argument(
        '--output-stats',
        action='store_true',
        help='include detailed statistics in output'
    )
    
    # Parse and handle arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Display parsed configuration
    print("\n" + "=" * 60)
    print("CONFIGURATION SUMMARY")
    print("=" * 60)
    
    print(f"Command: {args.command}")
    print(f"Verbosity level: {args.verbose}")
    
    if args.config:
        print(f"Config file: {args.config}")
    
    if args.command == 'process':
        print(f"Input file: {args.input}")
        print(f"Output format: {args.format}")
        print(f"Threads: {args.threads}")
        
        if args.verbose >= 1:
            print("\n--- VERBOSE OUTPUT ---")
            print("Processing workflow:")
            print("1. Reading input file")
            print("2. Validating data format")
            print("3. Processing with specified parameters")
            print("4. Generating output")
    
    elif args.command == 'analyze':
        print(f"Data file: {args.data}")
        print(f"Threshold: {args.threshold}")
        print(f"Include statistics: {'Yes' if args.output_stats else 'No'}")
        
        if args.verbose >= 1:
            print("\n--- VERBOSE OUTPUT ---")
            print("Analysis workflow:")
            print("1. Loading data file")
            print("2. Applying threshold filters")
            print("3. Computing analysis metrics")
            if args.output_stats:
                print("4. Generating detailed statistics")

if __name__ == '__main__':
    main()
