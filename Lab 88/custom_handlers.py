# Create file: custom_handlers.py
import logging
import sqlite3
import json
from datetime import datetime

class DatabaseHandler(logging.Handler):
    """Custom logging handler that writes logs to SQLite database"""
    
    def __init__(self, db_path='logs.db'):
        super().__init__()
        self.db_path = db_path
        
    def emit(self, record):
        """Write log record to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Format the log record
            timestamp = datetime.fromtimestamp(record.created).isoformat()
            
            cursor.execute('''
                INSERT INTO logs (timestamp, level, logger_name, message, 
                                module, function, line_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                record.levelname,
                record.name,
                record.getMessage(),
                record.module,
                record.funcName,
                record.lineno
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            # Handle errors in logging (important to avoid infinite loops)
            print(f"Error writing to database: {e}")

class ExternalFileHandler(logging.Handler):
    """Custom handler that writes logs to external files with custom format"""
    
    def __init__(self, filename, mode='a'):
        super().__init__()
        self.filename = filename
        self.mode = mode
        
    def emit(self, record):
        """Write log record to external file"""
        try:
            with open(self.filename, self.mode, encoding='utf-8') as f:
                log_entry = self.format(record)
                f.write(log_entry + '\n')
                f.flush()
        except Exception as e:
            print(f"Error writing to external file: {e}")
