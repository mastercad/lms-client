#!/usr/bin/env python2
from pylms.server import Server

import Config


def provide():
    """

    :rtype: Server
    """
    config = Config.get_config()

    server = Server(hostname=config.get('lms', 'server'))  # type: Server
    server.connect()

    return server
