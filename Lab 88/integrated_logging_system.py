# Create file: integrated_logging_system.py
import logging
import logging.handlers
import os
import sys
from datetime import datetime

from custom_handlers import DatabaseHandler, ExternalFileHandler
from custom_formatters import JSONFormatter, DetailedFormatter, ColoredFormatter
from exception_logger import ExceptionLogger

class IntegratedLoggingSystem:
    """Comprehensive logging system with all custom components"""
    
    def __init__(self, app_name='MyApplication'):
        self.app_name = app_name
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Set up all handlers
        self._setup_handlers()
        
        # Set up exception logging
        self.exception_logger = ExceptionLogger(f'{app_name}_exceptions')
    
    def _setup_handlers(self):
        """Set up all logging handlers"""
        
        # 1. Database Handler
        db_handler = DatabaseHandler()
        db_handler.setLevel(logging.INFO)
        self.logger.addHandler(db_handler)
        
        # 2. Rotating File Handler with detailed format
        rotating_handler = logging.handlers.RotatingFileHandler(
            filename=f'logs/{self.app_name}_rotating.log',
            maxBytes=1024*512,  # 512KB
            backupCount=3,
            encoding='utf-8'
        )
        rotating_handler.setFormatter(DetailedFormatter())
        rotating_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(rotating_handler)
        
        # 3. JSON File Handler
        json_handler = ExternalFileHandler(f'logs/{self.app_name}_json.log')
        json_handler.setFormatter(JSONFormatter())
        json_handler.setLevel(logging.WARNING)
        self.logger.addHandler(json_handler)
        
        # 4. Timed Rotating Handler
        timed_handler = logging.handlers.TimedRotatingFileHandler(
            filename=f'logs/{self.app_name}_daily.log',
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        timed_handler.setFormatter(DetailedFormatter())
        timed_handler.setLevel(logging.INFO)
        self.logger.addHandler(timed_handler)
        
        # 5. Console Handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter())
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)
        
        # 6. Error File Handler (only errors and critical)
        error_handler = logging.FileHandler(f'logs/{self.app_name}_errors.log', encoding='utf-8')
        error_handler.setFormatter(DetailedFormatter())
        error_handler.setLevel(logging.ERROR)
        self.logger.addHandler(error_handler)
    
    def log_application_start(self):
        """Log application startup"""
        self.logger.info(f"Application {self.app_name} started at {datetime.now()}")
        self.logger.info(f"Logging system initialized with {len(self.logger.handlers)} handlers")
    
    def log_application_stop(self):
        """Log application shutdown"""
        self.logger.info(f"Application {self.app_name} stopping at {datetime.now()}")
    
    def get_logger(self):
        """Get the configured logger"""
        return self.logger
    
    def log_exception(self, exc_info=None, context=None):
        """Log exception using the exception logger"""
        self.exception_logger.log_exception(exc_info, context)

def simulate_application_activity(logging_system):
    """Simulate various application activities for testing"""
    
    logger = logging_system.get_logger()
    
    # Simulate application startup
    logging_system.log_application_start()
    
    # Simulate normal operations
    logger.debug("Loading configuration files")
    logger.info("Database connection established")
    logger.info("User authentication successful")
    
    # Simulate warnings
    logger.warning("High memory usage detected")
    logger.warning("API rate limit approaching")
    
    # Simulate errors
    logger.error("Failed to send email notification")
    logger.error("Database query timeout")
    
    # Simulate critical issues
    logger.critical("System running out of disk space")
    
    # Simulate exceptions
    try:
        # Simulate a complex operation that fails
        data = {'users': [1, 2, 3]}
        user_id = data['users'][10]  # IndexError
    except Exception:
        logging_system.log_exception(context={'operation': 'user_lookup', 'user_data': str(data)})
    
    try:
        # Simulate another type of error
        config_file = open('missing_config.ini')
    except Exception:
        logging_system.log_exception(context={'operation': 'config_loading'})
    
    # Simulate more normal operations
    for i in range(10):
        logger.info(f"Processing batch {i+1}/10")
        logger.debug(f"Batch {i+1} contains {(i+1)*10} items")
    
    # Simulate application shutdown
    logging_system.log_application_stop()

def main():
    """Main function to test the integrated logging system"""
    
    print("Starting Integrated Logging System Test")
    print("=" * 50)
    
    # Create integrated logging system
    logging_system = IntegratedLoggingSystem('TestApp')
    
    # Simulate application activity
    simulate_application_activity(logging_system)
    
    print("\nIntegrated logging test complete!")
    print("\nGenerated files:")
    print("- logs.db (SQLite database)")
    print("- logs/TestApp_rotating.log (Rotating file)")
    print("- logs/TestApp_json.log (JSON format)")
    print("- logs/TestApp_daily.log (Daily rotation)")
    print("- logs/TestApp_errors.log (Errors only)")
    print("- exception_logs.log (Exception details)")
    print("- exception_logs.json (Exception JSON)")

if __name__ == "__main__":
    main()
