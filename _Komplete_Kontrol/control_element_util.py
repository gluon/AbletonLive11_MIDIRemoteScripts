# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\control_element_util.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1580 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import MIDI_CC_TYPE, midi
from ableton.v2.control_surface.elements import ButtonElement, EncoderElement, SliderElement, SysexElement
from .physical_display_element import PhysicalDisplayElement
from .skin import skin
MIDI_CHANNEL = 15

def create_button(identifier, name):
    return ButtonElement(False,
      MIDI_CC_TYPE, MIDI_CHANNEL, identifier, name=name, skin=skin)


def create_encoder(identifier, name, is_s_mk2=False):
    encoder = EncoderElement(MIDI_CC_TYPE,
      MIDI_CHANNEL,
      identifier,
      (Live.MidiMap.MapMode.relative_smooth_two_compliment),
      name=name,
      encoder_sensitivity=1.0)
    if is_s_mk2:
        encoder.set_feedback_delay(-1)
        encoder.mapping_sensitivity = 0.1
    return encoder


def create_slider_element(identifier, name):
    return SliderElement(MIDI_CC_TYPE, MIDI_CHANNEL, identifier, name=name)


def create_display_line(header, line_index, name, width=0):
    line = PhysicalDisplayElement(width_in_chars=width, name=name)
    line.set_message_parts(header + (line_index,), (midi.SYSEX_END,))
    return line


def create_sysex_element(header, index, name):
    return SysexElement((lambda value: header + (value, index, midi.SYSEX_END)
),
      default_value=0,
      optimized=True,
      name=name)