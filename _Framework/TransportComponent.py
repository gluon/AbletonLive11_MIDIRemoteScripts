# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\TransportComponent.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 9797 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from past.utils import old_div
from functools import partial
import Live
from . import Task
from .CompoundComponent import CompoundComponent
from .SubjectSlot import subject_slot
from .ToggleComponent import ToggleComponent
from .Util import clamp, const, in_range
TEMPO_TOP = 200.0
TEMPO_BOTTOM = 60.0
TEMPO_FINE_RANGE = 2.56
SEEK_SPEED = 10.0

class TransportComponent(CompoundComponent):

    def __init__(self, play_toggle_model_transform=const(True), *a, **k):
        (super(TransportComponent, self).__init__)(*a, **k)
        self._ffwd_button = None
        self._rwd_button = None
        self._tap_tempo_button = None
        self._tempo_control = None
        self._tempo_fine_control = None
        self._song_position_control = None
        self._rwd_task = Task.Task()
        self._ffwd_task = Task.Task()
        self._fine_tempo_needs_pickup = True
        self._prior_fine_tempo_value = -1
        self._end_undo_step_task = self._tasks.add(Task.sequence(Task.wait(1.5), Task.run(self.song().end_undo_step)))
        self._end_undo_step_task.kill()
        song = self.song()
        self._loop_toggle, self._punch_in_toggle, self._punch_out_toggle, self._record_toggle, self._play_toggle, self._stop_toggle, self._nudge_down_toggle, self._nudge_up_toggle, self._metronome_toggle, self._arrangement_overdub_toggle, self._overdub_toggle = self.register_components(ToggleComponent('loop', song), ToggleComponent('punch_in', song, is_momentary=True), ToggleComponent('punch_out', song, is_momentary=True), ToggleComponent('record_mode', song), ToggleComponent('is_playing',
          song, model_transform=play_toggle_model_transform), ToggleComponent('is_playing',
          song,
          model_transform=(const(False)),
          view_transform=(const(False))), ToggleComponent('nudge_down', song, is_momentary=True), ToggleComponent('nudge_up', song, is_momentary=True), ToggleComponent('metronome', song), ToggleComponent('arrangement_overdub', song), ToggleComponent('overdub', song))

    def set_stop_button(self, button):
        self._stop_toggle.set_toggle_button(button)

    def set_play_button(self, button):
        self._play_toggle.set_toggle_button(button)

    def set_seek_buttons(self, ffwd_button, rwd_button):
        if self._ffwd_button != ffwd_button:
            self._ffwd_button = ffwd_button
            self._ffwd_value_slot.subject = ffwd_button
            self._ffwd_task.kill()
        if self._rwd_button != rwd_button:
            self._rwd_button = rwd_button
            self._rwd_value_slot.subject = rwd_button
            self._rwd_task.kill()

    def set_seek_forward_button(self, ffwd_button):
        if self._ffwd_button != ffwd_button:
            self._ffwd_button = ffwd_button
            self._ffwd_value_slot.subject = ffwd_button
            self._ffwd_task.kill()

    def set_seek_backward_button(self, rwd_button):
        if self._rwd_button != rwd_button:
            self._rwd_button = rwd_button
            self._rwd_value_slot.subject = rwd_button
            self._rwd_task.kill()

    def set_nudge_buttons(self, up_button, down_button):
        self._nudge_up_toggle.set_toggle_button(up_button)
        self._nudge_down_toggle.set_toggle_button(down_button)

    def set_nudge_up_button(self, up_button):
        self._nudge_up_toggle.set_toggle_button(up_button)

    def set_nudge_down_button(self, down_button):
        self._nudge_down_toggle.set_toggle_button(down_button)

    def set_record_button(self, button):
        self._record_toggle.set_toggle_button(button)

    def set_tap_tempo_button(self, button):
        if self._tap_tempo_button != button:
            self._tap_tempo_button = button
            self._tap_tempo_value.subject = button
            self._update_tap_tempo_button()

    def set_loop_button(self, button):
        self._loop_toggle.set_toggle_button(button)

    def set_punch_buttons(self, in_button, out_button):
        self._punch_in_toggle.set_toggle_button(in_button)
        self._punch_out_toggle.set_toggle_button(out_button)

    def set_punch_in_button(self, in_button):
        self._punch_in_toggle.set_toggle_button(in_button)

    def set_punch_out_button(self, out_button):
        self._punch_out_toggle.set_toggle_button(out_button)

    def set_metronome_button(self, button):
        self._metronome_toggle.set_toggle_button(button)

    def set_arrangement_overdub_button(self, button):
        self._arrangement_overdub_toggle.set_toggle_button(button)

    def set_overdub_button(self, button):
        self._overdub_toggle.set_toggle_button(button)

    def set_tempo_control(self, control, fine_control=None):
        if self._tempo_control != control:
            self._tempo_control = control
            self._tempo_value.subject = control
        if self._tempo_fine_control != fine_control:
            self._tempo_fine_control = fine_control
            self._tempo_fine_value.subject = fine_control
            self._fine_tempo_needs_pickup = True
            self._prior_fine_tempo_value = -1

    def set_tempo_fine_control(self, fine_control):
        if self._tempo_fine_control != fine_control:
            self._tempo_fine_control = fine_control
            self._tempo_fine_value.subject = fine_control
            self._fine_tempo_needs_pickup = True
            self._prior_fine_tempo_value = -1

    def set_song_position_control(self, control):
        if self._song_position_control != control:
            self._song_position_control = control
            self._song_position_value.subject = control

    def update(self):
        super(TransportComponent, self).update()
        if self.is_enabled():
            self._update_tap_tempo_button()

    @subject_slot('value')
    def _ffwd_value_slot(self, value):
        self._ffwd_value(value)

    def _ffwd_value(self, value):
        if self._ffwd_button.is_momentary():
            self._ffwd_task.kill()
            if value:
                self._ffwd_task = self._tasks.add(partial(self._move_current_song_time, SEEK_SPEED))
        else:
            if self.is_enabled():
                self.song().current_song_time += 1

    @subject_slot('value')
    def _rwd_value_slot(self, value):
        self._rwd_value(value)

    def _rwd_value(self, value):
        if self._rwd_button.is_momentary():
            self._rwd_task.kill()
            if value:
                self._rwd_task = self._tasks.add(partial(self._move_current_song_time, -SEEK_SPEED))
        else:
            if self.is_enabled():
                song = self.song()
                song.current_song_time = max(0.0, song.current_song_time - 1)

    def _move_current_song_time(self, speed, delta):
        song = self.song()
        song.current_song_time = max(0.0, song.current_song_time + speed * delta)
        return Task.RUNNING

    @subject_slot('value')
    def _tap_tempo_value(self, value):
        if self.is_enabled():
            if not (value or self._tap_tempo_button.is_momentary()):
                if not self._end_undo_step_task.is_running:
                    self.song().begin_undo_step()
                self._end_undo_step_task.restart()
                self.song().tap_tempo()
            self._update_tap_tempo_button()

    def _update_tap_tempo_button(self):
        if self.is_enabled():
            if self._tap_tempo_button:
                self._tap_tempo_button.set_light(True)

    @subject_slot('value')
    def _tempo_value(self, value):
        if self.is_enabled():
            fraction = (TEMPO_TOP - TEMPO_BOTTOM) / 127.0
            self.song().tempo = fraction * value + TEMPO_BOTTOM

    @subject_slot('value')
    def _tempo_fine_value(self, value):
        if self.is_enabled():
            if self._fine_tempo_needs_pickup:
                if in_range(self._prior_fine_tempo_value, 0, 128):
                    range_max = max(value, self._prior_fine_tempo_value)
                    range_min = min(value, self._prior_fine_tempo_value)
                    if in_range(64, range_min, range_max + 1):
                        self._fine_tempo_needs_pickup = False
            else:
                difference = value - self._prior_fine_tempo_value
                ratio = 127.0 / TEMPO_FINE_RANGE
                new_tempo = clamp(self.song().tempo + old_div(difference, ratio), TEMPO_BOTTOM, TEMPO_TOP)
                self.song().tempo = new_tempo
        self._prior_fine_tempo_value = value

    @subject_slot('value')
    def _song_position_value(self, value):
        raise NotImplementedError