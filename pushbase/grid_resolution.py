# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\grid_resolution.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2593 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from past.utils import old_div
import Live
from ableton.v2.base import listenable_property, product
from ableton.v2.control_surface.control import ControlManager, RadioButtonControl, control_list
GridQuantization = Live.Clip.GridQuantization
QUANTIZATION_FACTOR = 24
QUANTIZATION_LIST = [
 2.0,
 3.0,
 4.0,
 6.0,
 8.0,
 12.0,
 16.0,
 24.0]
CLIP_VIEW_GRID_LIST = tuple(product([
 GridQuantization.g_thirtysecond,
 GridQuantization.g_sixteenth,
 GridQuantization.g_eighth,
 GridQuantization.g_quarter], [
 True, False]))
CLIP_LENGTH_LIST = [
 2.0,
 4.0,
 4.0,
 8.0,
 8.0,
 16.0,
 16.0,
 32.0]
DEFAULT_INDEX = 3

class GridResolution(ControlManager):
    quantization_buttons = control_list(RadioButtonControl,
      checked_color='NoteEditor.QuantizationSelected',
      unchecked_color='NoteEditor.QuantizationUnselected',
      control_count=8)
    index = listenable_property.managed(DEFAULT_INDEX)

    def __init__(self, *a, **k):
        (super(GridResolution, self).__init__)(*a, **k)
        self.index = DEFAULT_INDEX
        self.quantization_buttons[self.index].is_checked = True

    @property
    def step_length(self):
        return old_div(QUANTIZATION_LIST[self.index], QUANTIZATION_FACTOR)

    @property
    def clip_grid(self):
        return CLIP_VIEW_GRID_LIST[self.index]

    @property
    def clip_length(self):
        return CLIP_LENGTH_LIST[self.index]

    @quantization_buttons.checked
    def quantization_buttons(self, button):
        self.index = button.index