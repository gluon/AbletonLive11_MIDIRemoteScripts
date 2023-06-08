from __future__ import absolute_import, print_function, unicode_literals
import Live
MapMode = Live.MidiMap.MapMode
import _Framework.ButtonElement as ButtonElement
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
import _Framework.SliderElement as SliderElement
import _APC.RingedEncoderElement as RingedEncoderElement

def make_button(channel, identifier, *a, **k):
    return ButtonElement(True, MIDI_NOTE_TYPE, channel, identifier, *a, **k)


def make_pedal_button(identifier, *a, **k):
    return ButtonElement(True, MIDI_CC_TYPE, 0, identifier, *a, **k)


def make_slider(channel, identifier, *a, **k):
    return SliderElement(MIDI_CC_TYPE, channel, identifier, *a, **k)


def make_knob(channel, identifier, *a, **k):
    return SliderElement(MIDI_CC_TYPE, channel, identifier, *a, **k)


def make_ring_encoder(encoder_identifer, button_identifier, name='', *a, **k):
    button_name = '%s_Ring_Mode_Button' % name
    button = ButtonElement(False, MIDI_CC_TYPE, 0, button_identifier, name=button_name)
    encoder = RingedEncoderElement(
 MIDI_CC_TYPE, 0, encoder_identifer, (MapMode.absolute), *a, name=name, **k)
    encoder.set_ring_mode_button(button)
    return encoder


def make_encoder(channel, identifier, *a, **k):
    return EncoderElement(
 MIDI_CC_TYPE, channel, identifier, MapMode.relative_two_compliment, *a, **k)