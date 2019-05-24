#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from threading import Thread

import RPi.GPIO as GPIO
import threading
import time

import Config

config = Config.get_config()

pin_btn_next        = config.getint('gpio', 'next')
pin_btn_prev        = config.getint('gpio', 'prev')
pin_btn_play        = config.getint('gpio', 'play')
pin_btn_volume_up   = config.getint('gpio', 'volume_up')
pin_btn_volume_down = config.getint('gpio', 'volume_down')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_btn_next, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_btn_prev, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_btn_play, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_btn_volume_up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_btn_volume_down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


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
    print ("Play/Pause pressed")
    time.sleep(.5)


def btn_volume_up(player):
    player.prev()
    print("Button volume up pressed!")
    time.sleep(.1)


def btn_volume_down(player):
    player.prev()
    print("Button volume down pressed!")
    time.sleep(.1)


class Buttons(threading.Thread):
    def __init__(self, player=None):
        super(Buttons, self).__init__()
        self.setName("Buttons Thread")

        if player is not None:
            self.player = player

        self.running = True
        self._stop_event = threading.Event()

    def stop(self):
        self.running = False
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        delay_counter = 0

        while self.running:
            # hier ist eine logik vorgesehen um auf eine bestimmte dauer des drückens zu reagieren (natürlich ist 5000 bei 0.5 sleep etwas hoch...)
            if 5000 < delay_counter:
                delay_counter = 0  # type: int
            if GPIO.input(pin_btn_next):
                btn_next(self.player)
            if GPIO.input(pin_btn_prev):
                btn_prev(self.player)
            if GPIO.input(pin_btn_play):
                btn_toggle_play(self.player)
            if GPIO.input(pin_btn_volume_up):
                btn_volume_up(self.player)
            if GPIO.input(pin_btn_volume_down):
                btn_volume_down(self.player)

            time.sleep(.01)
            delay_counter += 1

    def set_player(self, player):
        self.player = player
        return self
