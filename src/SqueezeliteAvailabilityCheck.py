#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import psutil

import Config

config = Config.get_config()


def check():
    return config.get('player','path')+" -n "+config.get('lms', 'client_name') in (p.name() for p in psutil.process_iter())