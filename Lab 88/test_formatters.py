# Create file: test_formatters.py
import logging
import sys
from custom_formatters import JSONFormatter, DetailedFormatter, ColoredFormatter
from custom_handlers import ExternalFileHandler

def test_formatters():
    """Test all custom formatters"""
    
    # Create logger
    logger = logging.getLogger('formatter_test')
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # 1. JSON Formatter with file handler
    json_handler = ExternalFileHandler('logs_json.log', 'w')
    json_handler.setFormatter(JSONFormatter())
    logger.addHandler(json_handler)
    
    # 2. Detailed formatter with file handler
    detailed_handler = ExternalFileHandler('logs_detailed.log', 'w')
    detailed_handler.setFormatter(DetailedFormatter())
    logger.addHandler(detailed_handler)
    
    # 3. Colored formatter for console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)
    
    # Test logging with different levels
    logger.debug("Debug message for testing formatters")
    logger.info("Application initialization complete")
    logger.warning("Configuration file not found, using defaults")
    logger.error("Failed to connect to external service")
    logger.critical("System running out of memory")
    
    # Test exception logging
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero error occurred")
    
    print("\nFormatter testing complete!")
    print("Check the following files:")
    print("- logs_json.log (JSON format)")
    print("- logs_detailed.log (Detailed format)")
    print("- Console output (Colored format)")

if __name__ == "__main__":
    test_formatters()
