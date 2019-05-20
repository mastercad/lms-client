#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pylms.server import Server

import Config
import socket
from Exceptions import ServerNotFoundException

server = None

def provide():
    global server

    """

    :rtype: Server
    """
    config = Config.get_config()

    if server is None:
        server = Server(hostname=config.get('lms', 'server'))  # type: Server
        try:
            server.connect()
        except socket.error:
            raise ServerNotFoundException("LMS Server \"" + config.get('lms', 'server') + "\" nicht erreichbar!")

    return server
