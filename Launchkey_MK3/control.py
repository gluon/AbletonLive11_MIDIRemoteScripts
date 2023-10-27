# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\control.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1176 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import Control
DEFAULT_MESSAGE = '-'

class DisplayControl(Control):

    class State(Control.State):

        def __init__(self, *a, **k):
            (super(DisplayControl.State, self).__init__)(*a, **k)
            self._message = DEFAULT_MESSAGE

        @property
        def message(self):
            return self._message

        @message.setter
        def message(self, message):
            self._message = DEFAULT_MESSAGE if message is None else message
            self._send_current_message()

        def set_control_element(self, control_element):
            super(DisplayControl.State, self).set_control_element(control_element)
            self._send_current_message()

        def update(self):
            super(DisplayControl.State, self).update()
            self._send_current_message()

        def _send_current_message(self):
            if self._control_element:
                self._control_element.display_message(self._message)