#!/usr/bin/env python2
from pylms.player import Player

import Config
import LMSServerProvider


def get_client():
    """

    :rtype: Player
    """
    config = Config.get_config()

    server = LMSServerProvider.provide()
    player = server.get_player(config.get('lms', 'client_name'))  # type: Player

    return player
