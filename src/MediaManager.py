#!/usr/bin/env python2
# -*- coding: utf-8 -*-


class MediaManager:

    def __init__(self, player, resolver):
        self.player = player
        self.resolver = resolver

    def manage(self, media_entity):
        """

        :param media_entity: MediaEntity

        :return:
        """
        self.player.play(self.resolver.resolve(media_entity))

    def set_player(self, player):
        self.player = player
        return self

    def set_resolver(self, resolver):
        self.resolver = resolver
        return self