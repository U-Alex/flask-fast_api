import time
import threading

import arr_default


def slice_sum(data):
    _sum = 0
    for num in data:
        _sum += num
    return _sum


if __name__ == '__main__':
    count = arr_default.COUNT
    arr = arr_default.arr
    print(f'{len(arr) = }')

    time_total = time.time()
    idx_range = int(len(arr) / count)
    print(f'{idx_range = }')

    i = 0
    threads = []
    arr_sum = []
    for _ in range(count):
        t = threading.Thread(target=arr_sum.append, args=(slice_sum(arr[i: i + idx_range]),))
        threads.append(t)
        t.start()
        i += idx_range
    if i < len(arr):
        t = threading.Thread(target=arr_sum.append, args=(slice_sum(arr[i:]),))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(sum(arr_sum))

    print(f"всего затрачено - {time.time() - time_total:.4f} sec.")
    print(f"check - {sum(arr) = }")
