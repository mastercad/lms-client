#!/usr/bin/env python2
# -*- coding: utf8 -*-

from vlc import MediaPlayer

player = MediaPlayer("/path/to/file.mp3")  # type: MediaPlayer

player.play()
