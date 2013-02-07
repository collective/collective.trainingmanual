"""
This version works only on both Python 2.6 and Python 3.1.
http://docs.python.org/library/queue
http://docs.python.org/library/threading
"""

try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from threading import Thread

num_worker_threads = 5


def source():
    return range(100)


def do_work(o):
    print(o)


def worker():
    while True:
        item = q.get()
        # will always block, but the thread is
        # daemonized, so it's ok.
        do_work(item)
        q.task_done()


if __name__ == '__main__':
    q = Queue()
    for i in range(num_worker_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for item in source():
        q.put(item)

    q.join()  # block until all tasks are done
    
    print("Finished")
# The entire Python program exits when no alive non-daemon threads are left.
