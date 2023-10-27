# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\control_element_utils.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 1532 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, InputControlElement
from ableton.v2.control_surface.elements import ButtonElement, ColorSysexElement
from . import sysex
from .ringed_encoder import RingedEncoderElement

@depends(skin=None)
def create_button(identifier, name, channel=0, skin=None):
    return ButtonElement(True, MIDI_NOTE_TYPE, channel, identifier, name=name, skin=skin)


@depends(skin=None)
def create_pad_led(identifier, name, skin=None):

    def make_send_value_generator(id):

        def send_message_generator(v):
            return sysex.LIGHT_PAD_LED_MSG_PREFIX + (id,) + v + (sysex.END_BYTE,)

        return send_message_generator

    return ColorSysexElement(skin=skin,
      send_message_generator=(make_send_value_generator(identifier)),
      default_value=(0, 0, 0),
      optimized=True,
      name=name)


def create_ringed_encoder(identifier, ring_element_identifier, name):
    return RingedEncoderElement(MIDI_CC_TYPE,
      0,
      identifier,
      map_mode=(Live.MidiMap.MapMode.relative_signed_bit),
      ring_element=InputControlElement(MIDI_CC_TYPE,
      0, ring_element_identifier, name=(name + '_Ring_Element')),
      name=name)