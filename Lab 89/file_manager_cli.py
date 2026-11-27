#!/usr/bin/env python3
"""
File Manager CLI - Demonstrates comprehensive validation and error handling
"""

import argparse
import os
import sys
import re
from pathlib import Path

def validate_file_exists(filepath):
    """Custom validator to check if file exists"""
    if not os.path.isfile(filepath):
        raise argparse.ArgumentTypeError(f"File '{filepath}' does not exist")
    return filepath

def validate_directory_exists(dirpath):
    """Custom validator to check if directory exists"""
    if not os.path.isdir(dirpath):
        raise argparse.ArgumentTypeError(f"Directory '{dirpath}' does not exist")
    return dirpath

def validate_email(email):
    """Custom validator for email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise argparse.ArgumentTypeError(f"'{email}' is not a valid email address")
    return email

def validate_port(port):
    """Custom validator for network port"""
    try:
        port_num = int(port)
        if not (1 <= port_num <= 65535):
            raise argparse.ArgumentTypeError(f"Port must be between 1 and 65535, got {port_num}")
        return port_num
    except ValueError:
        raise argparse.ArgumentTypeError(f"Port must be a number, got '{port}'")

def safe_create_directory(path):
    """Safely create directory with error handling"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        print(f"Error: Permission denied creating directory '{path}'")
        return False
    except Exception as e:
        print(f"Error creating directory '{path}': {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='File Manager CLI with comprehensive validation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 file_manager_cli.py copy --source file.txt --dest backup/
  python3 file_manager_cli.py info --path /home/user/documents
  python3 file_manager_cli.py backup --source /data --email admin@example.com --port 8080
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Copy command
    copy_parser = subparsers.add_parser('copy', help='Copy files with validation')
    copy_parser.add_argument(
        '--source', 
        type=validate_file_exists,
        required=True,
        help='Source file (must exist)'
    )
    copy_parser.add_argument(
        '--dest',
        required=True,
        help='Destination path'
    )
    copy_parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite destination if it exists'
    )
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get file/directory information')
    info_parser.add_argument(
        '--path',
        type=validate_directory_exists,
        required=True,
        help='Path to analyze (must exist)'
    )
    info_parser.add_argument(
        '--recursive',
        action='store_true',
        help='Include subdirectories'
    )
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup with notification')
    backup_parser.add_argument(
        '--source',
        type=validate_directory_exists,
        required=True,
        help='Source directory to backup'
    )
    backup_parser.add_argument(
        '--email',
        type=validate_email,
        help='Email for backup notifications'
    )
    backup_parser.add_argument(
        '--port',
        type=validate_port,
        default=22,
        help='Network port for backup service (1-65535)'
    )
    backup_parser.add_argument(
        '--compression',
        choices=['none', 'gzip', 'bzip2'],
        default='gzip',
        help='Compression method'
    )
    
    # Parse arguments with error handling
    try:
        args = parser.parse_args()
    except SystemExit:
        # argparse calls sys.exit() on error, we catch it here
        return 1
    
    if not args.command:
        parser.print_help()
        return 1
    
    print("\n" + "=" * 50)
    print(f"EXECUTING: {args.command.upper()} COMMAND")
    print("=" * 50)
    
    try:
        if args.command == 'copy':
            print(f"Source file: {args.source}")
            print(f"Destination: {args.dest}")
            print(f"Overwrite: {'Yes' if args.overwrite else 'No'}")
            
            # Check if destination exists
            if os.path.exists(args.dest) and not args.overwrite:
                print(f"Error: Destination '{args.dest}' exists. Use --overwrite to replace.")
                return 1
            
            # Create destination directory if needed
            dest_dir = os.path.dirname(args.dest)
            if dest_dir and not os.path.exists(dest_dir):
                print(f"Creating destination directory: {dest_dir}")
                if not safe_create_directory(dest_dir):
                    return 1
            
            print("✓ Copy operation validated successfully")
            print("Note: This is a simulation - no actual copying performed")
        
        elif args.command == 'info':
            print(f"Analyzing path: {args.path}")
            print(f"Recursive: {'Yes' if args.recursive else 'No'}")
            
            # Get basic information
            path_obj = Path(args.path)
            if path_obj.is_file():
                size = path_obj.stat().st_size
                print(f"Type: File")
                print(f"Size: {size} bytes")
            else:
                items = list(path_obj.iterdir())
                print(f"Type: Directory")
                print(f"Items: {len(items)}")
                
                if args.recursive:
                    total_files = sum(1 for _ in path_obj.rglob('*') if _.is_file())
                    print(f"Total files (recursive): {total_files}")
            
            print("✓ Information retrieved successfully")
        
        elif args.command == 'backup':
            print(f"Source directory: {args.source}")
            print(f"Compression: {args.compression}")
            print(f"Network port: {args.port}")
            
            if args.email:
                print(f"Notification email: {args.email}")
            else:
                print("No email notifications configured")
            
            # Validate source directory has content
            source_path = Path(args.source)
            files = list(source_path.rglob('*'))
            if not files:
                print("Warning: Source directory appears to be empty")
            else:
                print(f"Found {len(files)} items to backup")
            
            print("✓ Backup configuration validated successfully")
            print("Note: This is a simulation - no actual backup performed")
    
    except Exception as e:
        print(f"Error executing command: {e}")
        return 1
    
    print("=" * 50)
    return 0

if __name__ == '__main__':
    sys.exit(main())
