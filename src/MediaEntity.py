#!/usr/bin/env python2
# -*- coding: utf-8 -*-


class MediaEntity:

    """

    Attributes
    ----------
    type : str
    id : int
    rfid : str
    local_name : str
    lms_name : str
    special_information : str

    """

    type = ''
    id = ''
    rfid = ''
    local_name = ''
    lms_name = ''
    special_information = ''

    def __init__(self, id, rfid, local_name, lms_name, special_information, type):
        self.id = id,
        self.rfid = rfid,
        self.local_name = local_name
        self.lms_name = lms_name
        self.special_information = special_information
        self.type = type

        print (self.type, self.rfid, self.id, self.local_name, self.lms_name, self.special_information)

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
        return self

    def get_rfid(self):
        return self.rfid

    def set_rfid(self, rfid):
        self.rfid = rfid
        return self

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type
        return self

    def get_local_name(self):
        return self.local_name

    def set_local_name(self, local_name):
        self.local_name = local_name
        return self

    def get_lms_name(self):
        return self.lms_name

    def set_lms_name(self, lms_name):
        self.lms_name = lms_name
        return self

    def get_special_information(self):
        return self.special_information

    def set_special_information(self, special_information):
        self.special_information = special_information
        return self