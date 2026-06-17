# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\decoration.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2663 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import find_if, liveobj_changed, liveobj_valid, old_hasattr
from ableton.v2.control_surface import DecoratorFactory

def find_decorated_object(proxied_object, decorator_factory):
    decorated_obj = None
    if liveobj_valid(proxied_object):
        decorated_obj = find_if(lambda obj: not liveobj_changed(obj.proxied_object, proxied_object)
, iter(decorator_factory.decorated_objects.values()))
    return decorated_obj


class TrackDecoratorFactory(DecoratorFactory):

    def decorate_all_mixer_tracks(self, mixer_tracks):
        tracks = []
        for track in mixer_tracks:
            decorated_track = self._get_decorated_track(track)
            tracks.append(decorated_track)

        self.sync_decorated_objects(tracks)
        return tracks

    def _get_nesting_level(self, track):
        if track.is_grouped:
            return self._get_nesting_level(track.group_track) + 1
        return 0

    def _get_chain_nesting_level(self, chain):
        parent_chain_or_track = chain.canonical_parent.canonical_parent
        if old_hasattr(parent_chain_or_track, 'group_track'):
            return self._get_nesting_level(parent_chain_or_track) + 1
        if old_hasattr(parent_chain_or_track, 'canonical_parent'):
            if old_hasattr(parent_chain_or_track.canonical_parent, 'canonical_parent'):
                return self._get_chain_nesting_level(parent_chain_or_track) + 1
        return 0

    def _get_track_for_chain(self, mixable):
        parent = mixable.canonical_parent
        while not isinstance(parent, Live.Track.Track):
            if not isinstance(parent, Live.Chain.Chain):
                parent = parent.canonical_parent

        return parent

    def _get_decorated_track(self, track):
        decorated = self.decorate(track)
        if getattr(track, 'group_track', None):
            decorated.parent_track = self.decorate(track.group_track)
            decorated.nesting_level = self._get_nesting_level(track)
        else:
            if isinstance(track, Live.Chain.Chain):
                parent_track = self._get_track_for_chain(track)
                decorated.parent_track = self.decorate(parent_track)
                decorated.nesting_level = self._get_chain_nesting_level(track)
            else:
                decorated.parent_track = None
                decorated.nesting_level = 0
        return decorated