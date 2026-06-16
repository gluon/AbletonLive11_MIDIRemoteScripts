# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\session_ring_selection_linking.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 406 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import SessionRingSelectionLinking as SessionRingSelectionLinkingBase

class SessionRingSelectionLinking(SessionRingSelectionLinkingBase):

    def _current_track(self):
        return self._session_ring.selected_item