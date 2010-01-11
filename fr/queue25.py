"""
This version works on Python 2.5 and 2.6.
http://docs.python.org/library/queue
http://docs.python.org/library/threading
"""

from Queue import Queue
from threading import Thread

num_worker_threads = 5


def source():
    return xrange(100)


def do_work(o):
    print o


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
#        t.daemon = True  # for Python 2.6 only
        t.setDaemon(True)  # for Python 2.4 to 2.6
        t.start()

    for item in source():
        q.put(item)

    q.join()  # block until all tasks are done
    
    print "Finished"
# The entire Python program exits when no alive non-daemon threads are left.
