import time
import asyncio

import arr_default


async def slice_sum(data):
    _sum = 0
    for num in data:
        _sum += num
    global arr_sum
    arr_sum.append(_sum)


async def main():
    tasks = []
    i = 0
    for _ in range(count):
        tasks.append(asyncio.create_task(slice_sum(arr[i: i + idx_range])))
        i += idx_range
    if i < len(arr):
        tasks.append(asyncio.create_task(slice_sum(arr[i:])))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    count = arr_default.COUNT
    arr = arr_default.arr
    print(f'{len(arr) = }')

    time_total = time.time()
    idx_range = int(len(arr) / count)
    print(f'{idx_range = }')

    arr_sum = []
    asyncio.run(main())

    print(sum(arr_sum))

    print(f"всего затрачено - {time.time() - time_total:.4f} sec.")
    print(f"check - {sum(arr) = }")
