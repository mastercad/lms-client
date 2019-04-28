#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import players.LMSPlayer as LMSPlayer
import players.VLCPlayer as VLCPlayer

from Exceptions import ServerNotFoundException
from Exceptions import ClientNotFoundException


def provide():
    """

    :rtype: Player|VLCPlayer
    """
    try :
        return LMSPlayer.get_client()
    except (ClientNotFoundException, ServerNotFoundException):
        return VLCPlayer.get_client()
