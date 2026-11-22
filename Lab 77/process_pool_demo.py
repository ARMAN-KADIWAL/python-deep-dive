def multiply_task(x, y, task_name):
    """Task that takes multiple arguments"""
    process_id = os.getpid()
    result = x * y
    print(f'Process {process_id} - {task_name}: {x} * {y} = {result}')
    return result
import multiprocessing
import time
import random
import os

def worker_task(task_id):
    """Simulate work being done by a worker process"""
    process_id = os.getpid()
    work_time = random.uniform(0.05, 0.15)
    print(f'Worker {process_id} starting task {task_id}')
    time.sleep(work_time)
    result = task_id ** 2
    print(f'Worker {process_id} completed task {task_id} in {work_time:.2f}s, result: {result}')
    return {'task_id': task_id, 'process_id': process_id, 'work_time': work_time, 'result': result}

def demonstrate_pool_map():
    """Demonstrate Pool.map() functionality"""
    print('=== Pool.map() Demonstration ===')
    tasks = list(range(1, 9))
    pool_size = 4
    print(f'Processing {len(tasks)} tasks with {pool_size} worker processes')
    start_time = time.time()
    with multiprocessing.get_context("spawn").Pool(processes=pool_size) as pool:
        results = pool.map(worker_task, tasks)
    end_time = time.time()
    print(f'\nAll tasks completed in {end_time - start_time:.2f} seconds')
    print('Results summary:')
    for result in results:
        print(f"  Task {result['task_id']}: {result['result']} (Process {result['process_id']})")

def demonstrate_pool_apply_async():
    """Demonstrate Pool.apply_async() for more control"""
    print('\n=== Pool.apply_async() Demonstration ===')
    tasks = list(range(1, 6))
    pool_size = 3
    print(f'Processing {len(tasks)} tasks asynchronously with {pool_size} workers')
    start_time = time.time()
    with multiprocessing.get_context("spawn").Pool(processes=pool_size) as pool:
        async_results = []
        for task_id in tasks:
            async_result = pool.apply_async(worker_task, (task_id,))
            async_results.append(async_result)
        results = []
        for async_result in async_results:
            result = async_result.get()
            results.append(result)
            print(f"Collected result for task {result['task_id']}")
    end_time = time.time()
    print(f'\nAll async tasks completed in {end_time - start_time:.2f} seconds')

def demonstrate_pool_starmap():
    """Demonstrate Pool.starmap() for multiple arguments"""
    print('\n=== Pool.starmap() Demonstration ===')
    task_args = [(2, 3, 'Task A'), (4, 5, 'Task B'), (6, 7, 'Task C'), (8, 9, 'Task D'), (10, 11, 'Task E')]
    with multiprocessing.get_context("spawn").Pool(processes=3) as pool:
        results = pool.starmap(multiply_task, task_args)
    print(f'Starmap results: {results}')

def main():
    print('Process Pool Demonstrations')
    print('=' * 50)
    demonstrate_pool_map()
    demonstrate_pool_apply_async()
    demonstrate_pool_starmap()
if __name__ == '__main__':
    main()
