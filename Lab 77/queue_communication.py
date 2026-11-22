import multiprocessing as mp
from queue import Empty


def producer(work, producer_id, num_items):
    for item in range(num_items):
        work.put((producer_id, item))


def consumer(work, results):
    while True:
        item = work.get()
        if item is None:
            return
        results.put(item)


def worker_with_results(work, results):
    while True:
        task = work.get()
        if task is None:
            return
        task_id, number = task
        results.put((task_id, number * number))


def collect(results, count):
    try:
        return [results.get(timeout=15) for _ in range(count)]
    except Empty as error:
        raise RuntimeError("A worker failed to return its expected result") from error


def finish(processes, queues):
    failed = []
    for process in processes:
        process.join(timeout=5)
        if process.is_alive():
            process.terminate()
            process.join()
            failed.append("worker did not finish")
        elif process.exitcode != 0:
            failed.append(f"exit code {process.exitcode}")
        process.close()
    for channel in queues:
        channel.close()
        channel.join_thread()
    if failed:
        raise RuntimeError(", ".join(failed))


def demonstrate_basic_queue():
    context = mp.get_context("spawn")
    work, results = context.Queue(), context.Queue()
    producers = [context.Process(target=producer, args=(work, i, 3)) for i in range(2)]
    consumers = [context.Process(target=consumer, args=(work, results)) for _ in range(2)]
    processes = producers + consumers
    for process in processes:
        process.start()
    try:
        for process in producers:
            process.join()
        for _ in consumers:
            work.put(None)
        actual = collect(results, 6)
        expected = [(i, j) for i in range(2) for j in range(3)]
        if sorted(actual) != expected:
            raise RuntimeError("Queue lost or duplicated a produced item")
        print("PASS: Six produced items consumed exactly once.")
        return actual
    finally:
        finish(processes, (work, results))


def demonstrate_bidirectional_queue():
    context = mp.get_context("spawn")
    work, results = context.Queue(), context.Queue()
    tasks = [(i, number) for i, number in enumerate((5, 10, 15, 20, 25))]
    workers = [context.Process(target=worker_with_results, args=(work, results)) for _ in range(3)]
    for process in workers:
        process.start()
    try:
        for task in tasks:
            work.put(task)
        for _ in workers:
            work.put(None)
        actual = collect(results, len(tasks))
        if sorted(actual) != [(i, n * n) for i, n in tasks]:
            raise RuntimeError("Bidirectional queue returned incorrect results")
        print(f"PASS: Bidirectional queue results: {sorted(actual)}")
        return actual
    finally:
        finish(workers, (work, results))


def main():
    demonstrate_basic_queue()
    demonstrate_bidirectional_queue()


if __name__ == "__main__":
    mp.freeze_support()
    main()
