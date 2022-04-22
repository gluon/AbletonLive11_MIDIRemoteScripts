# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/session_ring.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 753 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionRingComponentBase
from ...base import depends

class SessionRingComponent(SessionRingComponentBase):

    @depends(song=None)
    def __init__(self, name='Session_Ring', include_returns=False, tracks_to_use=None, song=None, *a, **k):
        if tracks_to_use is None:
            if include_returns:
                tracks_to_use = lambda: tuple(song.visible_tracks) + tuple(song.return_tracks)
        (super().__init__)(a, name=name, song=song, tracks_to_use=tracks_to_use, **k)