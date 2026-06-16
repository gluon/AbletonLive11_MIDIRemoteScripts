# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_5th_Gen\oxygen_5th_gen.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 782 bytes
from __future__ import absolute_import, print_function, unicode_literals
from Oxygen_Pro.oxygen_pro import Oxygen_Pro
LIVE_MODE_BYTE = 0

class Oxygen_5th_Gen(Oxygen_Pro):
    live_mode_byte = LIVE_MODE_BYTE
    has_session_component = False

    def __init__(self, *a, **k):
        (super(Oxygen_5th_Gen, self).__init__)(*a, **k)
        self.set_pad_translations(tuple([tuple([col, row, 36 + (3 - row) * 4 + col, 0]) for row in range(3, -1, -1) for col in iter((range(4)))]))