# Create file: custom_formatters.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs in JSON format"""
    
    def format(self, record):
        """Format log record as JSON"""
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'process': record.process,
            'thread': record.thread
        }
        
        # Add exception information if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry)

class DetailedFormatter(logging.Formatter):
    """Custom formatter with detailed information"""
    
    def __init__(self):
        super().__init__()
        
    def format(self, record):
        """Format log record with detailed information"""
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        formatted_message = (
            f"[{timestamp}] "
            f"{record.levelname:8} | "
            f"{record.name:15} | "
            f"{record.module:12}.{record.funcName:15}:{record.lineno:4} | "
            f"PID:{record.process:5} TID:{record.thread:5} | "
            f"{record.getMessage()}"
        )
        
        # Add exception information if present
        if record.exc_info:
            formatted_message += f"\n{self.formatException(record.exc_info)}"
            
        return formatted_message

class ColoredFormatter(logging.Formatter):
    """Formatter that adds colors to console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Format log record with colors"""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        
        formatted_message = (
            f"{color}[{timestamp}] {record.levelname:8}{reset} | "
            f"{record.name} | {record.getMessage()}"
        )
        
        return formatted_message
