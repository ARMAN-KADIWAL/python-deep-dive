class SingletonDatabaseConnection:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonDatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            print("Creating database connection...")
            self.connection_id = id(self)
            self.connection_count = 0
            SingletonDatabaseConnection._initialized = True
        self.connection_count += 1
    
    def get_connection_info(self):
        return f"Connection ID: {self.connection_id}, Access Count: {self.connection_count}"
    
    def execute_query(self, query):
        return f"Executing query: {query} on connection {self.connection_id}"

# Testing the Singleton pattern
print("=== Testing Singleton Pattern ===")
db1 = SingletonDatabaseConnection()
db2 = SingletonDatabaseConnection()
db3 = SingletonDatabaseConnection()

print(db1.get_connection_info())
print(db2.get_connection_info())
print(db3.get_connection_info())
print(f"Are db1 and db2 the same instance? {db1 is db2}")
print(f"Are db2 and db3 the same instance? {db2 is db3}")

# All instances share the same connection
print(db1.execute_query("SELECT * FROM users"))
print(db2.execute_query("SELECT * FROM products"))

