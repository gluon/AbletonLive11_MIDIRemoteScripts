# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\MultiButtonElement.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2995 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from .ConfigurableButtonElement import ConfigurableButtonElement

class MultiButtonElement(ConfigurableButtonElement):

    def __init__(self, slave_channels, is_momentary, msg_type, channel, identifier, skin=None, default_states=None, name='', color_slaves=False, *a, **k):
        (super(MultiButtonElement, self).__init__)(
 is_momentary, msg_type, channel, identifier, skin, default_states, *a, **k)
        self.name = name
        self._slave_buttons = [SlaveButtonElement(self, is_momentary, msg_type, slave_channel, identifier, skin, (default_states if color_slaves else None), *a, name=name + '_ch_' + str(slave_channel + 1), **k) for slave_channel in slave_channels]

    def reset(self):
        super(MultiButtonElement, self).reset()
        for button in self._slave_buttons:
            button.reset()

    def set_on_off_values(self, on_value, off_value):
        super(MultiButtonElement, self).set_on_off_values(on_value, off_value)
        for button in self._slave_buttons:
            button.set_on_off_values(on_value, off_value)

    def set_light(self, value):
        super(MultiButtonElement, self).set_light(value)
        for button in self._slave_buttons:
            button.set_light(value)

    def send_value(self, value, **k):
        (super(MultiButtonElement, self).send_value)(value, **k)
        for button in self._slave_buttons:
            (button.send_value)(value, **k)


class SlaveButtonElement(ConfigurableButtonElement):

    def __init__(self, master, is_momentary, msg_type, channel, identifier, skin=None, default_states=None, *a, **k):
        (super(SlaveButtonElement, self).__init__)(
 is_momentary, msg_type, channel, identifier, skin, default_states, *a, **k)
        self._master_button = master

    def receive_value(self, value):
        super(SlaveButtonElement, self).receive_value(value)
        self._master_button.receive_value(value)