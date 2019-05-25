#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ctypes


class Timespec(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]


CLOCK_MONTONIC_RAW = 4

librt = ctypes.CDLL('librt.so.1', use_errno=True)
clock_gettime = librt.clock_gettime
clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(Timespec)]

def monotonic_time():
    time_spec = Timespec()
    if 0 != clock_gettime(CLOCK_MONTONIC_RAW, ctypes.pointer(time_spec)):
        errno_ = ctypes.get_errno()
        raise OSError(errno_, os.strerror(errno_))
    return time_spec.tv_sec + time_spec.tv_nsec * 1e-9