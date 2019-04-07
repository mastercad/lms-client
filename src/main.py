#!/usr/bin/env python2
from Buttons import Buttons
from NFC import NFC
from Volume import Volume

button = Buttons()
button.start()

volume = Volume()
volume.start()

nfc = NFC()
nfc.start()
