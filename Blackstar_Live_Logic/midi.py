# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Blackstar_Live_Logic/midi.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 455 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.midi import SYSEX_END, SYSEX_START
SYSEX_HEADER = (
 SYSEX_START, 0, 32, 114)
NUMERIC_DISPLAY_COMMAND = (0, )
LIVE_INTEGRATION_MODE_ID = (
 SYSEX_START,
 0,
 0,
 116,
 1,
 0,
 77,
 67,
 1,
 0,
 7,
 1,
 0)