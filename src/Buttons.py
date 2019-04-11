#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import threading
import time

import Config
import LMSClient

client = LMSClient.get_client()
config = Config.get_config()

pin_btn_next = config.getint('gpio', 'next')
pin_btn_prev = config.getint('gpio', 'prev')
pin_btn_play = config.getint('gpio', 'play')

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_btn_next, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_btn_prev, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_btn_play, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# def button1(channel):
def btn_next():
    # GPIO.remove_event_detect(5);
    client.next()
    print("Button next pressed!")


# def button2(channel):
def btn_prev():
    client.prev()
    print("Button prev pressed!")


# def button3(channel):
def btn_toggle_play():
    client.toggle()


class Buttons(threading.Thread):
    def __init__(self):
        self.running = True
        super(Buttons, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self.running = False
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        delay_counter = 0

        while self.running:
            if 5000 < delay_counter:
                delay_counter = 0  # type: int
            if GPIO.input(pin_btn_next):
                btn_next()
                time.sleep(.5)
            if GPIO.input(pin_btn_prev):
                btn_prev()
                time.sleep(.5)
            if GPIO.input(pin_btn_play):
                btn_toggle_play()
                time.sleep(.5)
            delay_counter += 1
