#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import players.LMSPlayer as LMSPlayer
import players.VLCPlayer as VLCPlayer


def produce(online):
    """

    :rtype: Player|VLCPlayer
    """
    if online is True:
        return LMSPlayer.get_client()
    else:
        return VLCPlayer.get_client()
