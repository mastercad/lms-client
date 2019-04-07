#!/usr/bin/env python2
import threading
import time
import RPi.GPIO as GPIO
import MFRC522
import signal

import DatabaseProvider


class NFC(threading.Thread):
    # Capture SIGINT for cleanup when the script is aborted
    def end_read(signal, frame):
        global continue_reading
        print "Ctrl+C captured, ending read."
        continue_reading = False
        GPIO.cleanup()

    def run(self):
        continue_reading = True

        # Hook the SIGINT
        signal.signal(signal.SIGINT, self.end_read())

        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()

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
