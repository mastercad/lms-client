#!/usr/bin/env python2
import os
from configparser import ConfigParser
from Exceptions import FileNotFoundException


def get_config():
    config_parser = ConfigParser()  # type: ConfigParser

    if not os.path.isfile('../config/config.txt'):
        raise FileNotFoundException("Config File not found!")

    config_file_path = r'../config/config.txt'
    config_parser.read(config_file_path)

    return config_parser  # type: ConfigParser
