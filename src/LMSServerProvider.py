#!/usr/bin/env python2
from pylms.server import Server

import Config
import socket
from Exceptions import ServerNotFoundException


def provide():
    """

    :rtype: Server
    """
    config = Config.get_config()

    server = Server(hostname=config.get('lms', 'server'))  # type: Server

    try :
        server.connect()
    except socket.error:
        raise ServerNotFoundException("LMS Server \""+config.get('lms', 'server')+"\" nicht erreichbar!")

    return server
