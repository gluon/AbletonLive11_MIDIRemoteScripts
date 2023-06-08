<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/transport.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 2109 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

class TransportComponent(TransportComponentBase):

    def __init__(self, *a, **k):
<<<<<<< HEAD
        (super().__init__)(*a, **k)
=======
        (super(TransportComponent, self).__init__)(*a, **k)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self._loop_toggle.view_transform = lambda v: 'Transport.LoopOn' if v else 'Transport.LoopOff'
        self._record_toggle.view_transform = lambda v: 'Recording.On' if v else 'Recording.Off'

    def set_seek_forward_button(self, ffwd_button):
        super().set_seek_forward_button(ffwd_button)
        self._update_seek_button(self._ffwd_button)

    def set_seek_backward_button(self, rwd_button):
        super().set_seek_backward_button(rwd_button)
        self._update_seek_button(self._rwd_button)

    def _ffwd_value(self, value):
        super()._ffwd_value(value)
        self._update_seek_button(self._ffwd_button)

    def _rwd_value(self, value):
        super()._rwd_value(value)
        self._update_seek_button(self._rwd_button)

    def _update_button_states(self):
        super()._update_button_states()
        self._update_continue_playing_button()

    def _update_continue_playing_button(self):
        self.continue_playing_button.color = 'Transport.PlayOn' if self.song.is_playing else 'Transport.PlayOff'

    def _update_seek_button(self, button):
        if self.is_enabled():
<<<<<<< HEAD
            if button is not None:
=======
            if button != None:
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                button.set_light('Transport.SeekOn' if button.is_pressed() else 'Transport.SeekOff')

    def _update_stop_button_color(self):
        self.stop_button.color = 'Transport.StopEnabled' if self.play_button.is_toggled else 'Transport.StopDisabled'