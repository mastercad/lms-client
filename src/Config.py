#!/usr/bin/env python2
import ConfigParser


def get_config():
    config_parser = ConfigParser.ConfigParser()  # type: ConfigParser
    config_file_path = r'../config/config.txt'
    config_parser.read(config_file_path)

    return config_parser  # type: ConfigParser
