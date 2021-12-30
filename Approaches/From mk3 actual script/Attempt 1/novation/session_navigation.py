#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/session_navigation.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase
from .util import skin_scroll_buttons

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        super(SessionNavigationComponent, self).__init__(*a, **k)
        skin_scroll_buttons(self._vertical_banking, u'Session.Navigation', u'Session.NavigationPressed')
        skin_scroll_buttons(self._horizontal_banking, u'Session.Navigation', u'Session.NavigationPressed')
        skin_scroll_buttons(self._vertical_paginator, u'Session.Navigation', u'Session.NavigationPressed')
        skin_scroll_buttons(self._horizontal_paginator, u'Session.Navigation', u'Session.NavigationPressed')
