#!/usr/bin/env python2
# -*- coding: utf8 -*-
import curses
import RPi.GPIO as GPIO
import os

import Tools
import Database
import MediaMapper
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)

MFRC522 = SimpleMFRC522()


def read_start_change():
    os.system('clear')
    print ("Eingabe Wählen:")
    print ("    [1] => Datenbankeintrag anlegen oder updaten")
    print ("    [2] => Chip beschreiben")

    change = raw_input()

    try:
        return int(change)
    except:
        return 0


def new_database_entry():
    TYPES = ['PLAYLIST', 'MEDIA_FOLDER', 'MEDIA_FILE']

    (uid, value) = MFRC522.read()

    if value is not None:
        value = Tools.remove_invisible_chars(value)

    database = Database.Database()

    media_entity = MediaMapper.generate(database.find(uid))

    media_entity.set_rfid(uid)

    # local_path
    media_entity.set_local_name(str(prompt_with_default("Lokaler Pfad", media_entity.get_local_name())))

    # lms_path
    media_entity.set_lms_name(str(prompt_with_default("LMS Pfad", media_entity.get_lms_name())))

    # special_information
    media_entity.set_special_information(str(prompt_with_default("Spezielle Informationen", value)))

    # picture_path
    media_entity.set_picture_path(str(prompt_with_default("Bild Pfad", media_entity.get_picture_path())))

    # type
    media_entity.set_type(str(prompt_with_default("Type", media_entity.get_type())))

    print (database.save(media_entity))


def prompt_with_default(question, default_value=None):
    if default_value is None or "None" in default_value:
        default_value = ''
    return raw_input(str(question)+" ["+str(default_value)+"] : ") or default_value


def write_chip():
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.addstr("Eingabe von maximal 16 Zeichen: ")
    MFRC522.read()
    content = stdscr.getstr(1, 0, 16)
    curses.endwin()

    MFRC522.write(content)

    print ("Daten geschrieben:")
    print (MFRC522.read()[1])

    exit(0)


try:
    while True:
        change = read_start_change()
        print ("Change: "+str(change))
        if 1 == change:
            new_database_entry()
        elif 2 == change:
            write_chip()
finally:
    GPIO.cleanup()

