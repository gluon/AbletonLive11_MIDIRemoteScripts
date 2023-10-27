# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\grid_resolution.py
# Compiled at: 2023-09-13 04:24:51
# Size of source mod 2**32: 4132 bytes
from __future__ import absolute_import, print_function, unicode_literals
from typing import NamedTuple
from Live.Clip import GridQuantization
from ...base import listenable_property
from .. import Component
from ..controls import FixedRadioButtonGroup

class GridResolution(NamedTuple):
    name: str
    step_length: float
    grid: int
    is_triplet: bool


GRID_RESOLUTIONS = (
 GridResolution('1/32t', 0.08333333333333333, GridQuantization.g_thirtysecond, True),
 GridResolution('1/32', 0.125, GridQuantization.g_thirtysecond, False),
 GridResolution('1/16t', 0.16666666666666666, GridQuantization.g_sixteenth, True),
 GridResolution('1/16', 0.25, GridQuantization.g_sixteenth, False),
 GridResolution('1/8t', 0.3333333333333333, GridQuantization.g_eighth, True),
 GridResolution('1/8', 0.5, GridQuantization.g_eighth, False),
 GridResolution('1/4t', 0.6666666666666666, GridQuantization.g_quarter, True),
 GridResolution('1/4', 1.0, GridQuantization.g_quarter, False))
DEFAULT_INDEX = 3

class GridResolutionComponent(Component):
    resolution_buttons = FixedRadioButtonGroup(checked_color='NoteEditor.Resolution.Selected',
      unchecked_color='NoteEditor.Resolution.NotSelected',
      control_count=8)

    def __init__(self, name='Grid_Resolution', resolutions=None, default_index=DEFAULT_INDEX, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._resolutions = resolutions or GRID_RESOLUTIONS
        self._index = default_index
        self._update_resolution_buttons()

    @property
    def step_length(self):
        return self._resolutions[self.index].step_length

    @property
    def clip_grid(self):
        resolution = self._resolutions[self.index]
        return (
         resolution.grid, resolution.is_triplet)

    @property
    def is_triplet(self):
        return self._resolutions[self.index].is_triplet

    @listenable_property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        if index != self._index:
            self._index = index
            self._update_resolution_buttons()
            self.notify_index()

    def set_to(self, name):
        name = name.lower()
        for index, grid_resolution in enumerate(self._resolutions):
            if grid_resolution.name == name:
                self.index = index
                return

        raise AssertionError('{} is not a valid GridResolution name'.format(name))

    @resolution_buttons.checked
    def resolution_buttons(self, button):
        self.index = button.index

    def _update_resolution_buttons(self):
        self.resolution_buttons.checked_index = self._index