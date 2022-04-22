# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/drum_group.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1307 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import range
from past.utils import old_div
from ableton.v2.base import liveobj_valid
import ableton.v2.control_surface.components as DrumGroupComponentBase
from .note_pad import NotePadMixin
COMPLETE_QUADRANTS_RANGE = list(range(4, 116))
MAX_QUADRANT_INDEX = 7
NUM_PADS = 16
PADS_PER_ROW = 4

class DrumGroupComponent(NotePadMixin, DrumGroupComponentBase):

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        color = self._color_for_pad(pad) if liveobj_valid(pad) else 'DrumGroup.PadEmpty'
        if color == 'DrumGroup.PadFilled':
            button_row, _ = button.coordinate
            button_index = (self.matrix.height - button_row - 1) * PADS_PER_ROW
            pad_row_start_note = self._drum_group_device.visible_drum_pads[button_index].note
            pad_quadrant = MAX_QUADRANT_INDEX
            if pad_row_start_note in COMPLETE_QUADRANTS_RANGE:
                pad_quadrant = old_div(pad_row_start_note - 1, NUM_PADS)
            color = 'DrumGroup.PadQuadrant{}'.format(pad_quadrant)
        button.color = color