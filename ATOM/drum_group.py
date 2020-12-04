#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/drum_group.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import range
from past.utils import old_div
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import DrumGroupComponent as DrumGroupComponentBase
from .note_pad import NotePadMixin
COMPLETE_QUADRANTS_RANGE = list(range(4, 116))
MAX_QUADRANT_INDEX = 7
NUM_PADS = 16
PADS_PER_ROW = 4

class DrumGroupComponent(NotePadMixin, DrumGroupComponentBase):

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        color = self._color_for_pad(pad) if liveobj_valid(pad) else u'DrumGroup.PadEmpty'
        if color == u'DrumGroup.PadFilled':
            button_row, _ = button.coordinate
            button_index = (self.matrix.height - button_row - 1) * PADS_PER_ROW
            pad_row_start_note = self._drum_group_device.visible_drum_pads[button_index].note
            pad_quadrant = MAX_QUADRANT_INDEX
            if pad_row_start_note in COMPLETE_QUADRANTS_RANGE:
                pad_quadrant = old_div(pad_row_start_note - 1, NUM_PADS)
            color = u'DrumGroup.PadQuadrant{}'.format(pad_quadrant)
        button.color = color
