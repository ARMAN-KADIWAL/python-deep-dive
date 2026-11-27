import os
import re
from collections import Counter, defaultdict
from datetime import datetime

def analyze_log_file(file_path):
    """Analyze a log file and provide statistics"""
    if not os.path.exists(file_path):
        print(f"Log file not found: {file_path}")
        return
    
    print(f"\nAnalyzing: {file_path}")
    print("=" * 50)
    
    level_counts = Counter()
    hourly_counts = defaultdict(int)
    error_messages = []
    
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            # Extract log level
            level_match = re.search(r'- (DEBUG|INFO|WARNING|ERROR|CRITICAL) -', line)
            if level_match:
                level = level_match.group(1)
                level_counts[level] += 1
                
                # Extract timestamp for hourly analysis
                timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}):', line)
                if timestamp_match:
                    hour = timestamp_match.group(1)
                    hourly_counts[hour] += 1
                
                # Collect error messages
                if level in ['ERROR', 'CRITICAL']:
                    error_messages.append((line_num, line))
    
    # Display statistics
    print(f"Total lines: {sum(level_counts.values())}")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    
    print("\nLog Level Distribution:")
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        count = level_counts.get(level, 0)
        percentage = (count / sum(level_counts.values()) * 100) if level_counts else 0
        print(f"  {level:8}: {count:4} ({percentage:5.1f}%)")
    
    if hourly_counts:
        print("\nHourly Distribution:")
        for hour in sorted(hourly_counts.keys()):
            print(f"  {hour}: {hourly_counts[hour]} messages")
    
    if error_messages:
        print(f"\nErrors and Critical Issues ({len(error_messages)} found):")
        for line_num, message in error_messages[:5]:  # Show first 5

            print(f"  Line {line_num}: {message}")
    return {"levels": dict(level_counts), "hourly": dict(hourly_counts),
            "errors": error_messages}


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description="Analyze application logs")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()
    paths = args.files or sorted(str(p) for p in Path("logs").glob("*.log"))
    for path in paths:
        analyze_log_file(path)
    if not paths:
        print("Generate logs with complete_logging_app.py first.")
