import asyncio


async def task_with_callback(name, duration):
    print(f"Task {name} started")
    await asyncio.sleep(duration)
    print(f"Task {name} completed")
    return name


def callback_function(task):
    print(f"Done callback: {task.result()}")


async def event_loop_basics():
    loop = asyncio.get_running_loop()
    print(f"Current event loop: {loop}")
    loop.call_soon(print, "call_soon: Next loop iteration")
    loop.call_later(2, print, "call_later: About two seconds elapsed")

    tasks = [
        loop.create_task(task_with_callback("EventLoop1", 1)),
        loop.create_task(task_with_callback("EventLoop2", 2)),
    ]
    for task in tasks:
        task.add_done_callback(callback_function)
    await asyncio.gather(*tasks)


async def event_loop_scheduling():
    async def quick_task(name):
        print(f"Quick task {name}")
        return name

    tasks = []
    for i in range(3):
        tasks.append(asyncio.create_task(quick_task(f"Q{i}")))
        tasks.append(asyncio.create_task(task_with_callback(f"S{i}", 1)))
    results = await asyncio.gather(*tasks)
    print(f"Scheduled results: {results}")


async def event_loop_timing():
    loop = asyncio.get_running_loop()
    started = loop.time()
    await asyncio.sleep(1)
    print(f"Loop elapsed: {loop.time() - started:.2f}s")


async def main():
    await event_loop_basics()
    await event_loop_scheduling()
    await event_loop_timing()
    print("PASS: Event loop callbacks, scheduling and timing completed.")


if __name__ == "__main__":
    asyncio.run(main())
