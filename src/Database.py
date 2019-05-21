#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os

import sqlite3

import Config


class Database:

    def __init__(self):
        database_path = self.generate_database_path()

        init_needed = False
        if not os.path.isfile(database_path):
            init_needed = True

        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row

        if init_needed:
            self.init_tables()

    def execute(self, sql, *args, **kwargs):
        """

        Parameter
        ---------

        :param sql:
        :param args:
        :param kwargs:

        :return:

        """
        return self.connection.cursor().execute(sql, args)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    @staticmethod
    def dict_factory(cursor, row):
        dict_result = {}
        for index, column in enumerate(cursor.description):
            dict_result[column[0]] = row[index]
        return dict_result

    @staticmethod
    def generate_database_path():
        config = Config.get_config()
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return root_dir + '/../data/' + config.get('database', 'host_name') + ".sqlite"

    def init_tables(self):
        create_table_mappings = 'CREATE TABLE `mappings` (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'rfid TEXT NOT NULL, ' \
            'special_information TEXT, ' \
            'local_name TEXT, ' \
            'lms_name TEXT, ' \
            'picture_path TEXT, ' \
            'type TEXT NOT NULL)'

        self.connection.execute(create_table_mappings)

    #       print(config_parser.get('database', 'host_name'))
    #       print(config_parser.sections())

    #        print(config_parser['database'])
    #        config_parser.add_section('new-entry')
    #        config_parser.set('new-entry', 'test')
    #        with open('../config/config.txt', 'w') as config_file_handler:
    #            config_parser.write(config_file_handler)
