#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/undo_redo.py
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
