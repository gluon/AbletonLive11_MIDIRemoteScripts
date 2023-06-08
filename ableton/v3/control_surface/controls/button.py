from __future__ import absolute_import, print_function, unicode_literals
from . import ButtonControlBase, control_color

class ButtonControl(ButtonControlBase):

    class State(ButtonControlBase.State):
        color = control_color('DefaultButton.On')
        on_color = control_color(None)

        def __init__(self, color='DefaultButton.On', on_color=None, *a, **k):
            (super().__init__)(*a, **k)
            self.color = color
            self.on_color = on_color
            self._is_on = False

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