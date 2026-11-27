import logging
import logging.config
import os
import sys
import time
import random
from datetime import datetime

# Create logs directory
if not os.path.exists('logs'):
    os.makedirs('logs')

# Logging configuration dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
        'json': {
            'format': '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'file_debug': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'logs/debug.log',
            'mode': 'w'
        },
        'file_error': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'logs/errors.log',
            'mode': 'w'
        },
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': 'logs/app_rotating.log',
            'maxBytes': 2048,
            'backupCount': 3
        }
    },
    'loggers': {
        '': {  # root logger
            'level': 'DEBUG',
            'handlers': ['console', 'file_debug', 'file_error', 'rotating_file']
        }
    }
}

class UserManager:
    """Example class demonstrating logging in a real application"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.users = {}
        self.logger.info("UserManager initialized")
    
    def create_user(self, user_id, username, email):
        """Create a new user"""
        self.logger.debug(f"Attempting to create user: {username}")
        
        if user_id in self.users:
            self.logger.warning(f"User ID {user_id} already exists")
            return False
        
        if not email or '@' not in email:
            self.logger.error(f"Invalid email address: {email}")
            return False
        
        self.users[user_id] = {
            'username': username,
            'email': email,
            'created_at': datetime.now().isoformat()
        }
        
        self.logger.info(f"User created successfully: {username} (ID: {user_id})")
        return True
    
    def get_user(self, user_id):
        """Retrieve user information"""
        self.logger.debug(f"Looking up user ID: {user_id}")
        
        if user_id not in self.users:
            self.logger.warning(f"User not found: {user_id}")
            return None
        
        self.logger.debug(f"User found: {self.users[user_id]['username']}")
        return self.users[user_id]
    
    def delete_user(self, user_id):
        """Delete a user"""
        self.logger.debug(f"Attempting to delete user ID: {user_id}")
        
        if user_id not in self.users:
            self.logger.error(f"Cannot delete non-existent user: {user_id}")
            return False
        
        username = self.users[user_id]['username']
        del self.users[user_id]
        self.logger.info(f"User deleted: {username} (ID: {user_id})")
        return True

class PaymentProcessor:
    """Example payment processing with logging"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("PaymentProcessor initialized")
    
    def process_payment(self, user_id, amount, card_number):
        """Process a payment"""
        self.logger.info(f"Processing payment for user {user_id}: ${amount}")
        
        # Simulate processing time
        processing_time = random.uniform(0.5, 2.0)
        time.sleep(processing_time)
        
        # Simulate random failures
        if random.random() < 0.2:  # 20% failure rate
            self.logger.error(f"Payment failed for user {user_id}: Card declined")
            return False
        
        if amount > 1000:
            self.logger.warning(f"Large payment amount: ${amount} for user {user_id}")
        
        # Mask card number for logging
        masked_card = f"****-****-****-{card_number[-4:]}"
        self.logger.info(f"Payment successful: ${amount} charged to {masked_card}")
        self.logger.debug(f"Processing time: {processing_time:.2f} seconds")
        
        return True

def simulate_application():
    """Simulate a complete application with logging"""
    logger = logging.getLogger('MainApplication')
    
    logger.info("=== Application Starting ===")
    
    # Initialize components
    user_manager = UserManager()
    payment_processor = PaymentProcessor()
    
    # Simulate user operations
    users_data = [
        (1, "alice_smith", "alice@example.com"),
        (2, "bob_jones", "bob@example.com"),
        (3, "charlie_brown", "invalid-email"),  # This will cause an error
        (4, "diana_prince", "diana@example.com")
    ]
    
    logger.info("Creating users...")
    for user_id, username, email in users_data:
        user_manager.create_user(user_id, username, email)
    
    # Simulate user lookups
    logger.info("Testing user lookups...")
    for user_id in [1, 2, 5]:  # 5 doesn't exist
        user = user_manager.get_user(user_id)
        if user:
            logger.debug(f"Retrieved user: {user}")
    
    # Simulate payments
    logger.info("Processing payments...")
    payments = [
        (1, 29.99, "1234567890123456"),
        (2, 1500.00, "9876543210987654"),  # Large amount
        (4, 75.50, "5555444433332222")
    ]
    
    for user_id, amount, card in payments:
        success = payment_processor.process_payment(user_id, amount, card)
        if not success:
            logger.warning(f"Payment retry may be needed for user {user_id}")
    
    # Simulate cleanup
    logger.info("Cleaning up...")
    user_manager.delete_user(2)
    user_manager.delete_user(99)  # Doesn't exist
    
    logger.info("=== Application Finished ===")

def main():
    """Main function"""
    print("Complete Logging Application Demo")
    print("=" * 40)
    
    # Configure logging
    logging.config.dictConfig(LOGGING_CONFIG)
    
    try:
        simulate_application()
        
    except KeyboardInterrupt:
        logging.getLogger().info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.getLogger().critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
    
    # Display log file information
    print("\nLog files created:")
    print("-" * 20)
    
    log_files = ['debug.log', 'errors.log', 'app_rotating.log']
    for log_file in log_files:
        file_path = os.path.join('logs', log_file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  {log_file}: {size} bytes")
    
    # Show error log contents
    error_log_path = 'logs/errors.log'
    if os.path.exists(error_log_path) and os.path.getsize(error_log_path) > 0:
        print(f"\nError log contents:")
        print("-" * 30)
        with open(error_log_path, 'r') as f:
            print(f.read())

if __name__ == "__main__":
    main()
