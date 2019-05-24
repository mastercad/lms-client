#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os

import sqlite3
from sqlite3 import Row

import Config
from MediaEntity import MediaEntity


class Database:
    def __init__(self):
        self.databaseConnection = DatabaseConnection()

    def save(self, media_entity):
        """

        :param MediaEntity media_entity:

        :return: int
        """

        if media_entity.get_id() is None:
            query = self.generate_insert_query(media_entity)
        else:
            query = self.generate_update_query(media_entity)

        print ("Query:")
        print (query)

        cursor = self.databaseConnection.execute(query)
        self.databaseConnection.connection.commit()

        return cursor.lastrowid

    def find(self, uid):
        """

        :param MediaEntity media_entity:

        :return:
        """

        """

        Returns
        -------
        MediaEntity

        """
        if uid is None:
            return None

        return self.databaseConnection.execute(
            "SELECT * FROM `mappings` WHERE `rfid`='"+str(uid)+"'"
        ).fetchone()  # type: Row

    def delete(self, media_entity):
        """

        :param MediaEntity media_entity:

        :return:
        """
        return self.databaseConnection.execute(
            "DELETE mappings FROM mappings WHERE `rfid`='"+str(media_entity.get_rfid())+"'"
        ).lastrowid

    def generate_insert_query(self, media_entity):
        return "INSERT INTO `mappings` (`rfid`, `special_information`, `local_name`, `lms_name`, `picture_path`, `type`) "+\
           "VALUES ('"+str(media_entity.get_rfid())+"', "+\
            "'"+str(media_entity.get_special_information())+"', "+\
            "'"+str(media_entity.get_local_name())+"', "+\
            "'"+str(media_entity.get_lms_name())+"', "+\
            "'"+str(media_entity.get_picture_path())+"', "+\
            "'"+str(media_entity.get_type())+"')"

    def generate_update_query(self, media_entity):
        return "UPDATE `mappings` SET `rfid`='"+str(media_entity.get_rfid())+"', "+\
            "`special_information`='"+str(media_entity.get_special_information())+"', "+\
            "`local_name`='"+str(media_entity.get_local_name())+"', "+\
            "`lms_name`='"+str(media_entity.get_lms_name())+"', "+\
            "`picture_path`='"+str(media_entity.get_picture_path())+"', "+\
            "`type`='"+str(media_entity.get_type())+"' "+\
            "WHERE `id`='"+str(media_entity.get_id())+"'"


class DatabaseConnection:

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

    def __del__(self):
        self.connection.close()

    @staticmethod
    def dict_factory(cursor, row):
        dict_result = {}
        for index, column in enumerate(cursor.description):
            dict_result[column[0]] = row[index]
        return dict_result

    def generate_database_path(self):
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
