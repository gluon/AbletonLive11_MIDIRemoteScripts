<<<<<<< HEAD
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
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/undo_redo.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 610 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as UndoRedoComponentBase

class UndoRedoComponent(UndoRedoComponentBase):

    def __init__(self, name='Undo_Redo', *a, **k):
        (super().__init__)(a, name=name, **k)
        self.undo_button.color = 'UndoRedo.Undo'
        self.undo_button.pressed_color = 'UndoRedo.UndoPressed'
        self.redo_button.color = 'UndoRedo.Redo'
        self.redo_button.pressed_color = 'UndoRedo.RedoPressed'
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
