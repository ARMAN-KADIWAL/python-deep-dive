import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ThreadSafeSingleton, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.data = "Singleton Data"
            self._initialized = True
    
    def get_data(self):
        return f"Thread ID: {threading.current_thread().ident}, Data: {self.data}"

# Test thread safety
def create_singleton():
    singleton = ThreadSafeSingleton()
    print(singleton.get_data())

# Create multiple threads
threads = []
for i in range(5):
    thread = threading.Thread(target=create_singleton)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

