#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import subprocess
from subprocess import CalledProcessError

import psutil

import Config
import SqueezeliteAvailabilityCheck
import LMSPlayer as LMSPlayer
import VLCPlayer as VLCPlayer
from Exceptions import ClientNotFoundException

config = Config.get_config()


def produce(online):
    """

    :rtype: Player|VLCPlayer
    """
    if online is True:
        try:
            return LMSPlayer.get_client()
        except ClientNotFoundException:
            kill_not_needed_lms_player()
            return VLCPlayer.get_client()
    else:
        kill_not_needed_lms_player()
        return VLCPlayer.get_client()

def kill_not_needed_lms_player():
    global config
    lms_player = config.get('player','path').rsplit('/', 1)

    if 1 < len(lms_player):
        lms_player = lms_player[1]
    else:
        lms_player = lms_player[0]

    for proc in psutil.process_iter():
        if lms_player == proc.name():
            try:
                os.system("sudo killall -9 "+str(config.get('player', 'path')))
            except CalledProcessError as exception:
                return True
