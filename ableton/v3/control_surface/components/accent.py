from __future__ import absolute_import, print_function, unicode_literals
from ...base import depends, listenable_property
from .. import Component
from ..controls import ToggleButtonControl

class AccentComponent(Component):
    accent_button = ToggleButtonControl(color='Accent.Off', on_color='Accent.On')

    @depends(full_velocity=None)
    def __init__(self, name='Accent', full_velocity=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._full_velocity = full_velocity
        self.accent_button.connect_property(self, 'activated')

    @listenable_property
    def activated(self):
        return self._full_velocity.enabled

    @activated.setter
    def activated(self, state):
        if state != self._full_velocity.enabled:
            self._full_velocity.enabled = state
            self.notify_activated()

    @accent_button.released_delayed
    def accent_button(self, _):
        self.activated = False