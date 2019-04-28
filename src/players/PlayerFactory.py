#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import players.LMSPlayer as LMSPlayer
import players.VLCPlayer as VLCPlayer

ONLINE = 1
OFFLINE = 2


def produce(onlineState):
    """

    :rtype: Player|VLCPlayer
    """
    if onlineState is ONLINE:
        return LMSPlayer.get_client()
    elif onlineState is OFFLINE:
        return VLCPlayer.get_client()
