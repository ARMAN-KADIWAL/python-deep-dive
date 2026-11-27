import logging
import os
from datetime import datetime

# Create logs directory
if not os.path.exists('logs'):
    os.makedirs('logs')

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_advanced_logger():
    """Setup logger with advanced formatting"""
    logger = logging.getLogger('AdvancedLogger')
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # File handler with detailed format
    file_handler = logging.FileHandler('logs/advanced_format.log', mode='w')
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)-15s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler with colored format
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def demonstrate_advanced_logging():
    """Demonstrate advanced logging features"""
    logger = setup_advanced_logger()
    
    def process_user_data(user_id, username):
        """Example function to show function name in logs"""
        logger.debug(f"Starting to process user data for ID: {user_id}")
        logger.info(f"Processing user: {username}")
        
        if user_id < 0:
            logger.error(f"Invalid user ID: {user_id}")
            return False
        
        logger.debug("User data validation completed")
        return True
    
    def simulate_database_operation():
        """Simulate database operations"""
        logger.info("Connecting to database")
        logger.debug("Database connection parameters loaded")
        
        try:
            # Simulate some processing
            logger.info("Executing database query")
            logger.debug("Query: SELECT * FROM users WHERE active = 1")
            
            # Simulate warning
            logger.warning("Query took longer than expected (2.5s)")
            
            logger.info("Database operation completed successfully")
            
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            logger.critical("System cannot continue without database")
    
    # Run demonstrations
    logger.info("=== Advanced Logging Demonstration ===")
    
    # Test user processing
    process_user_data(123, "john_doe")
    process_user_data(-1, "invalid_user")
    
    # Test database simulation
    simulate_database_operation()
    
    logger.info("=== Demonstration Complete ===")

# Run demonstration
demonstrate_advanced_logging()

print("\nCheck the detailed log file:")
print("-" * 50)
with open('logs/advanced_format.log', 'r') as f:
    print(f.read())
