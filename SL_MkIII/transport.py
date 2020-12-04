#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/transport.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl

class TransportComponent(TransportComponentBase):

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._loop_toggle.view_transform = lambda v: (u'Transport.LoopOn' if v else u'Transport.LoopOff')
        self._record_toggle.view_transform = lambda v: (u'Recording.On' if v else u'Recording.Off')

    def set_seek_forward_button(self, ffwd_button):
        super(TransportComponent, self).set_seek_forward_button(ffwd_button)
        self._update_seek_button(self._ffwd_button)

    def set_seek_backward_button(self, rwd_button):
        super(TransportComponent, self).set_seek_backward_button(rwd_button)
        self._update_seek_button(self._rwd_button)

    def _ffwd_value(self, value):
        super(TransportComponent, self)._ffwd_value(value)
        self._update_seek_button(self._ffwd_button)

    def _rwd_value(self, value):
        super(TransportComponent, self)._rwd_value(value)
        self._update_seek_button(self._rwd_button)

    def _update_button_states(self):
        super(TransportComponent, self)._update_button_states()
        self._update_continue_playing_button()

    def _update_continue_playing_button(self):
        self.continue_playing_button.color = u'Transport.PlayOn' if self.song.is_playing else u'Transport.PlayOff'

    def _update_seek_button(self, button):
        if self.is_enabled() and button != None:
            button.set_light(u'Transport.SeekOn' if button.is_pressed() else u'Transport.SeekOff')

    def _update_stop_button_color(self):
        self.stop_button.color = u'Transport.StopEnabled' if self.play_button.is_toggled else u'Transport.StopDisabled'
