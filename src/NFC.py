#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import time
import RPi.GPIO as GPIO
import mfrc522
import signal

import DatabaseProvider

continue_reading = True


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


class NFC(threading.Thread):
    def __init__(self):
        super(NFC, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        global continue_reading
        # Hook the SIGINT
        signal.signal(signal.SIGINT, end_read)

        # Create an object of the class MFRC522
        MIFAREReader = mfrc522.MFRC522()

        while continue_reading:
            # Scan for cards
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == MIFAREReader.MI_OK:
                print "Card detected"

            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

                # Print UID
                print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])

                # This is the default key for authentication
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print "Authentication error"

    def __del__(self):
        print("Exit NFC")
        GPIO.cleanup()
