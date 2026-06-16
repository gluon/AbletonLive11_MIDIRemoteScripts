# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\auto_arm.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 3586 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import depends, listens, listens_group, task
from ...live import any_track_armed, liveobj_changed, liveobj_valid
from .. import Component

def track_can_be_auto_armed(track):
    return liveobj_valid(track) and track.can_be_armed and track.has_midi_input


class AutoArmComponent(Component):

    @depends(target_track=None)
    def __init__(self, name='Auto_Arm', target_track=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._target_track = target_track
        self._auto_arm_target = None
        self._update_auto_arm_task = self._tasks.add(task.run(self._update_auto_arm))
        self.register_slot(self._target_track, self.update, 'target_track')
        self._AutoArmComponent__on_tracks_changed.subject = self.song
        self._AutoArmComponent__on_tracks_changed()

    def disconnect(self):
        self._setup_new_auto_arm_target(None)
        super().disconnect()

    def update(self):
        super().update()
        self._update_auto_arm()

    def _can_auto_arm(self):
        return self.is_enabled() and not any_track_armed()

    def _auto_arm_target_changed(self, target_track):
        return liveobj_changed(target_track, self._auto_arm_target) or not track_can_be_auto_armed(self._auto_arm_target)

    def _set_auto_arm_state(self, state):
        if liveobj_valid(self._auto_arm_target):
            if self._auto_arm_target.implicit_arm != state:
                self._auto_arm_target.implicit_arm = state

    def _setup_new_auto_arm_target(self, target_track):
        new_target = target_track if track_can_be_auto_armed(target_track) else None
        self._AutoArmComponent__on_implicit_arm_changed.subject = new_target
        self._set_auto_arm_state(False)
        self._auto_arm_target = new_target

    def _update_auto_arm(self):
        self._update_auto_arm_task.kill()
        if self._can_auto_arm():
            target_track = self._target_track.target_track
            if self._auto_arm_target_changed(target_track):
                self._setup_new_auto_arm_target(target_track)
            self._set_auto_arm_state(True)
        else:
            self._setup_new_auto_arm_target(None)

    @listens('implicit_arm')
    def __on_implicit_arm_changed(self):
        self._update_auto_arm()

    @listens_group('arm')
    def __on_arm_changed(self, _):
        self._update_auto_arm_task.restart()

    @listens_group('input_routing_type')
    def __on_input_routing_type_changed(self, _):
        self._update_auto_arm_task.restart()

    @listens_group('is_frozen')
    def __on_frozen_state_changed(self, _):
        self._update_auto_arm_task.restart()

    @listens('tracks')
    def __on_tracks_changed(self):
        tracks = list(filter(lambda t: t.can_be_armed
, self.song.tracks))
        self._AutoArmComponent__on_arm_changed.replace_subjects(tracks)
        self._AutoArmComponent__on_input_routing_type_changed.replace_subjects(tracks)
        self._AutoArmComponent__on_frozen_state_changed.replace_subjects(tracks)