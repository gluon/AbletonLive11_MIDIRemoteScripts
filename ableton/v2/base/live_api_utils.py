# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\live_api_utils.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1689 bytes
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


def move_current_song_time(song, delta, truncate_to_beat=True):
    new_time = max(0, song.current_song_time + delta)
    if truncate_to_beat:
        new_time = int(new_time)
    song.current_song_time = new_time
    if not song.is_playing:
        song.start_time = new_time