# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\matrix_maps.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1546 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
PAD_TRANSLATIONS = ((0, 0, 60, 13), (1, 0, 61, 13), (2, 0, 62, 13), (3, 0, 63, 13),
                    (0, 1, 52, 13), (1, 1, 53, 13), (2, 1, 54, 13), (3, 1, 55, 13),
                    (0, 2, 44, 13), (1, 2, 45, 13), (2, 2, 46, 13), (3, 2, 47, 13),
                    (0, 3, 36, 13), (1, 3, 37, 13), (2, 3, 38, 13), (3, 3, 39, 13))
NON_FEEDBACK_CHANNEL = 0
FEEDBACK_CHANNELS = list(range(9, 16))
PAD_FEEDBACK_CHANNEL = FEEDBACK_CHANNELS[-1]
PLAYHEAD_FEEDBACK_CHANNELS = list(range(1, 9))