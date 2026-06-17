# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\drum_group.py
# Compiled at: 2022-11-28 08:01:32
# Size of source mod 2**32: 749 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import DrumGroupComponent as DrumGroupComponentBase
from .util import skin_scroll_buttons

class DrumGroupComponent(DrumGroupComponentBase):

    def __init__(self, *a, **k):
        (super(DrumGroupComponent, self).__init__)(*a, **k)
        skin_scroll_buttons(self._position_scroll, 'DrumGroup.Navigation', 'DrumGroup.NavigationPressed')
        skin_scroll_buttons(self._page_scroll, 'DrumGroup.Navigation', 'DrumGroup.NavigationPressed')

    def set_parent_track(self, track):
        pass