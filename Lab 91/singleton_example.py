# Example without Singleton - Multiple instances problem
class DatabaseConnection:
    def __init__(self):
        print("Creating new database connection...")
        self.connection_id = id(self)
    
    def get_connection_info(self):
        return f"Connection ID: {self.connection_id}"

# Creating multiple instances (not ideal for database connections)
db1 = DatabaseConnection()
db2 = DatabaseConnection()
db3 = DatabaseConnection()

print(db1.get_connection_info())
print(db2.get_connection_info())
print(db3.get_connection_info())
print(f"Are db1 and db2 the same instance? {db1 is db2}")

