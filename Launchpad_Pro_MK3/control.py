from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import InputControl, SendValueMixin

class SendReceiveValueControl(InputControl):

    class State(InputControl.State):

        def send_value(self, value):
            if self._control_element:
                self._control_element.send_value(value)