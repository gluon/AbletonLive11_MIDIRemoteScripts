# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\auto_arm_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 5326 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter
from functools import partial
from ableton.v2.base import mixin, nop
from ableton.v2.control_surface.components import AutoArmComponent
from ableton.v2.control_surface.mode import ModeButtonBehaviour
from .message_box_component import Messenger

class AutoArmRestoreBehaviour(ModeButtonBehaviour):

    def __init__(self, auto_arm=None, *a, **k):
        (super(AutoArmRestoreBehaviour, self).__init__)(*a, **k)
        self._auto_arm = auto_arm
        self._last_update_params = None
        self._should_call_super = True

    def press_immediate(self, component, mode):
        if component.selected_mode != mode:
            component.push_mode(mode)
            self._should_call_super = False
        else:
            self._should_call_super = True
        if self._auto_arm.needs_restore_auto_arm:
            self._auto_arm.restore_auto_arm()
            self._should_call_super = False

    def press_delayed(self, component, mode):
        if self._should_call_super:
            super(AutoArmRestoreBehaviour, self).press_delayed(component, mode)

    def release_immediate(self, component, mode):
        if self._should_call_super:
            super(AutoArmRestoreBehaviour, self).release_immediate(component, mode)

    def release_delayed(self, component, mode):
        if not self._should_call_super or len(component.active_modes) > 1:
            component.pop_mode(mode)
        else:
            super(AutoArmRestoreBehaviour, self).release_delayed(component, mode)

    def update_button(self, component, mode, selected_mode):
        self._last_update_params = (component, mode, selected_mode)
        button = component.get_mode_button(mode)
        button.mode_selected_color = 'DefaultButton.Alert' if self._auto_arm.needs_restore_auto_arm else 'DefaultButton.On'

    def update(self):
        if self._last_update_params:
            (self.update_button)(*self._last_update_params)


class RestoringAutoArmComponent(AutoArmComponent, Messenger):

    def __init__(self, *a, **k):
        AutoArmComponent.active_push_instances.append(self)
        (super(RestoringAutoArmComponent, self).__init__)(*a, **k)
        self._auto_arm_restore_behaviour = None
        self._notification_reference = partial(nop, None)

    def disconnect(self):
        AutoArmComponent.active_push_instances.remove(self)
        super(RestoringAutoArmComponent, self).disconnect()

    def _update_implicit_arm(self):
        super(RestoringAutoArmComponent, self)._update_implicit_arm()
        if self._auto_arm_restore_behaviour:
            self._auto_arm_restore_behaviour.update()
        self._update_notification()

    @property
    def needs_restore_auto_arm(self):
        song = self.song
        exclusive_arm = song.exclusive_arm
        selected_track = song.view.selected_track
        return self.is_enabled() and self.can_auto_arm_track(selected_track) and not selected_track.arm and any(filter(lambda track: (exclusive_arm or self.can_auto_arm_track(track)) and track.can_be_armed and track.arm
, song.tracks))

    def can_auto_arm(self):
        return self.is_enabled() and not self.needs_restore_auto_arm

    def auto_arm_restore_behaviour(self, *extra_classes, **extra_params):
        if not self._auto_arm_restore_behaviour:
            self._auto_arm_restore_behaviour = mixin(AutoArmRestoreBehaviour, *extra_classes)(auto_arm=self, **extra_params)
        else:
            pass
        return self._auto_arm_restore_behaviour

    def restore_auto_arm(self):
        song = self.song
        exclusive_arm = song.exclusive_arm
        for track in song.tracks:
            if not exclusive_arm:
                if self.can_auto_arm_track(track):
                    pass
            if track.can_be_armed:
                track.arm = False

    def _update_notification(self):
        if self.needs_restore_auto_arm:
            self._notification_reference = self.show_notification(('  Press [Note] to arm the track:    ' + self.song.view.selected_track.name),
              blink_text=('  Press        to arm the track:    ' + self.song.view.selected_track.name),
              notification_time=10.0)
        else:
            self._hide_notification()

    def _hide_notification(self):
        if self._notification_reference() is not None:
            self._notification_reference().hide()