import multiprocessing
import threading
import time
import os

def cpu_bound_task(name, duration):
    """Simulate a CPU-intensive task"""
    print(f'Process {name} (PID: {os.getpid()}) starting...')
    start_time = time.time()
    count = 0
    while time.time() - start_time < duration:
        count += 1
    print(f'Process {name} (PID: {os.getpid()}) completed. Count: {count}')
    return count

def run_sequential():
    """Run tasks sequentially"""
    print('=== Sequential Execution ===')
    start_time = time.time()
    cpu_bound_task('Task1', 2)
    cpu_bound_task('Task2', 2)
    cpu_bound_task('Task3', 2)
    end_time = time.time()
    print(f'Sequential execution time: {end_time - start_time:.2f} seconds\n')

def run_multiprocessing():
    """Run tasks using multiprocessing"""
    print('=== Multiprocessing Execution ===')
    start_time = time.time()
    processes = []
    for i in range(1, 4):
        process = multiprocessing.get_context("spawn").Process(target=cpu_bound_task, args=(f'Task{i}', 2))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end_time = time.time()
    print(f'Multiprocessing execution time: {end_time - start_time:.2f} seconds\n')
if __name__ == '__main__':
    print('Multiprocessing vs Sequential Execution Demo')
    print('=' * 50)
    run_sequential()
    run_multiprocessing()
