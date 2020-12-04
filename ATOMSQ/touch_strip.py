#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/touch_strip.py
from __future__ import absolute_import, print_function, unicode_literals
import math
from functools import partial
from itertools import chain, repeat
from ableton.v2.base import depends, listens
from ableton.v2.control_surface.elements import TouchEncoderElement

class TouchStripElement(TouchEncoderElement):

    def __init__(self, leds = None, *a, **k):
        assert leds is not None
        self.map_value_to_led_states = partial(map_value_to_led_states, 127, 0, len(leds))
        assert self.map_value_to_led_states(0)
        super(TouchStripElement, self).__init__(*a, **k)
        self._leds = leds

    def connect_to(self, parameter):
        super(TouchStripElement, self).connect_to(parameter)
        self._update_feedback_leds(force=True)
        self.__on_parameter_value.subject = self.mapped_parameter()

    def release_parameter(self):
        super(TouchStripElement, self).release_parameter()
        self.__on_parameter_value.subject = None

    @listens(u'value')
    def __on_parameter_value(self):
        self._update_feedback_leds()

    def _update_feedback_leds(self, force = False):
        for led, state in zip(self._leds, self.map_value_to_led_states(self._parameter_to_map_to.value)):
            led.send_value(state, force)


def map_value_to_led_states(on, off, num_leds, value):
    u"""
    Given `value` in the range [-1, 1], return an iterator
    that provides `num_leds` led states.
    
    Assuming that we have a strip of evenly spaced leds indexed from
    left to right, an led has state `on` if its offset from the center is in
    the same direction as `value` and the normalized magnitude of the offset
    is less than or equal to the magnitude of `value`.
    
    Otherwise it is `off`
    """
    assert -1.0 <= value <= 1, u'The input value must be in the range [-1, 1]'
    assert num_leds % 2 != 0, u'There must be an odd number of leds'
    assert num_leds >= 3, u'There must be at least 3 leds'
    mid_index = int(math.floor(num_leds / 2))
    active_length = mid_index + 1
    active_led_states = list(map(lambda i: (on if i / active_length <= abs(value) else off), map(float, range(active_length))))
    inactive_led_states = repeat(0, num_leds - active_length)
    if value < 0:
        return chain(reversed(active_led_states), inactive_led_states)
    return chain(inactive_led_states, active_led_states)
