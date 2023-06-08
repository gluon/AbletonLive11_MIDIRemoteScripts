from __future__ import absolute_import, division, print_function, unicode_literals
from ableton.v3.control_surface.components import DrumGroupComponent as DrumGroupComponentBase
from .note_pad import NotePadMixin
COMPLETE_QUADRANTS_RANGE = range(4, 116)
MAX_QUADRANT_INDEX = 7
NUM_PADS = 16
PADS_PER_ROW = 4

class DrumGroupComponent(NotePadMixin, DrumGroupComponentBase):

    @staticmethod
    def _filled_color(pad):
        pad_quadrant = MAX_QUADRANT_INDEX
        if pad.note in COMPLETE_QUADRANTS_RANGE:
            pad_quadrant = (pad.note - PADS_PER_ROW) // NUM_PADS
        return 'DrumGroup.PadQuadrant{}'.format(pad_quadrant)