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
            ensure_lms_player_is_running()
            return LMSPlayer.get_client()
        except ClientNotFoundException as exception:
            kill_not_needed_lms_player()
            return VLCPlayer.get_client()
    else:
        kill_not_needed_lms_player()
        return VLCPlayer.get_client()

def kill_not_needed_lms_player():
    global config
    for proc in psutil.process_iter():
        if config.get('player','name') == proc.name():
            try:
                pid = int(subprocess.check_output(["pidof", "-s", str(config.get('player', 'name'))]))
                os.system("sudo kill -9 "+str(pid))
            except CalledProcessError:
                return True

def ensure_lms_player_is_running():
    if False == SqueezeliteAvailabilityCheck.check():
        global config
        # @TODO hier gibts noch probleme. stellenweise wird squeezelite hier mit defunct gestartet, da muss noch ein fix her
        subprocess.Popen([config.get('player', 'name')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
