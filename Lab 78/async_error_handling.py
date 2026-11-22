import asyncio


async def unreliable_operation(task_id):
    await asyncio.sleep(1)
    if task_id in {2, 5}:
        raise RuntimeError(f"Task {task_id} failed intentionally")
    return f"Task {task_id} completed successfully"


async def safe_operation(task_id):
    try:
        result = await unreliable_operation(task_id)
        print(f"SUCCESS: {result}")
        return {"task": task_id, "status": "success"}
    except RuntimeError as error:
        print(f"HANDLED: {error}")
        return {"task": task_id, "status": "failed"}


async def main():
    results = await asyncio.gather(*(safe_operation(i) for i in range(1, 6)))
    failed = [item["task"] for item in results if item["status"] == "failed"]
    if failed != [2, 5]:
        raise RuntimeError("Error handling verification failed")
    print(f"Final results: {results}")
    print("PASS: Task 2 and Task 5 failed safely; other tasks completed.")


if __name__ == "__main__":
    asyncio.run(main())
