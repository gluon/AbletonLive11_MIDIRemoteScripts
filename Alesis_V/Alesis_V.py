#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Alesis_V/Alesis_V.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.DeviceComponent import DeviceComponent

class Alesis_V(ControlSurface):

    def __init__(self, *a, **k):
        super(Alesis_V, self).__init__(*a, **k)
        with self.component_guard():
            encoders = ButtonMatrixElement(rows=[[ EncoderElement(MIDI_CC_TYPE, 0, identifier + 20, Live.MidiMap.MapMode.absolute, name=u'Encoder_%d' % identifier) for identifier in range(4) ]])
            device = DeviceComponent(name=u'Device', is_enabled=False, layer=Layer(parameter_controls=encoders), device_selection_follows_track_selection=True)
            device.set_enabled(True)
            self.set_device_component(device)
