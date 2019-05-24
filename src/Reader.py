#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from types import NoneType

import mfrc522
import RPi.GPIO as GPIO

import Config
import Tools

GPIO.setwarnings(False)

RFID = mfrc522.MFRC522()
card_key = Tools.convert_string_to_int_array(Config.get_config().get("nfc", "card_key"))


def read():
    global card_key
    global RFID

    # Scan for cards
    (status,tag_type) = RFID.MFRC522_Request(RFID.PICC_REQIDL)

    # If a card is found
    if status == RFID.MI_OK:
        # Get the UID of the card
        (status, uid) = RFID.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == RFID.MI_OK:

            # Select the scanned tag
            RFID.MFRC522_SelectTag(uid)

            # Authenticate
            status = RFID.MFRC522_Auth(RFID.PICC_AUTHENT1A, 8, card_key, uid)

            # Check if authenticated
            if status == RFID.MI_OK :
                reader_content = RFID.MFRC522_Read(8)
                if type(reader_content) is not NoneType:
                    RFID.MFRC522_StopCrypto1()

                    return [
                        "%s:%s:%s:%s" % (uid[0], uid[1], uid[2], uid[3])
                        , ",".join("{0}".format(number) for number in reader_content)
                    ]
#    return [None, None]