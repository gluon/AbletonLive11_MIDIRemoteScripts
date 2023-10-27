# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\velocity_levels_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 5800 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from ableton.v2.base import EventObject, NamedTuple, listenable_property, listens, liveobj_valid, task
from ableton.v2.control_surface.components import PlayableComponent
from ableton.v2.control_surface.control import ButtonControl, control_matrix
from .matrix_maps import NON_FEEDBACK_CHANNEL
from .pad_control import PadControl
SLICE_MODE = Live.SimplerDevice.PlaybackMode.slicing
BASE_SLICING_NOTE = 36
INVALID_LEVEL = -1.0

class NullTargetNoteProvider(EventObject):

    @listenable_property
    def selected_target_note(self):
        return NamedTuple(note=(-1), channel=(-1))


class VelocityLevelsComponent(PlayableComponent):
    SOURCE_NOTES = list(reversed(list(range(64, 128))))
    DEFAULT_VELOCITY = 100
    matrix = control_matrix(PadControl)
    select_button = ButtonControl()

    def __init__(self, velocity_levels=None, target_note_provider=None, skin_base_key=None, *a, **k):
        (super(VelocityLevelsComponent, self).__init__)(*a, **k)
        self._target_note_provider = target_note_provider or NullTargetNoteProvider()
        self._VelocityLevelsComponent__on_selected_target_note_changed.subject = self._target_note_provider
        self._played_level = INVALID_LEVEL
        self.set_skin_base_key(skin_base_key or 'VelocityLevels')
        self._notification_task = self._tasks.add(task.run(self._update_velocity))
        self._notification_task.kill()
        self.set_velocity_levels(velocity_levels)

    @listenable_property
    def velocity(self):
        if 0<= self._played_level < 128:
            return self._played_level
        return self.DEFAULT_VELOCITY

    def set_velocities_playable(self, playable):
        self._notification_task.kill()
        self._set_control_pads_from_script(not playable)

    def set_velocity_levels(self, velocity_levels):
        self.velocity_levels = velocity_levels
        self._VelocityLevelsComponent__on_last_played_level.subject = velocity_levels
        self.update()

    def set_matrix(self, matrix):
        super(VelocityLevelsComponent, self).set_matrix(matrix)
        self._update_sensitivity_profile()

    def _update_control_from_script(self):
        super(VelocityLevelsComponent, self)._update_control_from_script()
        self._update_sensitivity_profile()

    def _update_sensitivity_profile(self):
        profile = 'default' if self._takeover_pads else 'drums'
        for button in self.matrix:
            button.sensitivity_profile = profile

    def _update_velocity(self):
        self._notification_task.kill()
        self.notify_velocity()

    def set_skin_base_key(self, base_key):
        self._skin_base_key = base_key
        self._update_led_feedback()

    @matrix.pressed
    def matrix(self, button):
        self._on_matrix_pressed(button)

    @matrix.released
    def matrix(self, button):
        self._on_matrix_released(button)

    @select_button.pressed
    def select_button(self, _value):
        self._set_control_pads_from_script(True)

    @select_button.released
    def select_button(self, _value):
        self._set_control_pads_from_script(False)

    def _on_matrix_pressed(self, button):
        has_levels = liveobj_valid(self.velocity_levels)
        levels = self.velocity_levels.levels if has_levels else []
        index = self._button_index(button)
        self._played_level = levels[index] if index < len(levels) else INVALID_LEVEL
        self._update_led_feedback()
        self.notify_velocity()

    @listens('selected_target_note')
    def __on_selected_target_note_changed(self):
        self.update()

    @listens('last_played_level')
    def __on_last_played_level(self):
        if not self._takeover_pads:
            played = self.velocity_levels.last_played_level if liveobj_valid(self.velocity_levels) else INVALID_LEVEL
            self._played_level = played
            self._update_led_feedback()
            self._notification_task.restart()

    def _button_index(self, button):
        y, x = button.coordinate
        return (self.height - 1 - y) * self.width + x

    def _note_translation_for_button(self, button):
        return (
         self.SOURCE_NOTES[self._button_index(button)], NON_FEEDBACK_CHANNEL)

    def _update_button_color(self, button):
        index = self._button_index(button)
        levels = self.velocity_levels.levels if liveobj_valid(self.velocity_levels) else []
        if index < len(levels) and self._played_level == levels[index]:
            color = 'SelectedLevel'
        else:
            y, _ = button.coordinate
            color = 'MidLevel'
            if y == 0:
                color = 'HighLevel'
            else:
                if y == self.height - 1:
                    color = 'LowLevel'
        button.color = self._skin_base_key + '.' + color

    def update(self):
        super(VelocityLevelsComponent, self).update()
        if liveobj_valid(self.velocity_levels):
            self.velocity_levels.enabled = self.is_enabled()
            self.velocity_levels.source_channel = NON_FEEDBACK_CHANNEL
            self.velocity_levels.notes = self.SOURCE_NOTES[:self.width * self.height]
            target_note = self._target_note_provider.selected_target_note
            self.velocity_levels.target_note = target_note.note
            self.velocity_levels.target_channel = target_note.channel
        if not self.is_enabled():
            self._notification_task.kill()