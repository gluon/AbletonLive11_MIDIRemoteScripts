# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\controls\button.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 3114 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import listenable_property
from ..display import Renderable
from elements.touch import TouchElement
from . import ButtonControlBase, control_color

class ButtonControl(ButtonControlBase):

    class State(ButtonControlBase.State, Renderable):
        is_held = listenable_property.managed(False)
        color = control_color('DefaultButton.On')
        on_color = control_color(None)

        def __init__(self, color='DefaultButton.On', on_color=None, *a, **k):
            (super().__init__)(*a, **k)
            self.color = color
            self.on_color = on_color
            self._is_on = False

        @listenable_property
        def is_pressed(self):
            return self._is_pressed

        @property
        def is_on(self):
            return self._is_on

        @is_on.setter
        def is_on(self, is_on):
            if is_on != self._is_on:
                self._is_on = is_on
                self._send_current_color()

        def _send_button_color(self):
            if self.on_color is not None and self.is_on:
                self._control_element.set_light(self.on_color)
            else:
                if self.color is not None:
                    self._control_element.set_light(self.color)

        def _has_delayed_event(self):
            return True

        def _call_listener(self, listener_name, *a):
            (super()._call_listener)(listener_name, *a)
            if listener_name == 'pressed':
                self.notify_is_pressed()
            else:
                if listener_name == 'pressed_delayed':
                    self.is_held = True
                else:
                    if listener_name == 'released':
                        self.is_held = False
                        self.notify_is_pressed()


class TouchControl(ButtonControl):

    class State(ButtonControl.State):

        def set_control_element(self, control_element):
            super().set_control_element(control_element)