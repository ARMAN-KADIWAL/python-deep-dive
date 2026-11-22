import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor


class WorkerThread(threading.Thread):
    def __init__(self, thread_id, task_queue, completed, result_lock):
        super().__init__(name=f"Worker-{thread_id}")
        self.thread_id = thread_id
        self.task_queue = task_queue
        self.completed = completed
        self.result_lock = result_lock

    def run(self):
        while True:
            task = self.task_queue.get()
            try:
                if task is None:
                    return
                self.process_task(task)
                with self.result_lock:
                    self.completed.append(task)
            finally:
                self.task_queue.task_done()

    def process_task(self, task):
        time.sleep(0.1)
        print(f"{self.name} completed {task}")


def download_simulation(file_name, size_mb):
    for progress in range(0, 101, 20):
        time.sleep(0.1)
        print(f"{file_name} ({size_mb} MB): {progress}%")
    return file_name


def concurrent_downloads():
    files = [("document.pdf", 5), ("video.mp4", 50), ("music.mp3", 10), ("software.zip", 100)]
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda item: download_simulation(*item), files))
    return results


def worker_pool_example():
    tasks = [f"Task-{i}" for i in range(1, 11)]
    task_queue = queue.Queue()
    completed = []
    result_lock = threading.Lock()
    workers = [WorkerThread(i, task_queue, completed, result_lock) for i in range(1, 4)]
    for task in tasks:
        task_queue.put(task)
    for _ in workers:
        task_queue.put(None)
    for worker in workers:
        worker.start()
    task_queue.join()
    for worker in workers:
        worker.join()
    if sorted(completed) != sorted(tasks):
        raise RuntimeError("Worker pool lost or duplicated a task")
    print(f"PASS: {len(completed)} unique tasks processed exactly once.")
    return completed


def main():
    concurrent_downloads()
    worker_pool_example()


if __name__ == "__main__":
    main()
