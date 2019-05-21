#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import LMSPlayer as LMSPlayer
import VLCPlayer as VLCPlayer
from Exceptions import ClientNotFoundException


def produce(online):
    print ("Is Online in PlayerFactory:"+str(online))
    """

    :rtype: Player|VLCPlayer
    """
    if online is True:
        try:
            print ("Erstelle LMS Player!")
            return LMSPlayer.get_client()
        except ClientNotFoundException as exception:
            print ("Erstelle VLC Player!")
            return VLCPlayer.get_client()
    else:
        print ("Erstelle VLC Player!")
        return VLCPlayer.get_client()
