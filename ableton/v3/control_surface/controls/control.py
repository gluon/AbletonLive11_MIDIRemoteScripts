from __future__ import absolute_import, print_function, unicode_literals
from . import InputControl, SendValueMixin

class SendValueInputControl(InputControl):

    class State(SendValueMixin, InputControl.State):
        pass