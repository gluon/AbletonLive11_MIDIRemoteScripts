# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\channel_strip.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 9960 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from typing import cast
from ...base import find_if
from ...live import action, is_track_armed, liveobj_changed, liveobj_valid
from .. import Component
from ..controls import ButtonControl, MappedButtonControl, MappedControl, control_list
from ..display import Renderable
from ..skin import LiveObjSkinEntry
MAX_NUM_SENDS = 12
CROSSFADE_COLORS = ('Mixer.CrossfadeA', 'Mixer.CrossfadeOff', 'Mixer.CrossfadeB')

class ChannelStripComponent(Component, Renderable):
    include_in_top_level_state = False
    _active_instances = []

    @staticmethod
    def other_arm_buttons_pressed(strip):
        return find_if(lambda x: x is not strip and x.arm_button.is_pressed
, ChannelStripComponent._active_instances) is not None

    @staticmethod
    def other_solo_buttons_pressed(strip):
        return find_if(lambda x: x is not strip and x.solo_button.is_pressed
, ChannelStripComponent._active_instances) is not None

    volume_control = MappedControl()
    pan_control = MappedControl()
    send_controls = control_list(MappedControl, control_count=MAX_NUM_SENDS)
    indexed_send_controls = control_list(MappedControl, control_count=MAX_NUM_SENDS)
    track_select_button = ButtonControl(disabled_color='Mixer.NoTrack')
    mute_button = MappedButtonControl(disabled_color='Mixer.NoTrack',
      color='Mixer.MuteOff',
      on_color='Mixer.MuteOn')
    solo_button = ButtonControl(disabled_color='Mixer.NoTrack',
      color='Mixer.SoloOff',
      on_color='Mixer.SoloOn')
    arm_button = ButtonControl(disabled_color='Mixer.NoTrack',
      color='Mixer.ArmOff',
      on_color='Mixer.ArmOn')
    crossfade_cycle_button = ButtonControl(disabled_color='Mixer.NoTrack')
    shift_button = ButtonControl(color=None)

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        ChannelStripComponent._active_instances.append(self)
        self._track = None
        self.register_slot(self.song.view, self._update_track_select_button, 'selected_track')

        def make_property_slot(property_name, update_method):
            return self.register_slot(None, update_method, property_name)

        self._track_property_slots = [
         make_property_slot('solo', self._update_solo_button),
         make_property_slot('arm', self._update_arm_button),
         make_property_slot('implicit_arm', self._update_arm_button),
         make_property_slot('input_routing_type', self._update_arm_button),
         make_property_slot('color', self._update_track_select_button)]
        self._mixer_device_property_slots = [
         make_property_slot('crossfade_assign', self._update_crossfade_cycle_button),
         make_property_slot('sends', self.update)]

    def disconnect(self):
        ChannelStripComponent._active_instances.remove(self)
        self._track = None
        super().disconnect()

    @property
    def track(self):
        return self._track

    def set_track(self, track):
        if liveobj_changed(track, self._track):
            self._track = track if liveobj_valid(track) else None
            for slot in self._track_property_slots:
                slot.subject = track

            for slot in self._mixer_device_property_slots:
                slot.subject = track.mixer_device if track else None

            self.update()

    def set_indexed_send_control(self, control_element, index):
        if index < MAX_NUM_SENDS:
            self.indexed_send_controls.set_control_element_at_index(control_element, index)
            self.update()

    @track_select_button.pressed
    def track_select_button(self, _):
        if liveobj_changed(self.song.view.selected_track, self._track):
            self.song.view.selected_track = self._track
            self.notify(self.notifications.Track.select, cast(str, self._track.name))

    @solo_button.pressed
    def solo_button(self, _):
        solo_exclusive = self.song.exclusive_solo != self.shift_button.is_pressed and not ChannelStripComponent.other_solo_buttons_pressed(self)
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
        arm_exclusive = self.song.exclusive_arm != self.shift_button.is_pressed and not ChannelStripComponent.other_arm_buttons_pressed(self)
        action.arm((self._track), exclusive=arm_exclusive)

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
        has_track = liveobj_valid(self._track)
        self.track_select_button.enabled = has_track
        if has_track:
            is_selected = self.song.view.selected_track == self._track
            self.track_select_button.color = LiveObjSkinEntry('Mixer.{}'.format('Selected' if is_selected else 'NotSelected'), self._track)

    def _update_solo_button(self):
        track_valid = liveobj_valid(self._track) and self._track != self.song.master_track
        self.solo_button.enabled = track_valid
        if track_valid:
            self.solo_button.is_on = self._track.solo

    def _update_arm_button(self):
        track_valid = liveobj_valid(self._track) and self._track.can_be_armed
        self.arm_button.enabled = track_valid
        if track_valid:
            self.arm_button.on_color = 'Mixer.ArmOn' if self._track.arm else 'Mixer.ImplicitArmOn'
            self.arm_button.is_on = is_track_armed(self._track)

    def _update_crossfade_cycle_button(self):
        track_valid = liveobj_valid(self._track) and self._track != self.song.master_track
        self.crossfade_cycle_button.enabled = track_valid
        if track_valid:
            self.crossfade_cycle_button.color = CROSSFADE_COLORS[self._track.mixer_device.crossfade_assign]