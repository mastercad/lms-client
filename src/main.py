#!/usr/bin/env python2
# -*- coding: utf-8 -*-

try:
    threads = []
    queues = []

    import os
    import socket
    import time

    import RPi.GPIO as GPIO
    import Queue

    import Database
    import MediaMapper
    from MediaEntity import MediaEntity
    from MediaManager import MediaManager
    from Buttons import Buttons
    from NFC import NFC
    from Time import monotonic_time

    last_key = None


    def has_live_threads(threads):
        return True in [thread.isAlive() for thread in threads]


    def main():
        global threads
        global queues
        global last_key
        global is_online
        global player

        database = Database.Database()

        buttons = Buttons()
        buttons.start()
        
        threads.append(buttons)

        nfc_queue = Queue.Queue()
        queues.append(nfc_queue)

        nfc = NFC(nfc_queue)
        nfc.start()
        threads.append(nfc)

        media_manager = MediaManager(buttons)

        while has_live_threads(threads):
            # synchronization timeout of threads kill
            [thread.join(1) for thread in threads
            if thread is not None and thread.isAlive()]

            # da hier scheinbar nur bei änderungen an der queue eine nachricht kommt, bzw aufgelegtem tag,
            # könnte man hier das emtfernen eines tags vernachlässigen, bzw. irgendwie hier prüfen.
            # oder das in einen eigenen thread auslagern, der sich dann um die verarbeitung kümmert, wenn nichts kommt
            (key, value) = get_timed_interruptable_precise(nfc_queue, timeout=1)

            
            if key != last_key:
                last_key = key

                media_entity = MediaMapper.generate(database.find(key))

                if media_entity.get_rfid() is not None:
                    print ("Neuer Chip erkannt!")
                    media_manager.manage(media_entity)
                else:
                    print ("RFID nicht gefunden!")


    def get_timed_interruptable_precise(queue, timeout):
        timeout += monotonic_time()
        while True:
            try:
                return queue.get(timeout=max(0, timeout - monotonic_time()))
            except Exception:
                pass

    if __name__ == '__main__':
        main()

except (KeyboardInterrupt, Exception) as exception:
    import sys
    import traceback

#    exc_type, exc_obj, exc_tb = sys.exc_info()
#    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#    print (exception)
#    print (exc_type, fname, exc_tb.tb_lineno)
#    print (traceback.format_exc())
#    print ("Sending kill to threads...")

    for thread in threads:  # type: thread
        thread.stop()

    for queue in queues:  # type: Queue
        queue.queue.clear()

    GPIO.cleanup()
    print ("Exited")
