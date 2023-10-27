# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\consts.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 649 bytes
from __future__ import absolute_import, print_function, unicode_literals
PRODUCT_ID_BYTE_PREFIX = (0, 32, 41)
LAUNCHKEY_25_ID_BYTE = 123
LAUNCHKEY_49_ID_BYTE = 124
LAUNCHKEY_61_ID_BYTE = 125
PRODUCT_ID_BYTES = (
 LAUNCHKEY_25_ID_BYTE, LAUNCHKEY_49_ID_BYTE, LAUNCHKEY_61_ID_BYTE)
IDENTITY_REQUEST = (240, 126, 127, 6, 1, 247)
IN_CONTROL_QUERY = (159, 11, 0)
DRUM_IN_CONTROL_ON_MESSAGE = (159, 15, 127)
DRUM_IN_CONTROL_OFF_MESSAGE = (159, 15, 0)
STANDARD_CHANNEL = 15
PULSE_LED_CHANNEL = 2
BLINK_LED_CHANNEL = 1
MAX_SENDS = 6