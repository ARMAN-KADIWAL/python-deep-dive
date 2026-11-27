import logging
import sys

def setup_logger(log_level):
    """Setup logger with specified level"""
    # Clear any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    return logging.getLogger(__name__)

def demonstrate_logging(logger):
    """Demonstrate different log levels"""
    logger.debug("Starting application debug mode")
    logger.info("Application initialized successfully")
    logger.warning("Configuration file not found, using defaults")
    logger.error("Failed to connect to database")
    logger.critical("System is shutting down due to critical error")

# Interactive log level selection
print("Available log levels:")
print("1. DEBUG")
print("2. INFO") 
print("3. WARNING")
print("4. ERROR")
print("5. CRITICAL")

try:
    choice = input("Select log level (1-5): ")
    
    levels = {
        '1': logging.DEBUG,
        '2': logging.INFO,
        '3': logging.WARNING,
        '4': logging.ERROR,
        '5': logging.CRITICAL
    }
    
    if choice in levels:
        logger = setup_logger(levels[choice])
        demonstrate_logging(logger)
    else:
        print("Invalid choice. Using INFO level as default.")
        logger = setup_logger(logging.INFO)
        demonstrate_logging(logger)
        
except KeyboardInterrupt:
    print("\nProgram interrupted by user")
    sys.exit(0)
