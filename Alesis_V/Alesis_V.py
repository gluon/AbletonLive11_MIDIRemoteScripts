# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Alesis_V/Alesis_V.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1465 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
import _Framework.ButtonMatrixElement as ButtonMatrixElement
import _Framework.ControlSurface as ControlSurface
import _Framework.DeviceComponent as DeviceComponent
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
import _Framework.Layer as Layer

class Alesis_V(ControlSurface):

    def __init__(self, *a, **k):
        (super(Alesis_V, self).__init__)(*a, **k)
        with self.component_guard():
            encoders = ButtonMatrixElement(rows=[
             [EncoderElement(MIDI_CC_TYPE, 0, (identifier + 20), (Live.MidiMap.MapMode.absolute), name=('Encoder_%d' % identifier)) for identifier in range(4)]])
            device = DeviceComponent(name='Device',
              is_enabled=False,
              layer=Layer(parameter_controls=encoders),
              device_selection_follows_track_selection=True)
            device.set_enabled(True)
            self.set_device_component(device)