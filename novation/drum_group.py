#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/drum_group.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import DrumGroupComponent as DrumGroupComponentBase
from .util import skin_scroll_buttons

class DrumGroupComponent(DrumGroupComponentBase):

    def __init__(self, *a, **k):
        super(DrumGroupComponent, self).__init__(*a, **k)
        skin_scroll_buttons(self._position_scroll, u'DrumGroup.Navigation', u'DrumGroup.NavigationPressed')
        skin_scroll_buttons(self._page_scroll, u'DrumGroup.Navigation', u'DrumGroup.NavigationPressed')

    def set_parent_track(self, track):
        pass
