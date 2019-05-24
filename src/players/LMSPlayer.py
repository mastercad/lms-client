#!/usr/bin/env python2
# -*- coding: utf8 -*-
from types import NoneType
import os

from pylms.player import Player
from vlc import Media

import Config
import LMSServerProvider
from Exceptions import ClientNotFoundException


def get_client():
    """

    :rtype: Player
    """
    return LMSPlayer()


class LMSPlayer:
    def __init__(self):
        self.config = Config.get_config()
        self.server = LMSServerProvider.provide()
        player_name = self.config.get('lms', 'client_name')
        self.player = self.server.get_player(player_name)  # rtype: Player

        if type(self.player) is NoneType:
            raise ClientNotFoundException(str(player_name)+" ist scheinbar nicht gestartet")

        self.paused=self.player.is_player

    def toggle(self):
        self.player.toggle()

    def next(self):
        self.player.next()
        return

    def prev(self):
        self.player.prev()
        return

    def play(self, media_path=None):
        self.current_file = media_path
        # altlast, kann eventuell weg, war geplant um mit dem alten lied weiter zu machen
        # wenn main neu gestartet wurde
#        if "" == self.current_file:
#            self.current_file = self.load_last_played_file()
#        if media_file is not None:
#            self.player.request("playlist play 1")
#            print (self.player.request(str(self.config.get('lms', 'client_name'))+" playlist play /Musik/Musik/John_Lennon_-_Woman.mp3"))

#        self.player.play()
#        self.player.playlist_play("C:\Users\andre\Music\Musik\80erBalladen\John_Lennon_-_Woman.mp3")
#        self.player.playlist_play("/Music/Musik/80erBalladen/John_Lennon_-_Woman.mp3")
#        self.player.playlist_play("/Musikordner/Music/Musik/80erBalladen/John_Lennon_-_Woman.mp3")
#        self.player.playlist_play("C:/Users/andre/Music/Musik/80erBalladen/John_Lennon_-_Woman.mp3")
        self.player.playlist_play(media_path)

    def stop(self):
        self.player.stop()

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


