#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from types import NoneType

from players import PlayerFactory
from players.LMSPlayer import LMSPlayer
from players.VLCPlayer import VLCPlayer
import LMSAvailabilityCheck
from MediaPathResolver import MediaPathResolver


class MediaManager:

    def __init__(self, buttons):
        self.player = None
        self.buttons = buttons
        self.media_entity = None

    def manage(self, media_entity):

        """

        :param media_entity: MediaEntity

        :return:
        """

        if isinstance(self.player, VLCPlayer):
            self.player.stop()

        self.media_entity = media_entity
        self.is_online = LMSAvailabilityCheck.check()
        
        if self.player is None:
            self.player = PlayerFactory.produce(self.is_online)

        # Falls es Probleme beim erstellen des LMS Players gab, in offline modus wechseln
        if not isinstance(self.player, LMSPlayer):
            self.is_online = False

        self.buttons.set_player(self.player)

        resolver = MediaPathResolver()
        media_path = resolver.resolve(self.media_entity, self.is_online)

        self.player.play(media_path)

    def __del__(self):
        if type(self.player) is not NoneType:
            self.player.stop()
