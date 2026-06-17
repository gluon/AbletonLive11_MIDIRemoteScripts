# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\FANTOM\sysex.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 1283 bytes
from __future__ import absolute_import, print_function, unicode_literals
SYSEX_START_BYTE = 240
SYSEX_END_BYTE = 247
HEADER = (
 SYSEX_START_BYTE, 65, 16, 0, 0, 0, 91)
INITIATE_CONNECTION = HEADER + (18, 14, 80, 0, 1, SYSEX_END_BYTE)
TERMINATE_CONNECTION = HEADER + (18, 14, 80, 0, 0, SYSEX_END_BYTE)
TRACK_INFO_DISPLAY_HEADER = HEADER + (18, 14, 80, 1, 0)
SCENE_NAME_DISPLAY_HEADER = HEADER + (18, 14, 80, 2, 0)
BEAT_TIME_DISPLAY_HEADER = HEADER + (18, 14, 80, 3, 0)
TEMPO_DISPLAY_HEADER = HEADER + (18, 14, 80, 3, 1)
REFRESH_REQUEST = HEADER + (17, 14)
NAME_LENGTH = 8
NAME_TERMINATOR = 0