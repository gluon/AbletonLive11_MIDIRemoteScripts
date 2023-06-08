from __future__ import absolute_import, print_function, unicode_literals
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
import _Framework.SliderElement as SliderElement

def make_encoder(identifier, channel, name):
    return EncoderElement(MIDI_CC_TYPE,
      channel, identifier, (Live.MidiMap.MapMode.absolute), name=name)


def make_slider(identifier, channel, name):
    return SliderElement(MIDI_CC_TYPE, channel, identifier, name=name)


def make_button(identifier, channel, name):
    return ButtonElement(True, MIDI_CC_TYPE, channel, identifier, name=name)