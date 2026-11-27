# Create file: monitor_logs.py
import os
import glob
from datetime import datetime

def monitor_log_files():
    """Monitor and display information about log files"""
    
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        print("Logs directory not found. Run rotating_handlers.py first.")
        return
    
    print("Log File Monitor")
    print("=" * 50)
    
    # Get all log files
    log_files = glob.glob(os.path.join(logs_dir, '*.log*'))
    
    if not log_files:
        print("No log files found.")
        return
    
    for log_file in sorted(log_files):
        file_stats = os.stat(log_file)
        file_size = file_stats.st_size
        modified_time = datetime.fromtimestamp(file_stats.st_mtime)
        
        print(f"\nFile: {log_file}")
        print(f"Size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        print(f"Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show first few lines
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"Lines: {len(lines)}")
                if lines:
                    print("First line:", lines[0].strip()[:100] + "..." if len(lines[0]) > 100 else lines[0].strip())
        except Exception as e:
            print(f"Error reading file: {e}")

if __name__ == "__main__":
    monitor_log_files()
