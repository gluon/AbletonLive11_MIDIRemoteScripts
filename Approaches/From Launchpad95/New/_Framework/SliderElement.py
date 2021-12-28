#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/SliderElement.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .EncoderElement import EncoderElement
from .InputControlElement import MIDI_NOTE_TYPE

class SliderElement(EncoderElement):
    u""" Class representing a slider on the controller """

    def __init__(self, msg_type, channel, identifier, *a, **k):
        assert msg_type is not MIDI_NOTE_TYPE
        super(SliderElement, self).__init__(msg_type, channel, identifier, map_mode=Live.MidiMap.MapMode.absolute, *a, **k)
