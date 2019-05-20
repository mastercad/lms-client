#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import Config
from MediaEntity import MediaEntity


class MediaPathResolver:

    def __init__(self):
        self.is_online = False
        self.config = Config.get_config()
        self.media_entity = None

    def set_online(self, is_online):
        self.is_online = is_online
        return self

    def resolve(self, media_entity):
        self.media_entity = media_entity

        """

        :param media_entity: MediaEntity

        :return: str
        """
        if self.is_online:
            return self.resolve_lms_media_path()
        else:
            return self.resolve_local_media_path()

    def resolve_lms_media_path(self):
        media_path = None
#        if "playlist" == self.media_entity.get_type():
        media_path = "favorites playlist play item_id:0"
            #  media_path = "playlist id "+str(self.media_entity.get_lms_name())
        return media_path

    def resolve_local_media_path(self):
        local_base_bath = self.config.get('offline', 'directory')
        media_path = local_base_bath+"/"+str(self.media_entity.get_local_name())
        return media_path