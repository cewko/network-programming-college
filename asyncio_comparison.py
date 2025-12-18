import asyncio
import random
import time


async def async_worker(task_id: int) -> None:
    sleep_time = random.uniform(1, 3)
    print(f"Task {task_id} started. Sleep time: {sleep_time:.2f} secs")

    await asyncio.sleep(sleep_time)


async def sequential_exec(task_number: int = 5) -> float:
    start_time = time.perf_counter()

    for i in range(1, task_number + 1):
        await async_worker(i)

    elapsed_time = time.perf_counter() - start_time

    print(f"Sequential execution time: {elapsed_time:.2f} secs\n")

    return elapsed_time


async def concurrent_exec(task_number: int = 5) -> float:
    start_time = time.perf_counter()

    tasks = [async_worker(i) for i in range(1, task_number + 1)]
    await asyncio.gather(*tasks)

    elapsed_time = time.perf_counter() - start_time

    print(f"Concurrent execution time: {elapsed_time:.2f} secs\n")

    return elapsed_time


async def main():
    sequential_time = await sequential_exec()
    concurrent_time = await concurrent_exec()

    time_saved = sequential_time - concurrent_time
    efficiency = (time_saved / sequential_time) * 100

    print(f"Time saved: {time_saved:.2f}")
    print(f"Concurrent execution is {efficiency:.2f} times faster")


if __name__ == "__main__":
    asyncio.run(main())

