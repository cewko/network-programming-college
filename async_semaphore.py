import asyncio
import random

from datetime import datetime


active = 0
max_concurrent = 0


async def async_worker(task_id: int, semaphore: asyncio.Semaphore):
    global active, max_concurrent

    work_time = random.uniform(0.1, 1.0)
    
    async with semaphore:
        active += 1
        max_concurrent = max(max_concurrent, active)
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-4]
        print(f"[{timestamp}] Task {task_id} started (active: {active}, max: {max_concurrent})")
        
        await asyncio.sleep(work_time)
        
        active -= 1
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-4]
        print(f"[{timestamp}] Task {task_id} completed (active: {active}, max: {max_concurrent})")


async def main():
    semaphore = asyncio.Semaphore(5)
    tasks = [async_worker(i, semaphore) for i in range(1, 51)]
    await asyncio.gather(*tasks)
    
    print(f"\nMax concurrent: {max_concurrent}")


if __name__ == "__main__":
    asyncio.run(main())