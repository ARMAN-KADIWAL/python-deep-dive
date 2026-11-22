import threading
import time
import random

class ResourcePool:
    """Thread-safe resource pool using RLock"""

    def __init__(self, max_resources=3):
        if max_resources < 1:
            raise ValueError("max_resources must be positive")
        self.max_resources = max_resources
        self.available_resources = list(range(1, max_resources + 1))
        self.in_use_resources = []
        self.lock = threading.RLock()

    def acquire_resource(self, client_name):
        """Acquire a resource from the pool"""
        with self.lock:
            if self.available_resources:
                resource = self.available_resources.pop(0)
                self.in_use_resources.append(resource)
                print(f"{client_name} acquired resource {resource}")
                return resource
            else:
                print(f"{client_name} waiting for resource...")
                return None

    def release_resource(self, resource, client_name):
        """Release a resource back to the pool"""
        with self.lock:
            if resource in self.in_use_resources:
                self.in_use_resources.remove(resource)
                self.available_resources.append(resource)
                print(f"{client_name} released resource {resource}")
                return True
            return False

    def get_status(self):
        """Get current pool status (demonstrates reentrant lock)"""
        with self.lock:
            return self._get_detailed_status()

    def _get_detailed_status(self):
        """Internal method that also needs the lock"""
        with self.lock:
            return {
                'available': len(self.available_resources),
                'in_use': len(self.in_use_resources),
                'available_resources': self.available_resources.copy(),
                'in_use_resources': self.in_use_resources.copy()
            }

def client_worker(client_name, resource_pool, work_duration):
    """Simulate a client using resources from the pool"""
    for i in range(3):
        print(f"{client_name} attempting to acquire resource (attempt {i+1})")


        resource = None
        while resource is None:
            resource = resource_pool.acquire_resource(client_name)
            if resource is None:
                time.sleep(0.5)


        print(f"{client_name} using resource {resource} for {work_duration} seconds")
        time.sleep(work_duration)


        resource_pool.release_resource(resource, client_name)


        time.sleep(0.2)

def demonstrate_resource_pool():
    """Demonstrate resource pool with multiple clients"""
    print("=== Resource Pool Demonstration ===")

    pool = ResourcePool(max_resources=2)


    clients = [
        ("Client-A", 2),
        ("Client-B", 1.5),
        ("Client-C", 1),
        ("Client-D", 2.5)
    ]

    threads = []

    for client_name, work_duration in clients:
        thread = threading.Thread(
            target=client_worker,
            args=(client_name, pool, work_duration)
        )
        threads.append(thread)
        thread.start()


    monitor_thread = threading.Thread(target=monitor_pool, args=(pool, 10))
    monitor_thread.daemon = True
    monitor_thread.start()


    for thread in threads:
        thread.join()

    print("All clients completed their work")
    final_status = pool.get_status()
    print(f"Final pool status: {final_status}")

def monitor_pool(pool, duration):
    """Monitor and display pool status periodically"""
    start_time = time.time()

    while time.time() - start_time < duration:
        status = pool.get_status()
        print(f"Pool Status - Available: {status['available']}, In Use: {status['in_use']}")
        time.sleep(1)

def deadlock_example():
    """Demonstrate potential deadlock scenario and how to avoid it"""
    print("\n=== Deadlock Prevention Example ===")

    lock1 = threading.Lock()
    lock2 = threading.Lock()

    def worker1():
        print("Worker 1: Acquiring lock1...")
        with lock1:
            print("Worker 1: Got lock1, working...")
            time.sleep(1)

            print("Worker 1: Acquiring lock2...")
            with lock2:
                print("Worker 1: Got both locks, doing work...")
                time.sleep(1)
        print("Worker 1: Released all locks")

    def worker2():
        print("Worker 2: Acquiring lock1...")
        with lock1:
            print("Worker 2: Got lock1, working...")
            time.sleep(1)

            print("Worker 2: Acquiring lock2...")
            with lock2:
                print("Worker 2: Got both locks, doing work...")
                time.sleep(1)
        print("Worker 2: Released all locks")


    thread1 = threading.Thread(target=worker1)
    thread2 = threading.Thread(target=worker2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Both workers completed successfully (no deadlock)")

def main():
    demonstrate_resource_pool()
    deadlock_example()

if __name__ == "__main__":
    main()
