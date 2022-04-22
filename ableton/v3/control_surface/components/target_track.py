# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/target_track.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 4769 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import depends, listens, listens_group, liveobj_changed, liveobj_valid
from .. import Component
from ..controls import ToggleButtonControl

class TargetTrackComponent(Component):
    __events__ = ('target_track', 'is_locked_to_track')
    lock_button = ToggleButtonControl(untoggled_color='TargetTrack.LockOff',
      toggled_color='TargetTrack.LockOn')

    @depends(show_message=None)
    def __init__(self, name='Target_Track', show_message=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._show_message = show_message
        self._target_track = None
        self._locked_to_track = False
        self.register_slot(self.song.view, self._selected_track_changed, 'selected_track')
        self._selected_track_changed()

    def disconnect(self):
        self._target_track = None
        super().disconnect()

    @property
    def target_track(self):
        return self._target_track

    @property
    def is_locked_to_track(self):
        return self._locked_to_track

    @is_locked_to_track.setter
    def is_locked_to_track(self, is_locked):
        self._locked_to_track = is_locked
        current_track = self._target_track
        self._set_target_track()
        self.notify_is_locked_to_track()
        if self._locked_to_track:
            self._show_message('Locked to {}'.format(self._target_track.name))
        else:
            self._show_message('Unlocked from {}'.format(current_track.name))

    @lock_button.toggled
    def lock_button(self, is_toggled, _):
        self.is_locked_to_track = is_toggled

    def _selected_track_changed(self):
        self._set_target_track()

    def _set_target_track(self):
        if not (self._locked_to_track and liveobj_valid(self._target_track)):
            new_target = self._get_new_target_track()
            if liveobj_changed(self._target_track, new_target):
                self._target_track = new_target
                self.notify_target_track()
            if self._locked_to_track:
                self._locked_to_track = False
                self.lock_button.is_toggled = False
                self.notify_is_locked_to_track()

    def _get_new_target_track(self):
        return self.song.view.selected_track


class ArmedTargetTrackComponent(TargetTrackComponent):

    def __init__(self, *a, **k):
        self._armed_track_list = []
        (super().__init__)(*a, **k)
        self._ArmedTargetTrackComponent__on_tracks_changed.subject = self.song
        self._ArmedTargetTrackComponent__on_tracks_changed()

    def disconnect(self):
        self._armed_track_list = None
        super().disconnect()

    @property
    def tracks(self):
        return [t for t in self.song.tracks if liveobj_valid(t) if t.can_be_armed]

    def _selected_track_changed(self):
        if not self._armed_track_list:
            self._set_target_track()

    def _get_new_target_track(self):
        if self._armed_track_list:
            return self._armed_track_list[(-1)]
        return super()._get_new_target_track()

    @listens('visible_tracks')
    def __on_tracks_changed(self):
        tracks = self.tracks
        self._ArmedTargetTrackComponent__on_arm_changed.replace_subjects(tracks)
        self._ArmedTargetTrackComponent__on_frozen_state_changed.replace_subjects(tracks)
        self._refresh_armed_track_list()

    @listens_group('arm')
    def __on_arm_changed(self, _):
        self._refresh_armed_track_list()

    @listens_group('is_frozen')
    def __on_frozen_state_changed(self, _):
        self._refresh_armed_track_list()

    def _refresh_armed_track_list(self):
        tracks = self.tracks
        for track in self._armed_track_list:
            if liveobj_valid(track):
                if track.arm:
                    if not track.is_frozen:
                        if track not in tracks:
                            pass
                    self._armed_track_list.remove(track)

        for track in tracks:
            if track.arm:
                if not track.is_frozen:
                    if track not in self._armed_track_list:
                        self._armed_track_list.append(track)

        self._set_target_track()