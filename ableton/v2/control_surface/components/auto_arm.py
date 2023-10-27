# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\auto_arm.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4741 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter
from ...base import listens, listens_group, task
from ...control_surface import Component

class AutoArmBase(Component):
    active_instances = []
    active_push_instances = []

    def __init__(self, *a, **k):
        (super(AutoArmBase, self).__init__)(*a, **k)
        self.active_instances.append(self)
        self._update_implicit_arm_task = self._tasks.add(task.run(self._update_implicit_arm))

    def disconnect(self):
        self.active_instances.remove(self)
        if self.active_instances or self.active_push_instances:
            self._update_implicit_arm_task.restart()
        super(AutoArmBase, self).disconnect()

    def update(self):
        super(AutoArmBase, self).update()
        self._update_implicit_arm()

    def _update_implicit_arm(self):
        raise NotImplementedError


class AutoArmComponent(AutoArmBase):

    def __init__(self, *a, **k):
        (super(AutoArmComponent, self).__init__)(*a, **k)
        self._on_tracks_changed.subject = self.song
        self._on_exclusive_arm_changed.subject = self.song
        self._on_tracks_changed()
        self._on_selected_track_changed.subject = self.song.view

    @property
    def needs_restore_auto_arm(self):
        song = self.song
        exclusive_arm = song.exclusive_arm
        selected_track = song.view.selected_track
        return self.can_auto_arm_track(selected_track) and not selected_track.arm and any(filter(lambda track: (exclusive_arm or self.can_auto_arm_track(track)) and track.can_be_armed and track.arm
, song.tracks))

    def track_can_be_armed(self, track):
        return track.can_be_armed and track.has_midi_input

    def can_auto_arm(self):
        return any([instance.is_enabled() for instance in AutoArmComponent.active_instances]) and not self.needs_restore_auto_arm

    def can_auto_arm_track(self, track):
        return self.track_can_be_armed(track)

    def can_update_implicit_arm(self):
        return not AutoArmComponent.active_push_instances or self in AutoArmComponent.active_push_instances

    @listens('selected_track')
    def _on_selected_track_changed(self):
        self.update()

    def _update_implicit_arm(self):
        self._update_implicit_arm_task.kill()
        if self.can_update_implicit_arm():
            song = self.song
            selected_track = song.view.selected_track
            can_auto_arm = self.can_auto_arm()
            for track in song.tracks:
                if self.track_can_be_armed(track):
                    track.implicit_arm = can_auto_arm and selected_track == track and self.can_auto_arm_track(track)

    @listens('tracks')
    def _on_tracks_changed(self):
        tracks = list(filter(lambda t: t.can_be_armed
, self.song.tracks))
        self._on_arm_changed.replace_subjects(tracks)
        self._on_input_routing_type_changed.replace_subjects(tracks)
        self._on_frozen_state_changed.replace_subjects(tracks)

    @listens('exclusive_arm')
    def _on_exclusive_arm_changed(self):
        self.update()

    @listens_group('arm')
    def _on_arm_changed(self, track):
        self._update_implicit_arm_task.restart()

    @listens_group('input_routing_type')
    def _on_input_routing_type_changed(self, track):
        self._update_implicit_arm_task.restart()

    @listens_group('is_frozen')
    def _on_frozen_state_changed(self, track):
        self._update_implicit_arm_task.restart()