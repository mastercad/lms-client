#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from players import PlayerFactory
import LMSAvailabilityCheck
from MediaPathResolver import MediaPathResolver
from players.LMSPlayer import LMSPlayer


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

        self.media_entity = media_entity
        self.is_online = LMSAvailabilityCheck.check()
        self.player = PlayerFactory.produce(self.is_online)

        # Falls es Probleme beim erstellen des Players gab, in offline modus wechseln
        if type(self.player) is not LMSPlayer:
            self.is_online = False

        self.buttons.set_player(self.player)

        resolver = MediaPathResolver()
        media_path = resolver.resolve(self.media_entity, self.is_online)

        self.player.play(media_path)

    def __end(self):
        print ("Ende "+str(type(self)))
        self.player.stop()