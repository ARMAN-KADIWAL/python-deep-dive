# Create file: rotating_handlers.py
import logging
import logging.handlers
import os
from custom_formatters import DetailedFormatter, JSONFormatter

def setup_rotating_handlers():
    """Set up various rotating file handlers"""
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('rotating_logger')
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # 1. Rotating File Handler (by size)
    size_handler = logging.handlers.RotatingFileHandler(
        filename='logs/app_size.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5,       # Keep 5 backup files
        encoding='utf-8'
    )
    size_handler.setFormatter(DetailedFormatter())
    size_handler.setLevel(logging.INFO)
    logger.addHandler(size_handler)
    
    # 2. Timed Rotating File Handler (by time)
    time_handler = logging.handlers.TimedRotatingFileHandler(
        filename='logs/app_time.log',
        when='midnight',     # Rotate at midnight
        interval=1,          # Every 1 day
        backupCount=7,       # Keep 7 days of logs
        encoding='utf-8'
    )
    time_handler.setFormatter(JSONFormatter())
    time_handler.setLevel(logging.DEBUG)
    logger.addHandler(time_handler)
    
    # 3. Memory Handler (buffers logs before writing)
    memory_handler = logging.handlers.MemoryHandler(
        capacity=100,        # Buffer 100 records
        flushLevel=logging.ERROR,  # Flush when ERROR or higher
        target=size_handler  # Target handler to flush to
    )
    logger.addHandler(memory_handler)
    
    # 4. Console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(console_handler)
    
    return logger

def test_rotating_handlers():
    """Test the rotating file handlers"""
    logger = setup_rotating_handlers()
    
    print("Testing rotating file handlers...")
    
    # Generate multiple log entries to test rotation
    for i in range(50):
        logger.debug(f"Debug message {i+1}")
        logger.info(f"Info message {i+1} - Processing item {i+1}")
        logger.warning(f"Warning message {i+1} - Resource usage high")
        
        if i % 10 == 0:
            logger.error(f"Error message {i+1} - Simulated error")
        
        if i % 20 == 0:
            logger.critical(f"Critical message {i+1} - System alert")
    
    # Force memory handler to flush
    logger.error("Forcing memory handler flush")
    
    print("Rotating handler test complete!")
    print("Check the 'logs' directory for generated log files")

if __name__ == "__main__":
    test_rotating_handlers()
