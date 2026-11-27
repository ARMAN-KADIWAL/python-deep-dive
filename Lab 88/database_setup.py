# Create file: database_setup.py
import sqlite3
import os

def create_log_database():
    """Create a SQLite database for storing log entries"""
    db_path = 'logs.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            logger_name TEXT NOT NULL,
            message TEXT NOT NULL,
            module TEXT,
            function TEXT,
            line_number INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database created successfully at {db_path}")

if __name__ == "__main__":
    create_log_database()
