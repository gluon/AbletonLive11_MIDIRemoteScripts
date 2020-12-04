#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Blackstar_Live_Logic/footswitch_row_control.py
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
import weakref
import Live
from ableton.v2.base import const, depends, mixin, listens
from ableton.v2.control_surface.control import ButtonControl, control_list, ControlList
PULSE_COLORS = set([u'Beat_Pulse', u'Subdivision_Pulse'])
PULSE_LENGTH_FRACTION = 0.2

def footswitch_row_control(*a, **k):
    c = mixin(FootswitchRowControl, FootswitchControl)
    return c(FootswitchControl, *a, **k)


class FootswitchControl(ButtonControl):
    DOUBLE_CLICK_DELAY = 0.8

    def __init__(self, *a, **k):
        super(FootswitchControl, self).__init__(*a, **k)

    class State(ButtonControl.State):

        def _send_button_color(self):
            if self.color in (u'DefaultButton.On', u'DefaultButton.Off'):
                self._control_element.set_light(self.color)


class FootswitchRowControl(ControlList):
    u"""
    A specialized `ControlList` that represents
    a row of footswitches with leds
    
    The control must be given the song time via
    `update_time` in order to blink the leds.
    """

    class State(ControlList.State):

        @depends(song=const(None))
        def __init__(self, song, *a, **k):
            super(FootswitchRowControl.State, self).__init__(*a, **k)
            assert song is not None
            self.song = song
            self._beat_pulse_end_pulse_timer = None
            self._subdivision_pulse_end_pulse_timer = None
            self._pulse_beat_pulse_leds_timer = None
            self._last_beat = None
            self._last_sub_division = None
            self.__on_tempo_changed.subject = song
            self.__on_tempo_changed()

        def update_time(self, time):
            beat = time.beats
            if beat != self._last_beat:
                self._update_led_pulse(u'Beat_Pulse', True)
                self._beat_pulse_end_pulse_timer.start()
            self._last_beat = beat
            sub_division = time.sub_division
            if sub_division != self._last_sub_division and sub_division % 2 != 0:
                self._update_led_pulse(u'Subdivision_Pulse', True)
                self._subdivision_pulse_end_pulse_timer.start()
            self._last_sub_division = sub_division

        @listens(u'tempo')
        def __on_tempo_changed(self):
            self._init_led_flashing(self.song.tempo)

        def _init_led_flashing(self, tempo):

            def make_led_end_pulse_timer(pulse_type, pulse_length):
                looper = weakref.ref(self)

                def end_pulse():
                    self = looper()
                    if self:
                        self._update_led_pulse(pulse_type, False)

                return Live.Base.Timer(callback=end_pulse, interval=int(1000 * pulse_length), repeat=False)

            seconds_per_beat = old_div(60.0, tempo)
            subdivision_pulse_pulse_length = PULSE_LENGTH_FRACTION * old_div(seconds_per_beat, 2.0)
            beat_pulse_pulse_length = PULSE_LENGTH_FRACTION * seconds_per_beat
            self._subdivision_pulse_end_pulse_timer = make_led_end_pulse_timer(u'Subdivision_Pulse', subdivision_pulse_pulse_length)
            self._beat_pulse_end_pulse_timer = make_led_end_pulse_timer(u'Beat_Pulse', beat_pulse_pulse_length)

        def _update_led_pulse(self, pulse_type, on):
            assert pulse_type in PULSE_COLORS
            for control in filter(lambda c: c._control_element, self):
                if control.color == pulse_type:
                    control._control_element.set_light(u'DefaultButton.On' if on else u'DefaultButton.Off')
