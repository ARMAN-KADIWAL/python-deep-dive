import logging
import os
from datetime import datetime

# Create logs directory
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create logger
logger = logging.getLogger('DualLogger')
logger.setLevel(logging.DEBUG)

# Create formatters
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
console_formatter = logging.Formatter(
    '%(levelname)s: %(message)s'
)

# Create file handler
log_filename = f"logs/dual_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Only INFO and above to console
console_handler.setFormatter(console_formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Test logging
def simulate_application():
    """Simulate an application with various log events"""
    logger.info("=== Application Starting ===")
    
    logger.debug("Loading configuration files")
    logger.debug("Configuration loaded successfully")
    
    logger.info("Connecting to database")
    logger.warning("Database connection slow - retrying")
    logger.info("Database connected successfully")
    
    logger.debug("Processing user request")
    logger.info("User authentication successful")
    
    logger.error("Failed to process payment - invalid card")
    logger.warning("Retrying payment with backup processor")
    logger.info("Payment processed successfully")
    
    logger.debug("Cleaning up resources")
    logger.info("=== Application Finished ===")

# Run simulation
simulate_application()

print(f"\nDetailed logs saved to: {log_filename}")
print("\nFile contents:")
print("-" * 50)
with open(log_filename, 'r') as f:
    print(f.read())
