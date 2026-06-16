# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MIDI_Mix\ControlElementUtils.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1190 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.ButtonMatrixElement as ButtonMatrixElement
from _Framework.Dependency import depends
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
import _Framework.SliderElement as SliderElement

@depends(skin=None)
def make_button(identifier, name, skin=None):
    return ButtonElement(True, MIDI_NOTE_TYPE, 0, identifier, name=name, skin=skin)


def make_slider(identifier, name):
    return SliderElement(MIDI_CC_TYPE, 0, identifier, name=name)


def make_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE,
      0, identifier, map_mode=(Live.MidiMap.MapMode.absolute), name=name)


def make_button_row(identifier_sequence, element_factory, name):
    return ButtonMatrixElement(rows=[[element_factory(identifier, name + '_%d' % index)] for index, identifier in enumerate(identifier_sequence)])