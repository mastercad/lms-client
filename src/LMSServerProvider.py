#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import telnetlib
import socket

from pylms.server import Server

import Config
from Exceptions import ServerNotFoundException

server = None


def provide():
    global server

    """

    :rtype: Server
    """
    config = Config.get_config()
    hostname = config.get('lms', 'server')
    server = Server(hostname)  # type: Server

    try:
        # schmutzige lösung um den timeout zu verkürzen auf dem pylms server
        server.telnet = telnetlib.Telnet(hostname, 9000, float(config.get('lms', 'timeout')))
        server.connect(False)
    except socket.error:
        raise ServerNotFoundException("LMS Server \"" + config.get('lms', 'server') + "\" nicht erreichbar!")

    return server
