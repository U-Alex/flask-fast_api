import time
import multiprocessing

import arr_default


def slice_sum(data, _arr_sum):
    _sum = 0
    for num in data:
        _sum += num
    with _arr_sum.get_lock():
        _arr_sum.value += _sum


if __name__ == '__main__':
    count = arr_default.COUNT
    arr = arr_default.arr
    print(f'{len(arr) = }')

    time_total = time.time()
    idx_range = int(len(arr) / count)
    print(f'{idx_range = }')

    arr_sum = multiprocessing.Value('i', 0)
    i = 0
    processes = []
    for _ in range(count):
        t = multiprocessing.Process(target=slice_sum, args=(arr[i: i + idx_range], arr_sum))
        processes.append(t)
        t.start()
        i += idx_range
    if i < len(arr):
        t = multiprocessing.Process(target=slice_sum, args=(arr[i:], arr_sum))
        processes.append(t)
        t.start()

    for t in processes:
        t.join()

    print(arr_sum.value)

    print(f"всего затрачено - {time.time() - time_total:.4f} sec.")
    print(f"check - {sum(arr) = }")
