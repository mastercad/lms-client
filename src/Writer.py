#!/usr/bin/env python2
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import mfrc522

import Config
import Tools

GPIO.setwarnings(False)

card_key = Tools.convert_string_to_int_array(Config.get_config().get('nfc', 'card_key'))


def write(data):
    global card_key

    # Create an object of the class MFRC522
    RFID = mfrc522.MFRC522()

    # Scan for cards
    (status, TagType) = RFID.MFRC522_Request(RFID.PICC_REQIDL)

    # Get the UID of the card
    (status, uid) = RFID.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == RFID.MI_OK:

        # Select the scanned tag
        RFID.MFRC522_SelectTag(uid)

        # Authenticate
        status = RFID.MFRC522_Auth(RFID.PICC_AUTHENT1A, 8, card_key, uid)

        # Check if authenticated
        if status == RFID.MI_OK:

            # Variable for the data to write
            empty_data = []

            # Fill the data with 0xFF
            for x in range(0, 16):
                empty_data.append(255)

            # Clean the Chip
            RFID.MFRC522_Write(8, empty_data)

            # Write the data
            RFID.MFRC522_Write(8, data)

            # Stop
            RFID.MFRC522_StopCrypto1()
        else:
            print "Authentication error"
