# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\midi.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 481 bytes
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