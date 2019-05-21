#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import time
import mfrc522

continue_reading = True


class NFC(threading.Thread):
    def __init__(self, queue):
        super(NFC, self).__init__()
        self.setName("NFC Thread")

        self.queue = queue
        self.running = True
        self._stop_event = threading.Event()

    def stop(self):
        self.running = False
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):

        # Create an object of the class MFRC522
        MIFAREReader = mfrc522.MFRC522()

        while self.running:
            time.sleep(0.1)
            self.queue.queue.clear()

            # Scan for cards
            (status,tag_type) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

#            print "Status: "+str(status)
#            print "TagType: "+str(tag_type)

            # If a card is found
            if status == MIFAREReader.MI_OK:
                # Get the UID of the card
                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                # If we have the UID, continue
                if status == MIFAREReader.MI_OK:

                    # This is the default key for authentication
                    card_key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                    # Select the scanned tag
                    MIFAREReader.MFRC522_SelectTag(uid)

                    # Authenticate
                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, card_key, uid)

                    # Check if authenticated
                    if status == MIFAREReader.MI_OK:
                        self.queue.put(
                            (
                                "%s:%s:%s:%s" % (uid[0], uid[1], uid[2], uid[3]),
                                ",".join("{0}".format(number) for number in MIFAREReader.MFRC522_Read(8))
                            )
                        )
                        MIFAREReader.MFRC522_StopCrypto1()

            # hier ist das problem, das immer wieder diese abfrage betreten wird, obwohl ein key aufgelegt ist
            # ich plane hier ein signal an den aufrufer zu senden per queue um zu signalisieren, dass der key entfernt wurde
#            elif MIFAREReader.MI_ERR == status and 0 == tag_type:
#                self.key_queue.put("EMPTY")
#                self.value_queue.put("EMPTY")
