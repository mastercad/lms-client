#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import psutil

import Config

config = Config.get_config()


def check():
    return config.get('player','name') in (p.name() for p in psutil.process_iter())