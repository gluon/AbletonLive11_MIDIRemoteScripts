#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_Essential/transport.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ToggleComponent, TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl

class TransportComponent(TransportComponentBase):
    play_button = ButtonControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._punch_in_toggle = ToggleComponent(u'punch_in', self.song, parent=self)
        self._punch_out_toggle = ToggleComponent(u'punch_out', self.song, parent=self)

    def set_play_button(self, button):
        self.play_button.set_control_element(button)
        self._update_play_button_color()

    def _update_button_states(self):
        self._update_play_button_color()
        self._update_stop_button_color()

    def _update_play_button_color(self):
        self.play_button.color = u'Transport.PlayOn' if self.song.is_playing else u'Transport.PlayOff'

    def _update_stop_button_color(self):
        self.stop_button.color = u'Transport.StopOff' if self.song.is_playing else u'Transport.StopOn'

    @play_button.pressed
    def play_button(self, _):
        if not self.song.is_playing:
            self.song.is_playing = True

    def _ffwd_value(self, value):
        super(TransportComponent, self)._ffwd_value(value)
        self._ffwd_button.set_light(u'DefaultButton.On' if value else u'DefaultButton.Off')

    def _rwd_value(self, value):
        super(TransportComponent, self)._rwd_value(value)
        self._rwd_button.set_light(u'DefaultButton.On' if value else u'DefaultButton.Off')
