# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad\DefChannelStripComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 16360 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from itertools import chain
import Live
import _Framework.ChannelStripComponent as ChannelStripComponent
from .ConfigurableButtonElement import ConfigurableButtonElement

class DefChannelStripComponent(ChannelStripComponent):

    def __init__(self):
        ChannelStripComponent.__init__(self)
        self._default_volume_button = None
        self._default_panning_button = None
        self._default_send1_button = None
        self._default_send2_button = None
        self._invert_mute_feedback = True

    def disconnect(self):
        if self._track != None:
            volume = self._track.mixer_device.volume
            panning = self._track.mixer_device.panning
            sends = self._track.mixer_device.sends
            if volume.value_has_listener(self._on_volume_changed):
                volume.remove_value_listener(self._on_volume_changed)
            if panning.value_has_listener(self._on_panning_changed):
                panning.remove_value_listener(self._on_panning_changed)
            if len(sends) > 0:
                if sends[0].value_has_listener(self._on_send1_changed):
                    sends[0].remove_value_listener(self._on_send1_changed)
            if len(sends) > 1:
                if sends[1].value_has_listener(self._on_send2_changed):
                    sends[1].remove_value_listener(self._on_send2_changed)
        if self._default_volume_button != None:
            self._default_volume_button.remove_value_listener(self._default_volume_value)
            self._default_volume_button = None
        if self._default_panning_button != None:
            self._default_panning_button.remove_value_listener(self._default_panning_value)
            self._default_panning_button = None
        if self._default_send1_button != None:
            self._default_send1_button.remove_value_listener(self._default_send1_value)
            self._default_send1_button = None
        if self._default_send2_button != None:
            self._default_send2_button.remove_value_listener(self._default_send2_value)
            self._default_send2_button = None
        ChannelStripComponent.disconnect(self)

    def set_track(self, track):
        if track != self._track:
            if self._track != None:
                volume = self._track.mixer_device.volume
                panning = self._track.mixer_device.panning
                sends = self._track.mixer_device.sends
                if volume.value_has_listener(self._on_volume_changed):
                    volume.remove_value_listener(self._on_volume_changed)
                if panning.value_has_listener(self._on_panning_changed):
                    panning.remove_value_listener(self._on_panning_changed)
                if len(sends) > 0:
                    if sends[0].value_has_listener(self._on_send1_changed):
                        sends[0].remove_value_listener(self._on_send1_changed)
                if len(sends) > 1:
                    if sends[1].value_has_listener(self._on_send2_changed):
                        sends[1].remove_value_listener(self._on_send2_changed)
            ChannelStripComponent.set_track(self, track)
        else:
            self.update()

    def set_default_buttons(self, volume, panning, send1, send2):
        if volume != self._default_volume_button:
            if self._default_volume_button != None:
                self._default_volume_button.remove_value_listener(self._default_volume_value)
            self._default_volume_button = volume
            if self._default_volume_button != None:
                self._default_volume_button.add_value_listener(self._default_volume_value)
        if panning != self._default_panning_button:
            if self._default_panning_button != None:
                self._default_panning_button.remove_value_listener(self._default_panning_value)
            self._default_panning_button = panning
            if self._default_panning_button != None:
                self._default_panning_button.add_value_listener(self._default_panning_value)
        if send1 != self._default_send1_button:
            if self._default_send1_button != None:
                self._default_send1_button.remove_value_listener(self._default_send1_value)
            self._default_send1_button = send1
            if self._default_send1_button != None:
                self._default_send1_button.add_value_listener(self._default_send1_value)
        if send2 != self._default_send2_button:
            if self._default_send2_button != None:
                self._default_send2_button.remove_value_listener(self._default_send2_value)
            self._default_send2_button = send2
            if self._default_send2_button != None:
                self._default_send2_button.add_value_listener(self._default_send2_value)
        self.update()

    def set_send_controls(self, controls):
        if controls != self._send_controls:
            self._send_controls = controls
            if self._send_controls != None:
                for control in self._send_controls:
                    if control != None:
                        control.reset()

            self.update()

    def update(self):
        super(DefChannelStripComponent, self).update()
        if self._allow_updates:
            if self.is_enabled():
                if self._track != None:
                    volume = self._track.mixer_device.volume
                    panning = self._track.mixer_device.panning
                    sends = self._track.mixer_device.sends
                    if not volume.value_has_listener(self._on_volume_changed):
                        volume.add_value_listener(self._on_volume_changed)
                    if not panning.value_has_listener(self._on_panning_changed):
                        panning.add_value_listener(self._on_panning_changed)
                    if len(sends) > 0:
                        if not sends[0].value_has_listener(self._on_send1_changed):
                            sends[0].add_value_listener(self._on_send1_changed)
                        self._on_send1_changed()
                    else:
                        if self._default_send1_button != None:
                            self._default_send1_button.turn_off()
                    if len(sends) > 1:
                        if not sends[1].value_has_listener(self._on_send2_changed):
                            sends[1].add_value_listener(self._on_send2_changed)
                        self._on_send2_changed()
                    else:
                        if self._default_send2_button != None:
                            self._default_send2_button.turn_off()
                    self._on_volume_changed()
                    self._on_panning_changed()
                else:
                    if self._default_volume_button != None:
                        self._default_volume_button.reset()
                    if self._default_panning_button != None:
                        self._default_panning_button.reset()
                    if self._default_send1_button != None:
                        self._default_send1_button.reset()
                    if self._default_send2_button != None:
                        self._default_send2_button.reset()
                    if self._mute_button != None:
                        self._mute_button.reset()
                    if self._arm_button != None:
                        self._arm_button.reset()
                    if self._solo_button != None:
                        self._solo_button.reset()
                    if self._volume_control != None:
                        self._volume_control.reset()
                    if self._pan_control != None:
                        self._pan_control.reset()
                    if self._send_controls != None:
                        for send_control in self._send_controls:
                            if send_control != None:
                                send_control.reset()

    def _default_volume_value(self, value):
        if not self.is_enabled() or self._track != None:
            if not (value != 0 or self._default_volume_button.is_momentary()):
                volume = self._track.mixer_device.volume
                if volume.is_enabled:
                    volume.value = volume.default_value

    def _default_panning_value(self, value):
        if not self.is_enabled() or self._track != None:
            if not (value != 0 or self._default_panning_button.is_momentary()):
                panning = self._track.mixer_device.panning
                if panning.is_enabled:
                    panning.value = panning.default_value

    def _default_send1_value(self, value):
        if not self.is_enabled() and self._track != None or len(self._track.mixer_device.sends) > 0:
            if not (value != 0 or self._default_send1_button.is_momentary()):
                send1 = self._track.mixer_device.sends[0]
                if send1.is_enabled:
                    send1.value = send1.default_value

    def _default_send2_value(self, value):
        if not self.is_enabled() and self._track != None or len(self._track.mixer_device.sends) > 1:
            if not (value != 0 or self._default_send2_button.is_momentary()):
                send2 = self._track.mixer_device.sends[1]
                if send2.is_enabled:
                    send2.value = send2.default_value

    def _on_mute_changed(self):
        if self.is_enabled():
            if self._mute_button != None:
                if self._track != None:
                    if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mute != self._invert_mute_feedback:
                        self._mute_button.turn_on()
                    else:
                        self._mute_button.turn_off()
                else:
                    self._mute_button.send_value(0)

    def _on_solo_changed(self):
        if self.is_enabled():
            if self._solo_button != None:
                if self._track != None:
                    if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.solo:
                        self._solo_button.turn_on()
                    else:
                        self._solo_button.turn_off()
                else:
                    self._solo_button.send_value(0)

    def _on_arm_changed(self):
        if self.is_enabled():
            if self._arm_button != None:
                if self._track != None:
                    if self._track in self.song().tracks and self._track.can_be_armed and self._track.arm:
                        self._arm_button.turn_on()
                    else:
                        self._arm_button.turn_off()
                else:
                    self._arm_button.send_value(0)

    def _on_volume_changed(self):
        if self.is_enabled():
            if self._default_volume_button != None:
                volume = self._track.mixer_device.volume
                if volume.value == volume.default_value:
                    self._default_volume_button.turn_on()
                else:
                    self._default_volume_button.turn_off()

    def _on_panning_changed(self):
        if self.is_enabled():
            if self._default_panning_button != None:
                panning = self._track.mixer_device.panning
                if panning.value == panning.default_value:
                    self._default_panning_button.turn_on()
                else:
                    self._default_panning_button.turn_off()

    def _on_send1_changed(self):
        sends = self._track.mixer_device.sends
        if self.is_enabled():
            if self._default_send1_button != None:
                send1 = sends[0]
                if send1.value == send1.default_value:
                    self._default_send1_button.turn_on()
                else:
                    self._default_send1_button.turn_off()

    def _on_send2_changed(self):
        sends = self._track.mixer_device.sends
        if self.is_enabled():
            if self._default_send2_button != None:
                send2 = sends[1]
                if send2.value == send2.default_value:
                    self._default_send2_button.turn_on()
                else:
                    self._default_send2_button.turn_off()