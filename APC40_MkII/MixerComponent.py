# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC40_MkII\MixerComponent.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 4063 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import chr, filter
from future.moves.itertools import zip_longest
from _Framework.Control import RadioButtonControl, control_list
from _Framework.Dependency import depends
from _Framework.Util import nop
from _APC.MixerComponent import ChanStripComponent as ChannelStripComponentBase
from _APC.MixerComponent import MixerComponent as MixerComponentBase

class ChannelStripComponent(ChannelStripComponentBase):

    def _on_cf_assign_changed(self):
        if self.is_enabled():
            if self._crossfade_toggle:
                state = self._track.mixer_device.crossfade_assign if self._track else 1
                value_to_send = None
                if state == 0:
                    value_to_send = 'Mixer.Crossfade.A'
                else:
                    if state == 1:
                        value_to_send = 'Mixer.Crossfade.Off'
                    else:
                        if state == 2:
                            value_to_send = 'Mixer.Crossfade.B'
                self._crossfade_toggle.set_light(value_to_send)


def _set_channel(controls, channel):
    for control in filter(None, controls or []):
        control.set_channel(channel)


class MixerComponent(MixerComponentBase):
    send_select_buttons = control_list(RadioButtonControl)

    @depends(show_message=nop)
    def __init__(self, num_tracks=0, show_message=nop, *a, **k):
        (super(MixerComponent, self).__init__)(a, num_tracks=num_tracks, **k)
        self._show_message = show_message
        self.on_num_sends_changed()
        self._pan_controls = None
        self._send_controls = None
        self._user_controls = None

    def _create_strip(self):
        return ChannelStripComponent()

    @send_select_buttons.checked
    def send_select_buttons(self, button):
        self.send_index = button.index

    def on_num_sends_changed(self):
        self.send_select_buttons.control_count = self.num_sends

    def on_send_index_changed(self):
        if self.send_index is None:
            self.send_select_buttons.control_count = 0
        else:
            if self.send_index < self.send_select_buttons.control_count:
                self.send_select_buttons[self.send_index].is_checked = True
        if self.is_enabled():
            if self._send_controls:
                self._show_controlled_sends_message()

    def _show_controlled_sends_message(self):
        if self._send_index is not None:
            send_name = chr(ord('A') + self._send_index)
            self._show_message('Controlling Send %s' % send_name)

    def set_pan_controls(self, controls):
        super(MixerComponent, self).set_pan_controls(controls)
        self._pan_controls = controls
        self._update_pan_controls()
        if self.is_enabled():
            if controls:
                self._show_message('Controlling Pans')

    def set_send_controls(self, controls):
        super(MixerComponent, self).set_send_controls(controls)
        self._send_controls = controls
        self._update_send_controls()
        if self.is_enabled():
            if controls:
                self._show_controlled_sends_message()

    def set_user_controls(self, controls):
        self._user_controls = controls
        self._update_user_controls()
        if self.is_enabled():
            if controls:
                self._show_message('Controlling User Mappings')

    def set_crossfade_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_crossfade_toggle(button)

    def _update_pan_controls(self):
        _set_channel(self._pan_controls, 0)

    def _update_send_controls(self):
        _set_channel(self._send_controls, 1)

    def _update_user_controls(self):
        _set_channel(self._user_controls, 2)

    def update(self):
        super(MixerComponent, self).update()
        if self.is_enabled():
            self._update_pan_controls()
            self._update_send_controls()
            self._update_user_controls()