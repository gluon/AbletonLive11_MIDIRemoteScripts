# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\button_matrix.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4534 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, range
from ...base import const, in_range, product, slicer, to_slice
from ..compound_element import CompoundElement

class ButtonMatrixElement(CompoundElement):

    def __init__(self, rows=[], *a, **k):
        (super(ButtonMatrixElement, self).__init__)(*a, **k)
        self._buttons = []
        self._orig_buttons = []
        self._button_coordinates = {}
        self._max_row_width = 0
        for row in rows:
            self.add_row(row)

    @property
    @slicer(2)
    def submatrix(self, col_slice, row_slice):
        col_slice = to_slice(col_slice)
        row_slice = to_slice(row_slice)
        rows = [row[col_slice] for row in self._orig_buttons[row_slice]]
        return ButtonMatrixElement(rows=rows)

    def add_row(self, buttons):
        self._buttons.append([None] * len(buttons))
        self._orig_buttons.append(buttons)
        for index, button in enumerate(buttons):
            self._button_coordinates[button] = (
             index, len(self._buttons) - 1)
            self.register_control_element(button)

        if self._max_row_width < len(buttons):
            self._max_row_width = len(buttons)

    def width(self):
        return self._max_row_width

    def height(self):
        return len(self._buttons)

    def send_value(self, column, row, value, force=False):
        if len(self._buttons[row]) > column:
            button = self._buttons[row][column]
            if button:
                button.send_value(value, force=force)

    def set_light(self, column, row, value):
        if len(self._buttons[row]) > column:
            button = self._buttons[row][column]
            if button:
                button.set_light(value)

    def get_button(self, row, column):
        row = int(row)
        if len(self._buttons[row]) > column:
            return self._buttons[row][column]

    def set_channel(self, channel):
        for button in self:
            if button:
                button.set_channel(channel)

    def reset(self):
        for button in self:
            if button:
                button.reset()

    def __iter__(self):
        for j, i in product(range(self.height()), range(self.width())):
            button = self.get_button(j, i)
            yield button

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return list(map(self._do_get_item, range(*indices)))
        if index < 0:
            index += len(self)
        return self._do_get_item(index)

    def _do_get_item(self, index):
        row, col = divmod(index, self.width())
        return self.get_button(row, col)

    def __len__(self):
        return self.width() * self.height()

    def iterbuttons(self):
        for j, i in product(range(self.height()), range(self.width())):
            button = self.get_button(j, i)
            yield (button, (i, j))

    def on_nested_control_element_value(self, value, sender):
        x, y = self._button_coordinates[sender]
        is_momentary = getattr(sender, 'is_momentary', const(None))()
        self.notify_value(value, x, y, is_momentary)

    def on_nested_control_element_received(self, control):
        x, y = self._button_coordinates[control]
        self._buttons[y][x] = control

    def on_nested_control_element_lost(self, control):
        x, y = self._button_coordinates[control]
        self._buttons[y][x] = None