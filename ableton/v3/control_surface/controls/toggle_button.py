<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from . import ButtonControl, Connectable, control_event

class ToggleButtonControl(ButtonControl):
    toggled = control_event('toggled')

    class State(ButtonControl.State, Connectable):
        requires_listenable_connected_property = True

        def connect_property(self, *a):
            (super().connect_property)(*a)
            self.is_on = self.connected_property_value

        def on_connected_property_changed(self, value):
            self.is_on = value

        def _on_pressed(self):
            super()._on_pressed()
            self.is_on = not self._is_on
            self._call_listener('toggled', self.is_on)
            self.connected_property_value = self.is_on
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/controls/toggle_button.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 470 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.control as ToggleButtonControlBase

class ToggleButtonControl(ToggleButtonControlBase):

    class State(ToggleButtonControlBase.State):

        def on_connected_property_changed(self, value=None):
            self.is_toggled = value or self.connected_property_value
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
