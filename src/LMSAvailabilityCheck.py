#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import LMSServerProvider
from Exceptions import ServerNotFoundException
import Config

config = Config.get_config()


def check():
    try :
        LMSServerProvider.provide()
        return True
    except ServerNotFoundException:
        return False