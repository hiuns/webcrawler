import asyncio
import time  # time.sleep is not async


async def do_work(item: str, delay_s: float = 1.0):
    print(f"{item} started")
    await asyncio.sleep(delay_s)
    print(f"{item} done")


async def main():

    start = time.perf_counter()

    todo = ["get package", "laundry", "bake cake"]

    # this makes it "wait" every tasks (1 sec per item)
    # for item in todo:
    #     await do_work(item)

    # creates tasks
    tasks = [asyncio.create_task(do_work(item)) for item in todo]
    # execute and await all of them all at once
    done, pending = await asyncio.wait(tasks, timeout=2.0)
    for task in done:
        result = task.result()

    # another way to make results
    tasks = [asyncio.create_task(do_work(item)) for item in todo]
    results = await asyncio.gather(*tasks)

    # example of taking coroutines directly - automatically creates tasks
    coros = [do_work(item) for item in todo]
    # catches exceptions too
    results = await asyncio.gather(*coros, return_exceptions=True)

    # taskgroup ensures all of the created tasks are automaticall awaited
    async with asyncio.TaskGroup() as tg:  # pyton 3.11+
        tasks = [tg.create_task(do_work(item)) for item in todo]

    end = time.perf_counter()

    print(f"it took: {end - start:.2f}s")


if __name__ == "__main__":
    # just calling makes a task but doesn't run it
    # main()
    # asyncio.run() actually makes it run
    asyncio.run(main())
