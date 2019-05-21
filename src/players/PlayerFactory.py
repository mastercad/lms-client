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
    print ("Is Online in PlayerFactory:"+str(online))
    """

    :rtype: Player|VLCPlayer
    """
    if online is True:
        try:
            ensure_lms_player_is_running()
            return LMSPlayer.get_client()
        except ClientNotFoundException:
            kill_not_needed_lms_player()
            return VLCPlayer.get_client()
    else:
        kill_not_needed_lms_player()
        return VLCPlayer.get_client()

def kill_not_needed_lms_player():
    global config
    for proc in psutil.process_iter():
        if config.get('player','name') == proc.name():
            # auskommentiert, funktioniert nur bei prozessen, die vom user selbst gestartet wurden
#            proc.kill()
            try:
                pid = int(subprocess.check_output(["pidof", "-s", str(config.get('player', 'name'))]))
                os.system("sudo kill -9 "+str(pid))
            # hier wurde kein process gefunden von subprocess.check_output => alles i.O.
            except CalledProcessError:
                return True

def ensure_lms_player_is_running():
    if False == SqueezeliteAvailabilityCheck.check():
        global config
        # python 3.5
        #subprocess.run([config.get('player', 'name')])
        # python 2.7
#        subprocess.call([config.get('player', 'name')])
        subprocess.Popen([config.get('player', 'name')], stdout=subprocess.PIPE)
