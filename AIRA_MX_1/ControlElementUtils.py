# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/AIRA_MX_1/ControlElementUtils.py
# Compiled at: 2022-01-28 05:06:40
# Size of source mod 2**32: 1170 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Resource import PrioritizedResource
from _Framework.Dependency import depends
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_CC_TYPE
import _Framework.ComboElement as ComboElement
import _Framework.ButtonElement as ButtonElement
import _Framework.EncoderElement as EncoderElement

@depends(skin=None)
def make_button(name, identifier, channel=0, msg_type=MIDI_NOTE_TYPE, is_momentary=True, is_modifier=False, skin=None):
    return ButtonElement(is_momentary,
      msg_type,
      channel,
      identifier,
      name=name,
      resource_type=(PrioritizedResource if is_modifier else None),
      skin=skin)


def make_encoder(name, identifier, channel=0):
    return EncoderElement(MIDI_CC_TYPE,
      channel, identifier, (Live.MidiMap.MapMode.absolute), name=name)


def with_modifier(control, modifier):
    return ComboElement(control,
      modifiers=[modifier], name=(control.name + '_With_Modifier'))