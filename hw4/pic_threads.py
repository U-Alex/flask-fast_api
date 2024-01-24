from sys import argv
import time
import requests
import threading

import pic_default_urls


def get_pic(pic_url):
    time_pic = time.time()
    response = requests.get(pic_url)
    filename = 'pics/' + 'thread__' + pic_url.split('/')[-1]
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"{filename} - {time.time() - time_pic:.2f} sec.")


if __name__ == '__main__':
    urls = [arg for arg in argv[1:]] if len(argv) > 1 else pic_default_urls.default_url
    time_total = time.time()

    threads = []
    for url in urls:
        t = threading.Thread(target=get_pic, args=(url,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    print(f" всего затрачено - {time.time() - time_total:.2f} sec.")

