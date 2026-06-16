# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\channel_strip.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1136 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import next
from ableton.v2.base import liveobj_valid
from novation.channel_strip import ChannelStripComponent as ChannelStripComponentBase

class ChannelStripComponent(ChannelStripComponentBase):

    def update(self):
        super(ChannelStripComponent, self).update()
        self._update_static_color_control()

    def _update_static_color_control(self):
        valid_track = liveobj_valid(self._track)
        color_value = self._static_color_value if valid_track else 0
        if valid_track:
            if self._send_controls:
                send_index = next((i for i, x in enumerate(self._send_controls) if x), None)
                if send_index is not None:
                    if send_index >= len(self._track.mixer_device.sends):
                        color_value = 0
        self.static_color_control.value = color_value