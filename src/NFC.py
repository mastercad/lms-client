#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from threading import Thread, Event
import time

import RPi.GPIO as GPIO #  only import for avoid warnings from GPIO

from mfrc522 import SimpleMFRC522


# if the player run and the write tool is used, warnings spawn and have no effect => disable
GPIO.setwarnings(False)


class NFC(Thread):
    def __init__(self, queue):
        super(NFC, self).__init__()
        self.MFRC522 = SimpleMFRC522()
        self.setName("NFC Thread")

        self.queue = queue
        self.running = True
        self._stop_event = Event()
        self.old_reader_content = None

    def stop(self):
        self.running = False
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while self.running:
            reader_content = self.MFRC522.read()

            if reader_content is not None and self.old_reader_content != reader_content:
                self.queue.queue.clear()
                self.old_reader_content = reader_content
                self.queue.put(reader_content)

            time.sleep(0.1)