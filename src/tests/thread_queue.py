#!/usr/bin/env python2

from Queue import Queue
from threading import Thread
import time


def producer(out_q):
    time.sleep(5)
    out_q.put('hello')


def consumer(in_q):
    h = in_q.get()
    print(h + ' world!')
    in_q.task_done()


q = Queue()
t1 = Thread(target=producer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t3 = Thread(target=consumer, args=(q,))

t1.start()
t2.start()
t3.start()

q.join()
print('q joined!')
