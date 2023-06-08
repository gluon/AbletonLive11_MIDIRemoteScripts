from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.controls import Control
DEFAULT_MESSAGE = '-'

class DisplayControl(Control):

    class State(Control.State):

        def __init__(self, *a, **k):
            (super().__init__)(*a, **k)
            self._message = DEFAULT_MESSAGE

        @property
        def message(self):
            return self._message

        @message.setter
        def message(self, message):
            self._message = DEFAULT_MESSAGE if message is None else message
            self._send_current_message()

        def set_control_element(self, control_element):
            super().set_control_element(control_element)
            self._send_current_message()

        def update(self):
            super().update()
            self._send_current_message()

        def _send_current_message(self):
            if self._control_element:
                self._control_element.display_message(self._message)