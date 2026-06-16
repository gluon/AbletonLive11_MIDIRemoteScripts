# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\midi.py
# Compiled at: 2022-12-08 12:23:09
# Size of source mod 2**32: 2668 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.midi import SYSEX_END, SYSEX_START
PAD_TRANSLATION_CHANNEL = 14
SYSEX_HEADER = (
 SYSEX_START, 0, 32, 107, 127, 66)
LED_HEADER = SYSEX_HEADER + (2, 2, 22)
DISPLAY_HEADER = SYSEX_HEADER + (4, 2, 96)
ENCODER_VALUE_HEADER = SYSEX_HEADER + (33, 16, 0)
REQUEST_DATA_BYTE = 1
PROGRAM_LOAD_BYTE = 98
make_connection_message = lambda parameter_byte: SYSEX_HEADER + (
 2,
 0,
 64,
 106,
 parameter_byte,
 SYSEX_END)
CONNECTION_MESSAGE = make_connection_message(33)
DISCONNECTION_MESSAGE = make_connection_message(32)
REQUEST_PROGRAM_MESSAGE = SYSEX_HEADER + (REQUEST_DATA_BYTE, 0, 64, 1, SYSEX_END)
ARTURIA_PROGRAM_CLEAR_SCREEN_MESSAGE = SYSEX_HEADER + (
 4,
 1,
 96,
 10,
 10,
 95,
 81,
 0,
 SYSEX_END)
ARTURIA_PROGRAM_GENERIC_PARAMETER_FEEDBACK_MESSAGE = SYSEX_HEADER + (
 2,
 2,
 64,
 106,
 16,
 SYSEX_END)
COMMAND_ID_TO_DAW_PROGRAM_ID = {REQUEST_DATA_BYTE: 1, PROGRAM_LOAD_BYTE: 2}
ENCODER_ID_TO_SYSEX_ID = {
  86: 7, 87: 8, 89: 9, 90: 10, 110: 11, 111: 12, 116: 13, 117: 14}
PAD_ID_TO_SYSEX_ID = {
  36: 52,
  37: 53,
  38: 54,
  39: 55,
  40: 56,
  41: 57,
  42: 58,
  43: 59,
  44: 68,
  45: 69,
  46: 70,
  47: 71,
  48: 72,
  49: 73,
  50: 74,
  51: 75,
  105: 87,
  106: 88,
  107: 89,
  108: 90,
  109: 91}