#!/usr/bin/env python2
try:
    threads = []

    from Exceptions import ClientNotFoundException
    from Exceptions import ServerNotFoundException
    from Buttons import Buttons
    from NFC import NFC
    from Volume import Volume
    import RPi.GPIO as GPIO

    def has_live_threads(threads):
        return True in [thread.isAlive() for thread in threads]


    def main():
        global threads

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
                # synchronization timeout of threads kill
            [thread.join(1) for thread in threads
             if thread is not None and thread.isAlive()]

    if __name__ == '__main__':
        main()

except (KeyboardInterrupt, ClientNotFoundException, ServerNotFoundException) as exception:
    # Ctrl-C handling and send kill to threads
    print exception
    print "Sending kill to threads..."

    for thread in threads:  # type: thread
        thread.stop()

    GPIO.cleanup()
    print "Exited"
