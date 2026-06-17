# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_Key_25\SendToggleComponent.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 834 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import ButtonControl
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent

class SendToggleComponent(ControlSurfaceComponent):
    toggle_control = ButtonControl()

    def __init__(self, mixer, *args, **kwargs):
        (super(SendToggleComponent, self).__init__)(*args, **kwargs)
        self.mixer = mixer
        self.last_number_of_sends = self.mixer.num_sends
        self.set_toggle_button = self.toggle_control.set_control_element

    def inc_send_index(self):
        if self.mixer.num_sends:
            self.mixer.send_index = (self.mixer.send_index + 1) % self.mixer.num_sends

    @toggle_control.pressed
    def toggle_button_pressed(self, _button):
        self.inc_send_index()