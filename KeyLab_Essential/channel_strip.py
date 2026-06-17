# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\channel_strip.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 904 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
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