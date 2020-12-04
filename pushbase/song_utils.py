#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/song_utils.py
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
    u"""
    Returns either the parent track of a live object or None if one is not found.
    """
    track = live_object
    while liveobj_valid(track) and not isinstance(track, Live.Track.Track):
        track = getattr(track, u'canonical_parent', None)

    return track
