<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from . import ButtonControlBase, control_color
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/controls/button.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1109 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import ButtonControlBase, control_color
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

class ButtonControl(ButtonControlBase):

    class State(ButtonControlBase.State):
        color = control_color('DefaultButton.On')
        on_color = control_color(None)

<<<<<<< HEAD
        def __init__(self, color='DefaultButton.On', on_color=None, *a, **k):
            (super().__init__)(*a, **k)
            self.color = color
            self.on_color = on_color
=======
        def __init__(self, color=None, on_color=None, *a, **k):
            (super().__init__)(*a, **k)
            if color is not None:
                self.color = color
            if on_color is not None:
                self.on_color = on_color
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
            self._is_on = False

        @property
        def is_on(self):
            return self._is_on

        @is_on.setter
        def is_on(self, is_on):
<<<<<<< HEAD
            if is_on != self._is_on:
                self._is_on = is_on
                self._send_current_color()
=======
            self._is_on = is_on
            self._send_current_color()
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

        def _send_button_color(self):
            if self.on_color is not None and self.is_on:
                self._control_element.set_light(self.on_color)
            else:
<<<<<<< HEAD
                if self.color is not None:
                    self._control_element.set_light(self.color)
=======
                self._control_element.set_light(self.color)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
