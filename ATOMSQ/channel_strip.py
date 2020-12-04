#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/channel_strip.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from .control import DisplayControl

class ChannelStripComponent(ChannelStripComponentBase):
    track_name_display = DisplayControl()

    def _update_track_name_data_source(self):
        self.track_name_display.message = self._track.name if liveobj_valid(self._track) else u' - '
