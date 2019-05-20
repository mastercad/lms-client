#!/usr/bin/env python2
# -*- coding: utf8 -*-
from pylms.player import Player

import Config
import LMSServerProvider
from Exceptions import ClientNotFoundException


def get_client():
    """

    :rtype: Player
    """
#    config = Config.get_config()

#    server = LMSServerProvider.provide()
#    player = server.get_player(config.get('lms', 'client_name'))  # type: Player

#    if type(player) is not Player:
#        exception_message = "Client \""+config.get('lms', 'client_name')+"\" nicht gefunden"
#        raise ClientNotFoundException(exception_message)

#    return player
    return LMSPlayer()


class LMSPlayer:
    def __init__(self):
        self.config = Config.get_config()
        self.server = LMSServerProvider.provide()
        self.player = self.server.get_player(self.config.get('lms', 'client_name'))  # rtype: Player
#        self.current_file = self.load_last_played_file()
        self.paused=False

    def toggle(self):
        self.player.toggle()
#        if self.player.is_playing():
#            self.paused=True
#            self.player.pause()
#        else:
#            self.play_file(self.load_last_played_file())

    def next(self):
        self.player.next()
        return

    def prev(self):
        self.player.prev()
        return

    def play(self, media_file=None):
        self.current_file = media_file
        # altlast, kann eventuell weg, war geplant um mit dem alten lied weiter zu machen
        # wenn main neu gestartet wurde
#        if "" == self.current_file:
#            self.current_file = self.load_last_played_file()
        if media_file is not None:
            print ("MediaFile: "+str(media_file))
            self.player.request(media_file)
        self.player.play()

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


