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