# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/session_overview.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 576 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionOverviewComponentBase
from ableton.v3.base import depends

class SessionOverviewComponent(SessionOverviewComponentBase):

    @depends(session_ring=None)
    def __init__(self, name='Session_Overview', session_ring=None, *a, **k):
        (super().__init__)(a, name=name, session_ring=session_ring, enable_skinning=True, **k)