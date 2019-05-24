#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sqlite3 import Row
from MediaEntity import MediaEntity


def generate(row):
    """

    :param Row row:

    :return: MediaEntity
    """
    if isinstance(row, Row):
        # :rtype MediaEntity
        return MediaEntity(
            int(row['id']),
            str(row['rfid']),
            str(row['local_name']),
            str(row['lms_name']),
            str(row['special_information']),
            str(row['type']),
            str(row['picture_path'])
        )
    return MediaEntity()
