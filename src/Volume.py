#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import time
import RPi.GPIO as GPIO

import LMSClient

GPIO.setmode(GPIO.BCM)

CH = 0    # Analog/Digital-Channel
CLK = 27  # Clock
DIN = 19  # Digital in
DOUT = 6  # Digital out
CS = 26   # Chip-Select

GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(CS,   GPIO.OUT)

HIGH = True
LOW = False
oldValue = 1
maxValue = 1024

client = LMSClient.get_client()


def read_analog_data(adCh, CLKPin, DINPin, DOUTPin, CSPin):
    global oldValue
    global maxValue
    GPIO.output(CSPin, HIGH)
    GPIO.output(CSPin, LOW)
    GPIO.output(CLKPin, LOW)

    cmd = adCh
    cmd |= 0b00011000

    for i in range(5):
        if cmd & 0x10:  # 4. Bit prüfen und mit 0 anfangen
            GPIO.output(DINPin, HIGH)
        else:
            GPIO.output(DINPin, LOW)
        # Clocksignal negative Flanke erzeugen
        GPIO.output(CLKPin, HIGH)
        GPIO.output(CLKPin, LOW)
        cmd <<= 1 # Bitfolge eine Position nach links verschieben

    # Datenabruf
    adchvalue = 0 # Wert auf 0 zuruecksetzen
    for i in range(11):
        GPIO.output(CLKPin, HIGH)
        GPIO.output(CLKPin, LOW)
        adchvalue <<= 1 # 1 Postition nach links schieben
        if(GPIO.input(DOUTPin)):
            adchvalue |= 0x01

    time.sleep(0.5)

    minTolerance = oldValue - 100
    maxTolerance = oldValue + 100

#    print("MinTolerance: "+str(minTolerance))
#    print("MaxTolerance: "+str(maxTolerance))
#    print("adchvalue: "+str(adchvalue))

    if minTolerance <= adchvalue <= maxTolerance:
        oldValue = adchvalue

    if oldValue < 1:
        return 0

    volume = (oldValue / float(maxValue)) * 100
    return (int(volume) / 5) * 5


class Volume(threading.Thread):
    def __init__(self):
        self.running = True
        super(Volume, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self.running = False
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while self.running:
            volume = read_analog_data(CH, CLK, DIN, DOUT, CS)
            client.set_volume(volume)
