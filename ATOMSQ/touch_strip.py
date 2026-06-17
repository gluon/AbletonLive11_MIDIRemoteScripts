# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\touch_strip.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 2511 bytes
from __future__ import absolute_import, print_function, unicode_literals
import math
from functools import partial
from itertools import chain, repeat
from ableton.v3.base import listens
from ableton.v3.control_surface.elements import EncoderElement

class TouchStripElement(EncoderElement):

    def __init__(self, leds=None, *a, **k):
        self.map_value_to_led_states = partial(map_value_to_led_states, 127, 0, len(leds))
        (super().__init__)(0, *a, **k)
        self._leds = leds

    def connect_to(self, parameter):
        super().connect_to(parameter)
        self._update_feedback_leds(force=True)
        self._TouchStripElement__on_parameter_value.subject = self.mapped_parameter()

    def release_parameter(self):
        super().release_parameter()
        self._TouchStripElement__on_parameter_value.subject = None

    @listens('value')
    def __on_parameter_value(self):
        self._update_feedback_leds()

    def _update_feedback_leds(self, force=False):
        for led, state in zip(self._leds, self.map_value_to_led_states(self._parameter_to_map_to.value)):
            led.send_value(state, force)


def map_value_to_led_states(on, off, num_leds, value):
    mid_index = int(math.floor(num_leds / 2))
    active_length = mid_index + 1
    active_led_states = list(map(lambda i: on if i / active_length <= abs(value) else off
, map(float, range(active_length))))
    inactive_led_states = repeat(0, num_leds - active_length)
    if value < 0:
        return chain(reversed(active_led_states), inactive_led_states)
    return chain(inactive_led_states, active_led_states)