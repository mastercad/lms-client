#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#from docutils.nodes import system_message

try:
    threads = []
    queues = []

    import RPi.GPIO as GPIO
    import time
    import Queue
    import ctypes
    import os
    import socket

    import players.PlayerFactory as PlayerFactory
    import LMSAvailabilityCheck
    from Exceptions import ClientNotFoundException
    from Exceptions import ServerNotFoundException
    from MediaManager import MediaManager
    import MediaMapper
    from Buttons import Buttons
    from NFC import NFC
    from MediaEntity import MediaEntity
    from Database import Database

#    from Volume import Volume

    CLOCK_MONTONIC_RAW = 4

    last_key = None

    class timespec(ctypes.Structure):
        _fields_ = [
            ('tv_sec', ctypes.c_long),
            ('tv_nsec', ctypes.c_long)
        ]

    librt = ctypes.CDLL('librt.so.1', use_errno=True)
    clock_gettime = librt.clock_gettime
    clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

    def monotonic_time():
        time_spec = timespec()
        if 0 != clock_gettime(CLOCK_MONTONIC_RAW, ctypes.pointer(time_spec)):
            errno_ = ctypes.get_errno()
            raise OSError(errno_, os.strerror(errno_))
        return time_spec.tv_sec + time_spec.tv_nsec * 1e-9


    def has_live_threads(threads):
        return True in [thread.isAlive() for thread in threads]


    def main():
        global threads
        global queues
        global last_key
        global is_online
        global player

        buttons = Buttons()
        buttons.start()
        threads.append(buttons)

#        volume = Volume(player)
#        volume.start()
#        threads.append(volume)

        nfc_queue = Queue.Queue()
        queues.append(nfc_queue)

        nfc = NFC(nfc_queue)
        nfc.start()
        threads.append(nfc)

        media_manager = MediaManager(buttons)

#        online_state_queue = Queue.Queue()
#        queues.append(online_state_queue)

        while has_live_threads(threads):

            # das dient später einem dynamischen austausch der player wenn während der wiedergabe der LMS weg ist
#            online_state = LMSAvailabilityCheck.check()

            # synchronization timeout of threads kill
            [thread.join(1) for thread in threads
            if thread is not None and thread.isAlive()]

            # da hier scheinbar nur bei änderungen an der queue eine nachricht kommt, bzw aufgelegtem tag,
            # könnte man hier das emtfernen eines tags vernachlässigen, bzw. irgendwie hier prüfen.
            # oder das in einen eigenen thread auslagern, der sich dann um die verarbeitung kümmert, wenn nichts kommt
            (key, value) = get_timed_interruptable_precise(nfc_queue, timeout=1)
#            is_online = get_timed_interruptable_precise(online_state_queue, timeout=1)

            if key != last_key:
                last_key = key

                media_entity = MediaMapper.generate(key, value)

                if isinstance(media_entity, MediaEntity):
                    media_manager.manage(media_entity)
                else:
                    print ("Media File Not Found!")
#            time.sleep(0.1)


    def get_timed_interruptable_precise(queue, timeout):
        timeout += monotonic_time()
        while True:
            try:
                return queue.get(timeout=max(0, timeout - monotonic_time()))
            except Exception:
                pass

    if __name__ == '__main__':
        main()

#except (KeyboardInterrupt, ClientNotFoundException, ServerNotFoundException) as exception:
except (KeyboardInterrupt, Exception) as exception:
    import sys
    import traceback

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print (exception)
    print (exc_type, fname, exc_tb.tb_lineno)
    print (traceback.format_exc())
    print ("Sending kill to threads...")

    for thread in threads:  # type: thread
        thread.stop()

    for queue in queues:  # type: Queue
        queue.queue.clear()

    GPIO.cleanup()
    print ("Exited")
