# Create file: test_database_handler.py
import logging
from custom_handlers import DatabaseHandler
import sqlite3

def test_database_logging():
    """Test the custom database handler"""
    
    # Create logger
    logger = logging.getLogger('database_test')
    logger.setLevel(logging.DEBUG)
    
    # Add database handler
    db_handler = DatabaseHandler()
    db_handler.setLevel(logging.DEBUG)
    
    logger.addHandler(db_handler)
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("Application started successfully")
    logger.warning("This is a warning message")
    logger.error("An error occurred in the application")
    logger.critical("Critical system failure!")
    
    print("Log entries written to database")
    
    # Verify entries in database
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    
    print("\nRecent log entries from database:")
    for row in rows:
        print(f"ID: {row[0]}, Level: {row[2]}, Message: {row[4]}")
    
    conn.close()

if __name__ == "__main__":
    test_database_logging()
