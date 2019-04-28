#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import threading
import time

import Config
import LMSClient

config = Config.get_config()

pin_btn_next = config.getint('gpio', 'next')
pin_btn_prev = config.getint('gpio', 'prev')
pin_btn_play = config.getint('gpio', 'play')

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_btn_next, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_btn_prev, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_btn_play, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def btn_next(player):
    # GPIO.remove_event_detect(5);
    player.next()
    print("Button next pressed!")
    time.sleep(.5)


def btn_prev(player):
    player.prev()
    print("Button prev pressed!")
    time.sleep(.5)


def btn_toggle_play(player):
    player.toggle()
    time.sleep(.5)


class Buttons(threading.Thread):
    def __init__(self, player):
        self.player = player
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
                btn_next(self.player)
            if GPIO.input(pin_btn_prev):
                btn_prev(self.player)
            if GPIO.input(pin_btn_play):
                btn_toggle_play(self.player)

            time.sleep(.1)
            delay_counter += 1
