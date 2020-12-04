#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_Essential/ringed_encoder.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import round
from past.utils import old_div
import Live
from ableton.v2.control_surface import CompoundElement, MIDI_CC_TYPE
from ableton.v2.control_surface.elements import EncoderElement
RING_VALUE_MIN = 17
RING_VALUE_MAX = 27

class RingedEncoderElement(CompoundElement, EncoderElement):

    def __init__(self, msg_type = MIDI_CC_TYPE, channel = 0, identifier = 0, map_mode = Live.MidiMap.MapMode.absolute, ring_element = None, *a, **k):
        assert ring_element is not None
        super(RingedEncoderElement, self).__init__(msg_type=msg_type, channel=channel, identifier=identifier, map_mode=map_mode, *a, **k)
        self._ring_element = self.register_control_element(ring_element)
        self.request_listen_nested_control_elements()
        self._ring_value_range = list(range(RING_VALUE_MIN, RING_VALUE_MAX + 1))

    def on_nested_control_element_value(self, value, control):
        pass

    def set_ring_value(self, parameter):
        ring_value = self._parameter_value_to_ring_value(parameter.value, parameter.min, parameter.max)
        self._ring_element.send_value(ring_value)

    def _parameter_value_to_ring_value(self, value, minv, maxv):
        vrange = self._ring_value_range
        index = int(round((value - minv) * old_div(len(vrange) - 1, float(maxv - minv))))
        return vrange[index]
