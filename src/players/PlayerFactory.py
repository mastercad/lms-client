#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import players.LMSPlayer as LMSPlayer
import players.VLCPlayer as VLCPlayer


def produce(online):
    print ("Is Online in PlayerFactory:"+str(online))
    """

    :rtype: Player|VLCPlayer
    """
    if online is True:
        print ("Erstelle LMS Player!")
        return LMSPlayer.get_client()
    else:
        print ("Erstelle VLC Player!")
        return VLCPlayer.get_client()
