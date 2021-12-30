#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/slider.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ..input_control_element import MIDI_NOTE_TYPE
from .encoder import EncoderElement

class SliderElement(EncoderElement):

    def __init__(self, msg_type, channel, identifier, *a, **k):
        assert msg_type is not MIDI_NOTE_TYPE
        super(SliderElement, self).__init__(msg_type, channel, identifier, map_mode=Live.MidiMap.MapMode.absolute, *a, **k)
