# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_Essential/channel_strip.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 875 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as ChannelStripComponentBase
from .ringed_mapped_encoder_control import RingedMappedEncoderControl

class ChannelStripComponent(ChannelStripComponentBase):
    pan_control = RingedMappedEncoderControl()

    def set_pan_control(self, control):
        self.pan_control.set_control_element(control)
        self.update()

    def _connect_parameters(self):
        super(ChannelStripComponent, self)._connect_parameters()
        self.pan_control.mapped_parameter = self.track.mixer_device.panning

    def _disconnect_parameters(self):
        self.pan_control.mapped_parameter = None
        super(ChannelStripComponent, self)._disconnect_parameters()