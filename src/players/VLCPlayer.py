#!/usr/bin/env python2
# -*- coding: utf8 -*-
import Config
import vlc
from vlc import MediaPlayer
from vlc import Media


def get_client():
    """

    :rtype: VLCPlayer
    """
    return VLCPlayer()


class VLCPlayer():
    def __init__(self):
        self.vlc_instance = vlc.Instance()  # :rtype: vlc
        self.player = self.vlc_instance.media_player_new()
        self.config = Config.get_config()

    def toggle(self):
        if self.player.is_playing():
            self.player.stop()
        else:
            self.player.play()

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))

    def get_volume(self):
        return self.player.audio_get_volume()

    def play_file(self, media_file_path):
        media = self.player.get_media()  # :rtype: Media
        media_file = Media(media_file_path)
#        self.set_media(media_file)
