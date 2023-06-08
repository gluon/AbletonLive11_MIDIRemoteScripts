from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ComboElement import ToggleElement
from _Framework.Control import ToggleButtonControl
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent

class BankToggleComponent(ControlSurfaceComponent):
    bank_toggle_button = ToggleButtonControl()

    def __init__(self, *a, **k):
        (super(BankToggleComponent, self).__init__)(*a, **k)
        self._toggle_elements = []

    @bank_toggle_button.toggled
    def bank_toggle_button(self, toggled, button):
        for e in self._toggle_elements:
            e.set_toggled(toggled)

    def create_toggle_element(self, *a, **k):
        element = ToggleElement(*a, **k)
        element.toggled = self.bank_toggle_button.is_toggled
        self._toggle_elements.append(element)
        return element