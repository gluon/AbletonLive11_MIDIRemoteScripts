# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/base/live_api_util.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1127 bytes
from __future__ import absolute_import, print_function, unicode_literals
from . import liveobj_valid

def is_song_recording(song):
    return song.session_record or song.record_mode


def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


def toggle_or_cycle_parameter_value(parameter):
    if liveobj_valid(parameter):
        if parameter.is_quantized:
            if parameter.value + 1 > parameter.max:
                parameter.value = parameter.min
            else:
                parameter.value = parameter.value + 1
        else:
            parameter.value = parameter.max if parameter.value == parameter.min else parameter.min