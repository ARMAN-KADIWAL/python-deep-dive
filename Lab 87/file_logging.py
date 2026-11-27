import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Generate log filename with timestamp
log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logging to file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_filename,
    filemode='w'
)

# Get logger
logger = logging.getLogger(__name__)

# Log messages
logger.info("Application started")
logger.debug("Debug information: Processing user data")
logger.warning("Warning: Low disk space detected")
logger.error("Error: Failed to save user preferences")
logger.critical("Critical: Database connection lost")
logger.info("Application finished")

print(f"Logs written to: {log_filename}")
print("Check the log file contents:")
print("-" * 40)

# Display log file contents
with open(log_filename, 'r') as f:
    print(f.read())
