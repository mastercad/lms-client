#!/usr/bin/env python2
# -*- coding: utf8 -*-
from pylms.player import Player

import Config
import LMSServerProvider
from Exceptions import ClientNotFoundException


def get_client():
    """

    :rtype: Player
    """
    config = Config.get_config()

    server = LMSServerProvider.provide()
    player = server.get_player(config.get('lms', 'client_name'))  # type: Player

    if type(player) is not Player:
        exception_message = "Client \""+config.get('lms', 'client_name')+"\" nicht gefunden"
        raise ClientNotFoundException(exception_message)

    return player
