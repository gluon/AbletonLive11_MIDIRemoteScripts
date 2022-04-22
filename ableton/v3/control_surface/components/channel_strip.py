# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/channel_strip.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 8271 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from ...base import find_if, liveobj_changed, liveobj_valid
from .. import Component
from ..controls import ButtonControl, MappedButtonControl, MappedControl, control_list
MAX_NUM_SENDS = 12
CROSSFADE_COLORS = ('Mixer.CrossfadeA', 'Mixer.CrossfadeOff', 'Mixer.CrossfadeB')

class ChannelStripComponent(Component):
    _active_instances = []

    @staticmethod
    def other_arm_buttons_pressed(strip):
        return find_if(lambda x: x is not strip and x.arm_button.is_pressed, ChannelStripComponent._active_instances) is not None

    @staticmethod
    def other_solo_buttons_pressed(strip):
        return find_if(lambda x: x is not strip and x.solo_button.is_pressed, ChannelStripComponent._active_instances) is not None

    track_select_button = ButtonControl(disabled_color='Mixer.Empty',
      color='Mixer.NotSelected',
      on_color='Mixer.Selected')
    mute_button = MappedButtonControl(disabled_color='Mixer.Empty',
      color='Mixer.MuteOff',
      on_color='Mixer.MuteOn')
    solo_button = ButtonControl(disabled_color='Mixer.Empty',
      color='Mixer.SoloOff',
      on_color='Mixer.SoloOn')
    arm_button = ButtonControl(disabled_color='Mixer.Empty',
      color='Mixer.ArmOff',
      on_color='Mixer.ArmOn')
    crossfade_cycle_button = ButtonControl(disabled_color='Mixer.Empty')
    volume_control = MappedControl()
    pan_control = MappedControl()
    send_controls = control_list(MappedControl, control_count=MAX_NUM_SENDS)
    indexed_send_controls = control_list(MappedControl, control_count=MAX_NUM_SENDS)

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        ChannelStripComponent._active_instances.append(self)
        self._shift_button = None
        self._track = None
        self.register_slot(self.song.view, self._update_track_select_button, 'selected_track')

        def make_property_slot(property_name, update_method):
            return self.register_slot(None, update_method, property_name)

        self._track_property_slots = [
         make_property_slot('solo', self._update_solo_button),
         make_property_slot('arm', self._update_arm_button),
         make_property_slot('input_routing_type', self._update_arm_button)]
        self._mixer_device_property_slots = [
         make_property_slot('crossfade_assign', self._update_crossfade_cycle_button),
         make_property_slot('sends', self.update)]

    def disconnect(self):
        ChannelStripComponent._active_instances.remove(self)
        self._track = None
        self._shift_button = None
        super().disconnect()

    @property
    def shift_pressed(self):
        return self._shift_button is not None and self._shift_button.is_pressed()

    @property
    def track(self):
        return self._track

    def set_track(self, track):
        self._track = track if liveobj_valid(track) else None
        for slot in self._track_property_slots:
            slot.subject = track

        for slot in self._mixer_device_property_slots:
            slot.subject = track.mixer_device if track else None

        self.update()

    def set_shift_button(self, button):
        self._shift_button = button

    def set_indexed_send_control(self, control, index):
        if index < MAX_NUM_SENDS:
            self.indexed_send_controls.set_control_element_at_index(control, index)
            self.update()

    @track_select_button.pressed
    def track_select_button(self, _):
        if liveobj_changed(self.song.view.selected_track, self._track):
            self.song.view.selected_track = self._track

    @solo_button.pressed
    def solo_button(self, _):
        solo_exclusive = self.song.exclusive_solo != self.shift_pressed and not ChannelStripComponent.other_solo_buttons_pressed(self)
        new_value = not self._track.solo
        for track in chain(self.song.tracks, self.song.return_tracks):
            if not (track == self._track or self._track).is_part_of_selection or track.is_part_of_selection:
                track.solo = new_value
            else:
                if solo_exclusive:
                    if track.solo:
                        track.solo = False

    @arm_button.pressed
    def arm_button(self, _):
        arm_exclusive = self.song.exclusive_arm != self.shift_pressed and not ChannelStripComponent.other_arm_buttons_pressed(self)
        new_value = not self._track.arm
        for track in self.song.tracks:
            if track.can_be_armed:
                if not (track == self._track or self._track).is_part_of_selection or track.is_part_of_selection:
                    track.arm = new_value
                else:
                    if arm_exclusive:
                        if track.arm:
                            track.arm = False

    @crossfade_cycle_button.pressed
    def crossfade_cycle_button(self, _):
        self._track.mixer_device.crossfade_assign = (self._track.mixer_device.crossfade_assign - 1) % len(self._track.mixer_device.crossfade_assignments.values)

    def _all_controls(self):
        return chain([
         self.volume_control, self.pan_control], self.send_controls, self.indexed_send_controls)

    def update(self):
        super().update()
        if self.is_enabled():
            self._update_track_select_button()
            self._update_solo_button()
            self._update_arm_button()
            self._update_crossfade_cycle_button()
            if liveobj_valid(self._track):
                self._connect_parameters()
            else:
                self._disconnect_parameters()
        else:
            self._disconnect_parameters()

    def _disconnect_parameters(self):
        for control in self._all_controls():
            control.mapped_parameter = None

        self.mute_button.mapped_parameter = None

    def _connect_parameters(self):
        self.volume_control.mapped_parameter = self._track.mixer_device.volume
        self.pan_control.mapped_parameter = self._track.mixer_device.panning
        if self._track == self.song.master_track:
            self.mute_button.mapped_parameter = None
        else:
            self.mute_button.mapped_parameter = self._track.mixer_device.track_activator
        self._connect_send_parameters(self.send_controls)
        self._connect_send_parameters(self.indexed_send_controls)

    def _connect_send_parameters(self, send_controls):
        for index, send_control in enumerate(send_controls):
            if index < len(self._track.mixer_device.sends):
                send_control.mapped_parameter = self._track.mixer_device.sends[index]
            else:
                send_control.mapped_parameter = None

    def _update_track_select_button(self):
        self.track_select_button.enabled = liveobj_valid(self._track)
        self.track_select_button.is_on = self.song.view.selected_track == self._track

    def _update_solo_button(self):
        track_valid = liveobj_valid(self._track) and self._track != self.song.master_track
        self.solo_button.enabled = track_valid
        if track_valid:
            self.solo_button.is_on = self._track.solo

    def _update_arm_button(self):
        track_valid = liveobj_valid(self._track) and self._track.can_be_armed
        self.arm_button.enabled = track_valid
        if track_valid:
            self.arm_button.is_on = self._track.arm

    def _update_crossfade_cycle_button(self):
        track_valid = liveobj_valid(self._track) and self._track != self.song.master_track
        self.crossfade_cycle_button.enabled = track_valid
        if track_valid:
            self.crossfade_cycle_button.color = CROSSFADE_COLORS[self._track.mixer_device.crossfade_assign]