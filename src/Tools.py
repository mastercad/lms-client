#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from string import atoi, printable


def convert_string_to_ascii_array(current_string):
    return [ord(current_char) for current_char in list(current_string)]


def convert_ascii_array_to_string(ascii_array):
    return ''.join(chr(int(current_char)) for current_char in ascii_array)


# ich glaub, das kann weg
def string_to_hex(current_string):
    list = []
    for char in current_string:
        hex_var = hex(ord(char)).replace('0x', '')
        if 1 == len(hex_var):
            hex_var = '0'+hex_var
        list.append(hex_var)

    return reduce(lambda x,y:x+y, list)


def hex_to_string(hex_var):
    return hex_var and chr(atoi(hex_var[:2], base=16)) + hex_to_string(hex_var[2:]) or ''


def convert_ascii_string_to_string(current_string, separator):
    return convert_ascii_array_to_string(current_string.split(separator))


def convert_char_to_ascii(current_char):
    return int(format(ord(current_char)))


def format_uid(uid):
    uid_string = ""
    for index in range(0, len(uid)):
        uid_string += "%x" % uid[index]

    return uid_string.upper()


def remove_invisible_chars(current_string):
    return ''.join(char for char in current_string if char in printable).strip()


def convert_string_to_int_array(current_string):
    return [int(number) for number in current_string.split(',')]


def fill_list_with_char(current_list, max_length, character):
    for x in range(len(current_list), max_length):
        current_list.append(character)
    return current_list
