import logging
import json
import os
from datetime import datetime

# Create logs directory
if not os.path.exists('logs'):
    os.makedirs('logs')

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        # Create log entry dictionary
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage()
        }
        
        # Add extra fields if they exist
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'duration'):
            log_entry['duration_ms'] = record.duration
            
        return json.dumps(log_entry)

def setup_json_logger():
    """Setup logger with JSON formatting"""
    logger = logging.getLogger('JSONLogger')
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # JSON file handler
    json_handler = logging.FileHandler('logs/structured.json', mode='w')
    json_handler.setFormatter(JSONFormatter())
    json_handler.setLevel(logging.DEBUG)
    
    # Regular console handler for readability
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    logger.addHandler(json_handler)
    logger.addHandler(console_handler)
    
    return logger

def demonstrate_structured_logging():
    """Demonstrate structured logging with extra context"""
    logger = setup_json_logger()
    
    # Basic logging
    logger.info("Application started")
    
    # Logging with extra context
    logger.info("User login attempt", extra={'user_id': 12345, 'request_id': 'req-001'})
    logger.warning("Slow database query", extra={'duration': 2500, 'query': 'SELECT * FROM users'})
    logger.error("Payment processing failed", extra={
        'user_id': 12345,
        'request_id': 'req-002',
        'payment_amount': 99.99,
        'error_code': 'CARD_DECLINED'
    })
    
    # Simulate API request logging
    for i in range(3):
        request_id = f"req-{100 + i}"
        user_id = 1000 + i
        duration = 150 + (i * 50)
        
        logger.info("API request processed", extra={
            'request_id': request_id,
            'user_id': user_id,
            'duration': duration,
            'endpoint': '/api/users/profile'
        })
    
    logger.info("Application shutdown")

# Run demonstration
demonstrate_structured_logging()

print("\nStructured JSON logs:")
print("-" * 50)
with open('logs/structured.json', 'r') as f:
    for line in f:
        # Pretty print each JSON log entry
        log_entry = json.loads(line.strip())
        print(json.dumps(log_entry, indent=2))
        print("-" * 30)
