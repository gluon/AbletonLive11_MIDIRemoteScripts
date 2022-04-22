# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_MK2/consts.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 626 bytes
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