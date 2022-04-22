# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/session_navigation.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 1196 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionNavigationComponentBase
from ...base import add_scroll_encoder, depends, skin_scroll_buttons

class SessionNavigationComponent(SessionNavigationComponentBase):

    @depends(session_ring=None)
    def __init__(self, name='Session_Navigation', session_ring=None, *a, **k):
        (super().__init__)(a, name=name, session_ring=session_ring, **k)
        add_scroll_encoder(self._horizontal_banking)
        add_scroll_encoder(self._vertical_banking)
        for c in (
         self._vertical_banking,
         self._horizontal_banking,
         self._vertical_paginator,
         self._horizontal_paginator):
            skin_scroll_buttons(c, 'Session.Navigation', 'Session.NavigationPressed')

    def set_horizontal_encoder(self, control):
        self._horizontal_banking.scroll_encoder.set_control_element(control)

    def set_vertical_encoder(self, control):
        self._vertical_banking.scroll_encoder.set_control_element(control)