import asyncio
import aiohttp
import time
import os

from pathlib import Path

IMAGES_DIR = "images"
PICSUM_URL = "https://picsum.photos/800/600"


def ensure_image_dir():
    Path(IMAGES_DIR).mkdir(exist_ok=True)


async def download_image(session: aiohttp.ClientSession, image_id: int) -> dict:
    filename = f"{int(time.time() * 1000000)}_{image_id}.jpg"
    path = os.path.join(IMAGES_DIR, filename)

    start_time = time.perf_counter()

    try:
        async with session.get(PICSUM_URL) as response:
            if response.status == 200:
                content = await response.read()

                with open(path, "wb") as f:
                    f.write(content)
                
                elapsed_time = time.perf_counter() - start_time
                print(f"Image {image_id} downloaded in {elapsed_time:.2f} seconds ({filename})")

                return {
                    "id": image_id,
                    "filename": filename,
                    "time": elapsed_time,
                    "success": True
                }
            else:
                print(f"Image download failed with status {response.status}")
                return {"id": image_id, "success": False}
            
    except Exception as error:
        print(f"Image exception {image_id}. {error}")
        return {"id": image_id, "success": False, "error": str(error)}
    

async def concurrent_download(num_images: int) -> tuple:
    print(f"\nConcurrent download of {num_images} images")

    ensure_image_dir()
    start_time = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, i) for i in range(1, num_images + 1)]
        results = await asyncio.gather(*tasks)

    elapsed_time = time.perf_counter() - start_time

    return results, elapsed_time


async def sequential_download(num_images: int) -> tuple:
    print(f"\nSequential download of {num_images} images")

    ensure_image_dir()
    start_time = time.perf_counter()
    results = []

    async with aiohttp.ClientSession() as session:
        for i in range(1, num_images + 1):
            result = await download_image(session, i)
            results.append(result)
            await asyncio.sleep(0.1)

    elapsed_time = time.perf_counter() - start_time

    return results, elapsed_time


def print_results(results: list, elapsed: float, mode: str):
    successful = sum(True for r in results if r.get("success"))
    failed = len(results) - successful

    print(f"\n{mode} result")
    print(f"Total time {elapsed:.2f} seconds")
    print(f"Successful {successful}/{len(results)}")
    print(f"Failed {failed}")


async def main():
    num_images = 10

    seq_results, seq_time = await sequential_download(num_images)
    print_results(seq_results, seq_time, "sequential")

    conc_results, conc_time = await concurrent_download(num_images)
    print_results(conc_results, conc_time, "concurrent")

    print("\nComparison:")
    print(f"Sequential {seq_time:.2f} seconds")
    print(f"Concurrent {conc_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())