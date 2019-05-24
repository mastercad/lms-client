#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import time
import RPi.GPIO as GPIO #  only import for avoid warnings from GPIO

import Reader

# if the player run and the write tool is used, warnings spawn and have no effect => disable
GPIO.setwarnings(False)


class NFC(threading.Thread):
    def __init__(self, queue):
        super(NFC, self).__init__()
        self.setName("NFC Thread")

        self.queue = queue
        self.running = True
        self._stop_event = threading.Event()
        self.old_reader_content = None

    def stop(self):
        self.running = False
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while self.running:
            reader_content = Reader.read()

            if reader_content is not None and self.old_reader_content != reader_content:
                self.queue.queue.clear()
                self.old_reader_content = reader_content
                self.queue.put(reader_content)

            time.sleep(0.1)