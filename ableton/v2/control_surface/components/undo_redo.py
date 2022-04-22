# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/undo_redo.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 631 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .. import Component
from ..control import ButtonControl

class UndoRedoComponent(Component):
    undo_button = ButtonControl()
    redo_button = ButtonControl()

    @undo_button.pressed
    def undo_button(self, button):
        self._undo()

    @redo_button.pressed
    def redo_button(self, button):
        self._redo()

    def _redo(self):
        if self.song.can_redo:
            self.song.redo()

    def _undo(self):
        if self.song.can_undo:
            self.song.undo()