#!/usr/bin/env python2

import threading
import time

#def loop1_10():
#    for i in range(1, 11):
#        time.sleep(1)
#        print(i)

#threading.Thread(target=loop1_10()).start()
#threading.Thread(target=loop1_10()).start()
#threading.Thread(target=loop1_10()).start()


class MyThread(threading.Thread):
    def run(self):
        print("{} started!".format(self.getName()))
        time.sleep(1)
        print("{} finished!".format(self.getName()))

def main():
    for x in range(4):
        myThread = MyThread(name="Thread-{}".format(x + 1))
        myThread.start()
        time.sleep(.9)

if __name__ == '__main__':main()
