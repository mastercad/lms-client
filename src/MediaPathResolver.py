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

    def resolve(self, media_entity, is_online):
        """

        :param MediaEntity media_entity:
        :param bool is_online:

        :return:
        """
        self.media_entity = media_entity
        self.is_online = is_online

        if self.is_online:
            return self.resolve_lms_media_path()
        else:
            return self.resolve_local_media_path()

    def resolve_lms_media_path(self):
        return self.media_entity.get_lms_name()

    def resolve_local_media_path(self):
        local_base_bath = self.config.get('offline', 'directory')
        media_path = local_base_bath+"/"+str(self.media_entity.get_local_name())
        return media_path