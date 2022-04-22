# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/base/live_api_utils.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 1110 bytes
from __future__ import absolute_import, print_function, unicode_literals

def liveobj_changed(obj, other):
    return obj != other or type(obj) != type(other)


def liveobj_valid(obj):
    return obj != None


def is_parameter_bipolar(param):
    return param.min == -1 * param.max


def duplicate_clip_loop(clip):
    if not liveobj_valid(clip) or clip.is_midi_clip:
        try:
            clip.duplicate_loop()
        except RuntimeError:
            pass