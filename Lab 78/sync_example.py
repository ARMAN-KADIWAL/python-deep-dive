import time


def slow_operation(name, duration):
    print(f"Starting {name}...", flush=True)
    time.sleep(duration)
    print(f"Completed {name} after {duration} seconds", flush=True)
    return f"Result from {name}"


def main():
    started = time.perf_counter()
    results = [
        slow_operation("Task 1", 2),
        slow_operation("Task 2", 3),
        slow_operation("Task 3", 1),
    ]
    print(f"Total execution time: {time.perf_counter() - started:.2f} seconds")
    print(f"Results: {results}")


if __name__ == "__main__":
    main()
