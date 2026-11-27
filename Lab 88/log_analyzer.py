# Create file: log_analyzer.py
import sqlite3
import json
import os
import glob
from datetime import datetime

class LogAnalyzer:
    """Tool to analyze generated log files"""
    
    def __init__(self):
        self.db_path = 'logs.db'
    
    def analyze_database_logs(self):
        """Analyze logs stored in the database"""
        print("Database Log Analysis")
        print("-" * 30)
        
        if not os.path.exists(self.db_path):
            print("Database not found. Run the integrated logging system first.")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count logs by level
        cursor.execute("""
            SELECT level, COUNT(*) as count 
            FROM logs 
            GROUP BY level 
            ORDER BY count DESC
        """)
        
        print("Log entries by level:")
        for level, count in cursor.fetchall():
            print(f"  {level}: {count}")
        
        # Recent logs
        cursor.execute("""
            SELECT timestamp, level, message 
            FROM logs 
            ORDER BY id DESC 
            LIMIT 5
        """)
        
        print("\nMost recent log entries:")
        for timestamp, level, message in cursor.fetchall():
            print(f"  [{timestamp}] {level}: {message[:60]}...")
        
        conn.close()
    
    def analyze_json_logs(self):
        """Analyze JSON formatted logs"""
        print("\nJSON Log Analysis")
        print("-" * 20)
        
        json_files = glob.glob('logs/*_json.log')
        if not json_files:
            print("No JSON log files found.")
            return
        
        for json_file in json_files:
            print(f"\nAnalyzing {json_file}:")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        print("  File is empty")
                        continue
                    
                    # Split by lines and parse each JSON object
                    json_objects = []
                    for line in content.split('\n'):
                        if line.strip():
                            try:
                                # Handle multi-line JSON
                                if line.strip().startswith('{'):
                                    json_obj = json.loads(line)
                                    json_objects.append(json_obj)
                            except json.JSONDecodeError:
                                continue
                    
                    if json_objects:
                        from collections import Counter
                        counts = Counter(item.get('level', 'UNKNOWN') for item in json_objects)
                        print("  Records:", len(json_objects))
                        for level, count in sorted(counts.items()):
                            print(f"  {level}: {count}")
                    else:
                        print("  No valid JSON records")
            except (OSError, UnicodeError) as error:
                print(f"  Error: {error}")


if __name__ == "__main__":
    analyzer = LogAnalyzer()
    analyzer.analyze_database_logs()
    analyzer.analyze_json_logs()
