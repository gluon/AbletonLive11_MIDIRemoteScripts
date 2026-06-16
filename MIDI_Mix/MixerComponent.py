# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MIDI_Mix\MixerComponent.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1345 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import ButtonControl
from _APC.MixerComponent import MixerComponent as MixerComponentBase

class MixerComponent(MixerComponentBase):
    bank_up_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')
    bank_down_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')

    def __init__(self, *a, **k):
        (super(MixerComponent, self).__init__)(*a, **k)

    def set_send_controls(self, controls):
        self._send_controls = controls
        if controls:
            for index, strip in enumerate(self._channel_strips):
                strip.set_send_controls((
                 controls.get_button(index, 0), controls.get_button(index, 1)))

    @bank_up_button.pressed
    def bank_up_button(self, button):
        new_offset = self._track_offset + len(self._channel_strips)
        if len(self.tracks_to_use()) > new_offset:
            self.set_track_offset(new_offset)

    @bank_down_button.pressed
    def bank_down_button(self, button):
        self.set_track_offset(max(0, self._track_offset - len(self._channel_strips)))