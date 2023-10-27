# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\footswitch_row_control.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 4184 bytes
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
import weakref, Live
from ableton.v2.base import const, depends, listens, mixin
from ableton.v2.control_surface.control import ButtonControl, ControlList, control_list
PULSE_COLORS = set(['Beat_Pulse', 'Subdivision_Pulse'])
PULSE_LENGTH_FRACTION = 0.2

def footswitch_row_control(*a, **k):
    c = mixin(FootswitchRowControl, FootswitchControl)
    return c(FootswitchControl, *a, **k)


class FootswitchControl(ButtonControl):
    DOUBLE_CLICK_DELAY = 0.8

    def __init__(self, *a, **k):
        (super(FootswitchControl, self).__init__)(*a, **k)

    class State(ButtonControl.State):

        def _send_button_color(self):
            if self.color in ('DefaultButton.On', 'DefaultButton.Off'):
                self._control_element.set_light(self.color)


class FootswitchRowControl(ControlList):

    class State(ControlList.State):

        @depends(song=(const(None)))
        def __init__(self, song, *a, **k):
            (super(FootswitchRowControl.State, self).__init__)(*a, **k)
            self.song = song
            self._beat_pulse_end_pulse_timer = None
            self._subdivision_pulse_end_pulse_timer = None
            self._pulse_beat_pulse_leds_timer = None
            self._last_beat = None
            self._last_sub_division = None
            self._State__on_tempo_changed.subject = song
            self._State__on_tempo_changed()

        def update_time(self, time):
            beat = time.beats
            if beat != self._last_beat:
                self._update_led_pulse('Beat_Pulse', True)
                self._beat_pulse_end_pulse_timer.start()
            self._last_beat = beat
            sub_division = time.sub_division
            if sub_division != self._last_sub_division:
                if sub_division % 2 != 0:
                    self._update_led_pulse('Subdivision_Pulse', True)
                    self._subdivision_pulse_end_pulse_timer.start()
            self._last_sub_division = sub_division

        @listens('tempo')
        def __on_tempo_changed(self):
            self._init_led_flashing(self.song.tempo)

        def _init_led_flashing(self, tempo):

            def make_led_end_pulse_timer(pulse_type, pulse_length):
                looper = weakref.ref(self)

                def end_pulse():
                    self = looper()
                    if self:
                        self._update_led_pulse(pulse_type, False)

                return Live.Base.Timer(callback=end_pulse,
                  interval=(int(1000 * pulse_length)),
                  repeat=False)

            seconds_per_beat = old_div(60.0, tempo)
            subdivision_pulse_pulse_length = PULSE_LENGTH_FRACTION * old_div(seconds_per_beat, 2.0)
            beat_pulse_pulse_length = PULSE_LENGTH_FRACTION * seconds_per_beat
            self._subdivision_pulse_end_pulse_timer = make_led_end_pulse_timer('Subdivision_Pulse', subdivision_pulse_pulse_length)
            self._beat_pulse_end_pulse_timer = make_led_end_pulse_timer('Beat_Pulse', beat_pulse_pulse_length)

        def _update_led_pulse(self, pulse_type, on):
            for control in filter(lambda c: c._control_element
, self):
                if control.color == pulse_type:
                    control._control_element.set_light('DefaultButton.On' if on else 'DefaultButton.Off')