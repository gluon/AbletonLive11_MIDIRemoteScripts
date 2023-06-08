from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import _Framework.ChannelStripComponent as ChannelStripComponent

class SelectChanStripComponent(ChannelStripComponent):

    def __init__(self):
        ChannelStripComponent.__init__(self)

    def _arm_value(self, value):
        if self.is_enabled():
            track_was_armed = False
            if self._track != None:
                if self._track.can_be_armed:
                    track_was_armed = self._track.arm
            ChannelStripComponent._arm_value(self, value)
            if not self._track != None and self._track.can_be_armed or self._track.arm:
                if not track_was_armed:
                    if self._track.view.select_instrument():
                        self.song().view.selected_track = self._track