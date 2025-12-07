import asyncio


async def main(filenames):
    tasks = [read_file_async(filename) for filename in filenames]
    names = await asyncio.gather(*tasks)
    return ' '.join(names)
