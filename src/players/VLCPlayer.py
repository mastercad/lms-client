#!/usr/bin/env python2
# -*- coding: utf8 -*-
import Config
import vlc
import os
from vlc import MediaPlayer
from vlc import Media


def get_client():
    """

    :rtype: VLCPlayer
    """
    return VLCPlayer()


class VLCPlayer:
    def __init__(self):
        self.config = Config.get_config()
        self.vlc_instance = vlc.Instance()  # :rtype: vlc
        self.player = self.vlc_instance.media_player_new()  # :rtype: MediaPlayer
        self.current_file = self.load_last_played_file()
        self.paused=False

    def toggle(self):
        if self.player.is_playing():
            self.paused=True
            self.player.pause()
        else:
            self.play_file(self.load_last_played_file())

    def next(self):
        if self.paused is False and self.player.is_playing:
            self.player.stop()
        return

    def prev(self):
        if self.paused is False and self.player.is_playing:
            self.player.stop()
            self.player.play()
        return

    def play(self, media_file):
        self.current_file = media_file
        # altlast, kann eventuell weg, war geplant um mit dem alten lied weiter zu machen
        # wenn main neu gestartet wurde
        if "" == self.current_file:
            self.current_file = self.load_last_played_file()
        self.play_file(media_file)

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))

    def get_volume(self):
        return self.player.audio_get_volume()

    def play_file(self, media_file_path):
        if False is self.paused:
            self.player.set_media(Media(media_file_path))
            self.paused=False
        self.player.play()

    def load_last_played_file(self):
        last_played_file_path_name = self.generate_last_played_file_path()
        self.ensure_file_exists(last_played_file_path_name)
        last_played_file = open(last_played_file_path_name, 'r')
        return last_played_file.read()

    def save_last_played_file(self, current_played_file):
        last_played_file_path_name = self.generate_last_played_file_path()
        self.ensure_file_exists(last_played_file_path_name)
        last_played_file = open(last_played_file_path_name, 'w')
        return last_played_file.write(current_played_file)

    def generate_last_played_file_path(self):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        return current_directory+"/../../"+self.config.get('system', 'last_played_file')

    """
    methode in eigene file klasse oder ähnliches auslagern
    """
    @staticmethod
    def ensure_file_exists(file_path_name):
        if not os.path.exists(file_path_name):
            open(file_path_name, 'w').close()
        return os.path.exists(file_path_name)


