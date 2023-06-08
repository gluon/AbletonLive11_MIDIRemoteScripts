from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import ButtonElement

class RgbButtonElement(ButtonElement):

    def __init__(self, *a, **k):
        self._led_channel = k.pop('led_channel', 0)
        (super(RgbButtonElement, self).__init__)(*a, **k)

    def _do_send_value(self, value, channel=None):
        super(RgbButtonElement, self)._do_send_value(value, channel=(self._led_channel))