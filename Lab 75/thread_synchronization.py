import threading
import time
import random


shared_counter = 0
counter_lock = threading.Lock()


class BankAccount:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.lock = threading.Lock()
        self.transaction_history = []

    def deposit(self, amount, account_holder):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        """Thread-safe deposit operation"""
        with self.lock:
            old_balance = self.balance
            time.sleep(0.1)
            self.balance += amount
            transaction = f"{account_holder} deposited ${amount}. Balance: ${old_balance} -> ${self.balance}"
            self.transaction_history.append(transaction)
            print(transaction)

    def withdraw(self, amount, account_holder):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        """Thread-safe withdrawal operation"""
        with self.lock:
            if self.balance >= amount:
                old_balance = self.balance
                time.sleep(0.1)
                self.balance -= amount
                transaction = f"{account_holder} withdrew ${amount}. Balance: ${old_balance} -> ${self.balance}"
                self.transaction_history.append(transaction)
                print(transaction)
                return True
            else:
                print(f"{account_holder} attempted to withdraw ${amount} but insufficient funds (${self.balance})")
                return False

    def get_balance(self):
        """Thread-safe balance check"""
        with self.lock:
            return self.balance

def safe_increment(thread_name, iterations):
    """Safe increment with lock synchronization"""
    global shared_counter, counter_lock

    for i in range(iterations):
        with counter_lock:

            current_value = shared_counter
            time.sleep(0.0001)
            shared_counter = current_value + 1

        if i % 1000 == 0:
            print(f"{thread_name}: iteration {i}, counter = {shared_counter}")

def demonstrate_thread_safety():
    """Demonstrate thread-safe operations using locks"""
    global shared_counter
    shared_counter = 0

    print("=== Thread Safety with Locks ===")
    print("Running safe increment with multiple threads...")

    iterations = 5000
    num_threads = 3

    threads = []
    start_time = time.time()


    for i in range(num_threads):
        thread = threading.Thread(
            target=safe_increment,
            args=(f"Thread-{i+1}", iterations)
        )
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()
    expected_value = iterations * num_threads

    print(f"\nResults:")
    print(f"Expected counter value: {expected_value}")
    print(f"Actual counter value: {shared_counter}")
    print(f"Difference: {expected_value - shared_counter}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

    if shared_counter == expected_value:
        print("✅ Thread synchronization successful! Counter value is correct.")
    else:
        raise RuntimeError("Thread synchronization failed")

def bank_account_simulation():
    """Simulate concurrent bank account operations"""
    print("\n=== Bank Account Simulation ===")

    account = BankAccount(1000)
    print(f"Initial balance: ${account.get_balance()}")

    def customer_transactions(customer_name, account):
        """Simulate customer performing random transactions"""
        for i in range(5):
            operation = random.choice(['deposit', 'withdraw'])
            amount = random.randint(50, 200)

            if operation == 'deposit':
                account.deposit(amount, customer_name)
            else:
                account.withdraw(amount, customer_name)

            time.sleep(random.uniform(0.1, 0.3))


    customers = ['Alice', 'Bob', 'Charlie']
    threads = []

    for customer in customers:
        thread = threading.Thread(target=customer_transactions, args=(customer, account))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    print(f"\nFinal balance: ${account.get_balance()}")
    print(f"Total transactions: {len(account.transaction_history)}")

def main():
    demonstrate_thread_safety()
    bank_account_simulation()

if __name__ == "__main__":
    main()
