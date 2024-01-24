from sys import argv
import time
import asyncio
import aiohttp

import default_urls


async def get_pic(pic_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(pic_url) as a_get:
            time_pic = time.time()
            filename = 'pics/' + 'async__' + pic_url.split('/')[-1]
            pic = await a_get.read()
            with open(filename, "wb") as f:
                f.write(pic)
            print(f"{filename} - {time.time() - time_pic:.2f} sec.")


async def main():
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_pic(url)))
        #task = asyncio.ensure_future(get_pic(url))
        #tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    urls = [arg for arg in argv[1:]] if len(argv) > 1 else default_urls.default_url
    time_total = time.time()

    asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    print(f" всего затрачено - {time.time() - time_total:.2f} sec.")

