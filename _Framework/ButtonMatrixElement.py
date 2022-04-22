# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ButtonMatrixElement.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4231 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, range
from .CompoundElement import CompoundElement
from .Util import const, in_range, product, slicer, to_slice

class ButtonMatrixElement(CompoundElement):

    def __init__(self, rows=[], *a, **k):
        (super(ButtonMatrixElement, self).__init__)(*a, **k)
        self._buttons = []
        self._orig_buttons = []
        self._button_coordinates = {}
        self._max_row_width = 0
        list(map(self.add_row, rows))

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

    def get_button(self, column, row):
        if len(self._buttons[row]) > column:
            return self._buttons[row][column]

    def reset(self):
        for button in self:
            if button:
                button.reset()

    def __iter__(self):
        for j, i in product(range(self.height()), range(self.width())):
            button = self.get_button(i, j)
            (yield button)

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return list(map(self._do_get_item, list(range(*indices))))
        if index < 0:
            index += len(self)
        return self._do_get_item(index)

    def _do_get_item(self, index):
        row, col = divmod(index, self.width())
        return self.get_button(col, row)

    def __len__(self):
        return self.width() * self.height()

    def iterbuttons(self):
        for j, i in product(range(self.height()), range(self.width())):
            button = self.get_button(i, j)
            (yield (button, (i, j)))

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