<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/midi.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1553 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from numbers import Number
NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
CC_STATUS = 176
PB_STATUS = 224
SYSEX_START = 240
SYSEX_END = 247
SYSEX_GENERAL_INFO = 6
SYSEX_NON_REALTIME = 126
SYSEX_IDENTITY_REQUEST_ID = 1
SYSEX_IDENTITY_RESPONSE_ID = 2
SYSEX_IDENTITY_REQUEST_MESSAGE = (
 SYSEX_START,
 SYSEX_NON_REALTIME,
 127,
 SYSEX_GENERAL_INFO,
 SYSEX_IDENTITY_REQUEST_ID,
 SYSEX_END)

def is_valid_channel(channel):
    if not isinstance(channel, Number):
        return False
    return 0 <= channel < 16


def is_valid_value(value, max_val=128):
    if not isinstance(value, Number):
        return False
    return 0 <= value < max_val


def is_valid_identifier(identifier):
    if not isinstance(identifier, Number):
        return False
    return 0 <= identifier < 128


def is_sysex(midi_bytes):
    return len(midi_bytes) != 3


def is_valid_sysex(midi_bytes):
    return is_sysex(midi_bytes) and midi_bytes[0] == SYSEX_START and midi_bytes[(-1)] == SYSEX_END


def is_pitchbend(midi_bytes):
    return midi_bytes[0] & 240 == PB_STATUS


def extract_value(midi_bytes):
    if is_pitchbend(midi_bytes):
        return midi_bytes[1] + (midi_bytes[2] << 7)
    return midi_bytes[2]


def pretty_print_bytes(midi_bytes):
    hex_values = list(map(hex, midi_bytes))
    return ' '.join(hex_values)