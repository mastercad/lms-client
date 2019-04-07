#!/usr/bin/env python2
import sqlite3

import Config


def provide():
    """

    :rtype: Connection
    """
    config = Config.get_config()
    connection = sqlite3.connect(config.get('database', 'host_name'))

    return connection


#       print(config_parser.get('database', 'host_name'))
#       print(config_parser.sections())

#        print(config_parser['database'])
#        config_parser.add_section('new-entry')
#        config_parser.set('new-entry', 'test')
#        with open('../config/config.txt', 'w') as config_file_handler:
#            config_parser.write(config_file_handler)
