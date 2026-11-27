import logging
from logging.handlers import RotatingFileHandler
import os
import time

# Create logs directory
if not os.path.exists('logs'):
    os.makedirs('logs')

# Setup rotating file handler
def setup_rotating_logger():
    """Setup logger with rotating file handler"""
    logger = logging.getLogger('RotatingLogger')
    logger.setLevel(logging.DEBUG)
    
    # Create rotating file handler
    # maxBytes: Maximum size per file (1KB for demo)
    # backupCount: Number of backup files to keep
    handler = RotatingFileHandler(
        'logs/rotating_app.log',
        maxBytes=1024,  # 1KB for demonstration
        backupCount=3
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

# Test rotation
logger = setup_rotating_logger()

print("Generating logs to demonstrate rotation...")
print("Check the logs directory for multiple files.")

# Generate enough logs to trigger rotation
for i in range(100):
    logger.info(f"Log message number {i+1} - This is a test message to fill up the log file")
    if i % 10 == 0:
        logger.warning(f"Warning message {i+1}")
    if i % 25 == 0:
        logger.error(f"Error message {i+1}")
    
    # Small delay to see timestamp differences
    time.sleep(0.01)

print("\nLog rotation completed!")
print("Check the logs directory:")

# List log files
log_files = [f for f in os.listdir('logs') if f.startswith('rotating_app')]
log_files.sort()

for log_file in log_files:
    file_path = os.path.join('logs', log_file)
    file_size = os.path.getsize(file_path)
    print(f"  {log_file}: {file_size} bytes")
