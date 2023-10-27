# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey\consts.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 896 bytes
from __future__ import absolute_import, print_function, unicode_literals
SIZE_QUERY = (240, 126, 127, 6, 1, 247)
SIZE_RESPONSE = (240, 126, 127, 6, 2, 0, 32, 41, 0, 25, 0)
LIVE_MODE_ON = (144, 12, 127)
LIVE_MODE_OFF = (144, 12, 0)
PAD_TRANSLATIONS = ((0, 0, 48, 9), (1, 0, 49, 9), (2, 0, 50, 9), (3, 0, 51, 9), (0, 1, 44, 9),
                    (1, 1, 45, 9), (2, 1, 46, 9), (3, 1, 47, 9), (0, 2, 40, 9), (1, 2, 41, 9),
                    (2, 2, 42, 9), (3, 2, 43, 9), (0, 3, 36, 9), (1, 3, 37, 9), (2, 3, 38, 9),
                    (3, 3, 39, 9))
LED_FLASHING_ON = (176, 0, 40)
LED_FLASHING_OFF = (176, 0, 32)
LED_OFF = 4
RED_FULL = 15
RED_BLINK = 11
GREEN_FULL = 60
GREEN_BLINK = 56
AMBER_FULL = 63
AMBER_HALF = 29
AMBER_BLINK = 59