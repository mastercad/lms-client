#!/usr/bin/env python2
from Buttons import Buttons
from NFC import NFC
from Volume import Volume


def has_live_threads(threads):
    return True in [thread.isAlive() for thread in threads]


def main():
    threads = []

    button = Buttons()
    button.start()
    threads.append(button)

    volume = Volume()
    volume.start()
    threads.append(volume)

    nfc = NFC()
    nfc.start()
    threads.append(nfc)

    while has_live_threads(threads):
        try:
            # synchronization timeout of threads kill
            [thread.join(1) for thread in threads
             if thread is not None and thread.isAlive()]
        except KeyboardInterrupt:
            # Ctrl-C handling and send kill to threads
            print "Sending kill to threads..."
            for thread in threads:  # type: thread
                thread.stop()

    print "Exited"


if __name__ == '__main__':
    main()
