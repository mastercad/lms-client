#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

CH = 0    # Analog/Digital-Channel
CLK = 23  # Clock / SCLK BCM 11
DIN = 19  # Digital in / MOSI BCM 10
DOUT = 21  # Digital out / MISO BCM 9
CS = 26   # Chip-Select BCM 7

GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(CS,  GPIO.OUT)
GPIO.setup(DOUT,GPIO.IN)

HIGH = True
LOW = False

INIT_VALUE = 9999999999
maxValue = 1024
prevValue = INIT_VALUE


def read_analog_data_with_tollerance(adCh, CLKPin, DINPin, DOUTPin, CSPin):
    global maxValue
    global prevValue
    global INIT_VALUE

    cmd=adCh
    cmd |= 0b00011000

    GPIO.output(CSPin, HIGH)
    GPIO.output(CSPin, LOW)
    GPIO.output(CLKPin, LOW)

    for i in range(5):
        if (cmd & 0x10): # 4. Bit prüfen und mit 0 anfangen
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

    if prevValue == INIT_VALUE:
        prevValue = adchvalue

    min_tolerance = prevValue - 100
    max_tolerance = prevValue + 100

#    print "Min: "+str(min_tolerance)
#    print "Max: "+str(max_tolerance)
#    print "Current: "+str(adchvalue)
#    print "Old: "+str(prevValue)

    if min_tolerance <= adchvalue <= max_tolerance:
        prevValue = adchvalue

    if prevValue < 1:
        return 0

    return round((float(prevValue) / float(maxValue)) * 100)


def read_analog_data_with_average(adCh, CLKPin, DINPin, DOUTPin, CSPin):
    global maxValue

    current_count = 0
    current_value = 0

    while current_count < 20:

        cmd=adCh
        cmd |= 0b00011000

        GPIO.output(CSPin, HIGH)
        GPIO.output(CSPin, LOW)
        GPIO.output(CLKPin, LOW)

        for i in range(5):
            if (cmd & 0x10): # 4. Bit prüfen und mit 0 anfangen
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

        current_value += adchvalue
        current_count += 1

    current_value = float(current_value) / float(current_count)

    if prevValue < 1:
        return 0

    return round((float(current_value) / float(maxValue)) * 100)


def read_analog_data(adCh, CLKPin, DINPin, DOUTPin, CSPin):
    global maxValue

    cmd=adCh
    cmd |= 0b00011000

    GPIO.output(CSPin, HIGH)
    GPIO.output(CSPin, LOW)
    GPIO.output(CLKPin, LOW)

    for i in range(5):
        if (cmd & 0x10): # 4. Bit prüfen und mit 0 anfangen
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

    if prevValue < 1:
        return 0

    return round((float(adchvalue) / float(maxValue)) * 100)


class Volume(threading.Thread):

    def __init__(self, player):
        self.running = True
        self.player = player
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
            time.sleep(0.5)
            print "Volume: "+str(volume)
            self.player.set_volume(volume)
