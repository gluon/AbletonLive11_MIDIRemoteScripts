# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\toggle_button.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3057 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .button import ButtonControlBase
from .control import Connectable, control_color, control_event

class ToggleButtonControl(ButtonControlBase):
    toggled = control_event('toggled')

    class State(ButtonControlBase.State, Connectable):
        untoggled_color = control_color('DefaultButton.Off')
        toggled_color = control_color('DefaultButton.On')
        requires_listenable_connected_property = True

        def __init__(self, untoggled_color=None, toggled_color=None, *a, **k):
            (super(ToggleButtonControl.State, self).__init__)(*a, **k)
            if untoggled_color is not None:
                self.untoggled_color = untoggled_color
            if toggled_color is not None:
                self.toggled_color = toggled_color
            self._is_toggled = False

        @property
        def is_toggled(self):
            return self._is_toggled

        @is_toggled.setter
        def is_toggled(self, toggled):
            if self._is_toggled != toggled:
                self._is_toggled = toggled
                self._send_current_color()

        def connect_property(self, *a):
            (super(ToggleButtonControl.State, self).connect_property)(*a)
            self.is_toggled = self.connected_property_value

        def on_connected_property_changed(self, value):
            self.is_toggled = value

        def _send_button_color(self):
            self._control_element.set_light(self.toggled_color if self._is_toggled else self.untoggled_color)

        def _on_pressed(self):
            super(ToggleButtonControl.State, self)._on_pressed()
            self._is_toggled = not self._is_toggled
            self._call_listener('toggled', self._is_toggled)
            self.connected_property_value = self.is_toggled