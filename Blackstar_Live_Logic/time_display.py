#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Blackstar_Live_Logic/time_display.py
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
import math
from ableton.v2.base import clamp, const, depends, listens, task
from ableton.v2.control_surface import NotifyingControlElement
from ableton.v2.control_surface.control import Control
MAX_DISPLAY_DIGITS = 3
NUM_DIGITS_TO_BYTE = {3: (7,),
 2: (6,),
 1: (4,)}

def truncate_to_n_least_significant_digits(num, n):
    u"""
    Return a list of the `n` least significant
    digits of `num`
    """
    if n <= 0:
        return []
    digits = []
    num_up_to_digit_n_minus_one = 0
    for i in range(n):
        num_up_to_digit_n = num % pow(10, i + 1)
        divisor = pow(10, i)
        digits.append(old_div(num_up_to_digit_n - num_up_to_digit_n_minus_one, divisor))

    return digits[::-1]


class TimeDisplayElement(NotifyingControlElement):

    def __init__(self, header, tail, *a, **k):
        super(TimeDisplayElement, self).__init__(*a, **k)
        self._header = header
        self._tail = tail

    def display_time(self, digits, num_digits, dots):
        self.send_midi(self._header + digits + num_digits + dots + self._tail)

    def reset(self):
        pass


class TimeDisplayControl(Control):

    class State(Control.State):

        def __init__(self, *a, **k):
            super(TimeDisplayControl.State, self).__init__(*a, **k)
            self._last_time = None

        def update(self):
            super(TimeDisplayControl.State, self).update()
            self._display_time(0, 0)

        def update_time(self, bars, beats):
            new_time = (bars, beats)
            if self._last_time and self._last_time != new_time:
                self._display_time(bars, beats)
            self._last_time = new_time

        def _display_time(self, bars, beats):
            if self._control_element:
                display_bars = bars > 0
                num_beat_digits = int(math.log10(beats)) + 1 if beats > 0 else 1
                num_bar_digits = MAX_DISPLAY_DIGITS - num_beat_digits
                digits = tuple(truncate_to_n_least_significant_digits(bars, num_bar_digits) + truncate_to_n_least_significant_digits(beats, num_beat_digits))
                if display_bars:
                    num_digits = 3 if digits[0] != 0 or num_beat_digits > 1 else 2
                else:
                    num_digits = num_beat_digits
                if not display_bars:
                    dots = (0,)
                elif num_beat_digits >= 2:
                    dots = (1,)
                else:
                    dots = (2,)
                self._control_element.display_time(digits, NUM_DIGITS_TO_BYTE[num_digits], dots)
