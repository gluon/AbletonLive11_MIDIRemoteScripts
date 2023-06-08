from __future__ import absolute_import, print_function, unicode_literals
from Oxygen_Pro.oxygen_pro import Oxygen_Pro
LIVE_MODE_BYTE = 0

class Oxygen_5th_Gen(Oxygen_Pro):
    live_mode_byte = LIVE_MODE_BYTE
    has_session_component = False

    def __init__(self, *a, **k):
        (super(Oxygen_5th_Gen, self).__init__)(*a, **k)
        self.set_pad_translations(tuple([tuple([col, row, 36 + (3 - row) * 4 + col, 0]) for row in range(3, -1, -1) for col in iter((range(4)))]))