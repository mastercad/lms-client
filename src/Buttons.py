#!/usr/bin/env python2
import RPi.GPIO as GPIO
import threading

import Config
import LMSClient

config = Config.get_config()

pin_btn_next = config.get('gpio', 'next')
pin_btn_prev = config.get('gpio', 'prev')
pin_btn_play = config.get('gpio', 'play')

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_btn_next, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(pin_btn_prev, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(pin_btn_play, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


# def button1(channel):
def btn_next():
    # GPIO.remove_event_detect(5);
    print("Button next pressed!")


# def button2(channel):
def btn_prev():
    print("Button prev pressed!")


# def button3(channel):
def btn_play():
    print("Button play pressed!")


class Buttons(threading.Thread):
    def run(self):
        delay_counter = 0

        while True:
            if 5000 < delay_counter:
                delay_counter = 0  # type: int
            if GPIO.input(pin_btn_next):
                btn_next()
            if GPIO.input(pin_btn_prev):
                btn_prev()
            if GPIO.input(pin_btn_play):
                btn_play()
            delay_counter += 1
