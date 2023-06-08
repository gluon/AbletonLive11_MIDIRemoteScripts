from __future__ import absolute_import, print_function, unicode_literals
from .. import Component
from ..controls import ButtonControl

class UndoRedoComponent(Component):
    undo_button = ButtonControl(color='UndoRedo.Undo',
      pressed_color='UndoRedo.UndoPressed')
    redo_button = ButtonControl(color='UndoRedo.Redo',
      pressed_color='UndoRedo.RedoPressed')

    def __init__(self, name='Undo_Redo', *a, **k):
        (super().__init__)(a, name=name, **k)

    @undo_button.pressed
    def undo_button(self, _):
        if self.song.can_undo:
            self.song.undo()

    @redo_button.pressed
    def redo_button(self, _):
        if self.song.can_redo:
            self.song.redo()