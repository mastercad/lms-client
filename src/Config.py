#!/usr/bin/env python2
import os
from configparser import ConfigParser
from Exceptions import FileNotFoundException


def get_config():
    config_parser = ConfigParser()  # type: ConfigParser
    root_path = os.path.dirname(os.path.abspath(__file__))
    config_file_path = root_path+'/../config/config.txt'

    if not os.path.isfile(config_file_path):
        raise FileNotFoundException("Config File not found!")

    config_parser.read(r''+config_file_path)

    return config_parser  # type: ConfigParser
