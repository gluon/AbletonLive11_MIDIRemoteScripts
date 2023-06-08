<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Komplete_Kontrol/control_element_util.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 1521 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
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
<<<<<<< HEAD
    return SysexElement((lambda value: header + (value, index, midi.SYSEX_END)
),
=======
    return SysexElement((lambda value: header + (value, index, midi.SYSEX_END)),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
      default_value=0,
      optimized=True,
      name=name)