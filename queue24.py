"""
This version works on Python 2.4 to 2.6.
http://docs.python.org/library/queue
http://docs.python.org/library/threading
"""

from Queue import Queue, Empty
from threading import Thread

num_worker_threads = 5


def source():
    return xrange(100)


def do_work(o):
    print o


def worker():
    while True:
        try:
            item = q.get_nowait()
        except Empty:
            break
        do_work(item)


if __name__ == '__main__':
    q = Queue()

    for item in source():
        q.put(item)

    threads = []

    for i in range(num_worker_threads):
        t = Thread(target=worker)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print "Finished"
# The entire Python program exits when no alive non-daemon threads are left.
