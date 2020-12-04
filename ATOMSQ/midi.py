#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/midi.py
from __future__ import absolute_import, print_function, unicode_literals
NATIVE_MODE_ON_MESSAGE = (143, 0, 1)
NATIVE_MODE_OFF_MESSAGE = (143, 0, 0)
RED_MIDI_CHANNEL = 1
GREEN_MIDI_CHANNEL = 2
BLUE_MIDI_CHANNEL = 3
USER_MODE_START_CHANNEL = 10
SYSEX_START_BYTE = 240
SYSEX_END_BYTE = 247
SYSEX_HEADER = (SYSEX_START_BYTE,
 0,
 1,
 6,
 34)
DISPLAY_HEADER = SYSEX_HEADER + (18,)
LOWER_FIRMWARE_TOGGLE_HEADER = SYSEX_HEADER + (19,)
UPPER_FIRMWARE_TOGGLE_HEADER = SYSEX_HEADER + (20,)
