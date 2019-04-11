#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import time
import RPi.GPIO as GPIO

import LMSClient

GPIO.setmode(GPIO.BCM)

CH = 0    # Analog/Digital-Channel
CLK = 21  # Clock / SCLK
DIN = 20  # Digital in / MOSI
DOUT = 19  # Digital out / MISO
CS = 7   # Chip-Select

GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(DOUT,GPIO.IN)
GPIO.setup(CS,  GPIO.OUT)

HIGH = True
LOW = False

client = LMSClient.get_client()

oldValue = -999999
maxValue = 1024

def read_analog_data(adCh, CLKPin, DINPin, DOUTPin, CSPin):
    global oldValue
    global maxValue
    
    average_count = 0
    prevValue = oldValue
    average_volume = 0
    
    while average_count < 20:
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
    
        if -999999 == prevValue:
            prevValue = adchvalue
            
        time.sleep(0.01)
            
        minTolerance = prevValue - 100
        maxTolerance = prevValue + 100
                
        if minTolerance <= adchvalue <= maxTolerance:
            average_volume += adchvalue
            prevValue = adchvalue
            average_count += 1
            oldValue = adchvalue
    oldValue = average_volume / average_count
    
    if oldValue < 1:
        return 0

    return round((float(oldValue) / float(maxValue)) * 100)


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
        global oldValue
        oldValue = client.get_volume() / float(1024)
        while self.running:
            volume = read_analog_data(CH, CLK, DIN, DOUT, CS)
            print "Volume: "+str(volume)
            client.set_volume(volume)
