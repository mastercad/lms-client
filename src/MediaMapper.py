#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sqlite3 import Cursor, Row
from Database import Database
from MediaEntity import MediaEntity

database = Database()  # type: Database


def generate(key_id, key_value):
    """

    Returns
    -------
    MediaEntity

    """
    global database  # type: Database
    result = database.execute("SELECT * FROM mappings WHERE rfid='"+key_id+"'").fetchone()  # type: Cursor

    if isinstance(result, Row):
        # :rtype MediaEntity
        return MediaEntity(
            result['id'],
            result['rfid'],
            result['local_name'],
            result['lms_name'],
            result['special_information'],
            result['type']
        )
    return None
