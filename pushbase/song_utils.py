# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/song_utils.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 937 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import liveobj_valid

def is_return_track(song, track):
    return track in list(song.return_tracks)


def delete_track_or_return_track(song, track):
    tracks = list(song.tracks)
    if track in tracks:
        track_index = tracks.index(track)
        song.delete_track(track_index)
    else:
        track_index = list(song.return_tracks).index(track)
        song.delete_return_track(track_index)


def find_parent_track(live_object):
    track = live_object
    while liveobj_valid(track):
        if not isinstance(track, Live.Track.Track):
            track = getattr(track, 'canonical_parent', None)

    return track