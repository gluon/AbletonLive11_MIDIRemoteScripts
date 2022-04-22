# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Generic/SelectChanStripComponent.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1046 bytes
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