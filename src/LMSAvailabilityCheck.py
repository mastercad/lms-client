#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import socket
import telnetlib

import Config

config = Config.get_config()


def check():
    try :
        telnet = telnetlib.Telnet(config.get('lms', 'server'), 9000, float(config.get('system', 'timeout')))
        return True
    except socket.timeout as exception:
        return False