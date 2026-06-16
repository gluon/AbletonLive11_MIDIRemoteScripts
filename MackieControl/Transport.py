# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\Transport.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 25809 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from past.utils import old_div
from ableton.v2.base import move_current_song_time
from .MackieControlComponent import *

class Transport(MackieControlComponent):

    def __init__(self, main_script):
        MackieControlComponent.__init__(self, main_script)
        self._Transport__forward_button_down = False
        self._Transport____rewind_button_down = False
        self._Transport__zoom_button_down = False
        self._Transport__scrub_button_down = False
        self._Transport__cursor_left_is_down = False
        self._Transport__cursor_right_is_down = False
        self._Transport__cursor_up_is_down = False
        self._Transport__cursor_down_is_down = False
        self._Transport__cursor_repeat_delay = 0
        self._Transport__transport_repeat_delay = 0
        self._Transport____fast_forward_counter = 0
        self._Transport__fast___rewind_counter = 0
        self._Transport__jog_step_count_forward = 0
        self._Transport__jog_step_count_backwards = 0
        self._Transport__last_focussed_clip_play_state = CLIP_STATE_INVALID
        self.song().add_record_mode_listener(self._Transport__update_record_button_led)
        self.song().add_is_playing_listener(self._Transport__update_play_button_led)
        self.song().add_loop_listener(self._Transport__update_loop_button_led)
        self.song().add_punch_out_listener(self._Transport__update_punch_out_button_led)
        self.song().add_punch_in_listener(self._Transport__update_punch_in_button_led)
        self.song().add_can_jump_to_prev_cue_listener(self._Transport__update_prev_cue_button_led)
        self.song().add_can_jump_to_next_cue_listener(self._Transport__update_next_cue_button_led)
        self.application().view.add_is_view_visible_listener('Session', self._Transport__on_session_is_visible_changed)
        self.refresh_state()

    def destroy(self):
        self.song().remove_record_mode_listener(self._Transport__update_record_button_led)
        self.song().remove_is_playing_listener(self._Transport__update_play_button_led)
        self.song().remove_loop_listener(self._Transport__update_loop_button_led)
        self.song().remove_punch_out_listener(self._Transport__update_punch_out_button_led)
        self.song().remove_punch_in_listener(self._Transport__update_punch_in_button_led)
        self.song().remove_can_jump_to_prev_cue_listener(self._Transport__update_prev_cue_button_led)
        self.song().remove_can_jump_to_next_cue_listener(self._Transport__update_next_cue_button_led)
        self.application().view.remove_is_view_visible_listener('Session', self._Transport__on_session_is_visible_changed)
        for note in transport_control_switch_ids:
            self.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))

        for note in jog_wheel_switch_ids:
            self.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))

        for note in marker_control_switch_ids:
            self.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))

        MackieControlComponent.destroy(self)

    def refresh_state(self):
        self._Transport__update_play_button_led()
        self._Transport__update_record_button_led()
        self._Transport__update_prev_cue_button_led()
        self._Transport__update_next_cue_button_led()
        self._Transport__update_loop_button_led()
        self._Transport__update_punch_in_button_led()
        self._Transport__update_punch_out_button_led()
        self._Transport__forward_button_down = False
        self._Transport____rewind_button_down = False
        self._Transport__zoom_button_down = False
        self._Transport__scrub_button_down = False
        self._Transport__cursor_left_is_down = False
        self._Transport__cursor_right_is_down = False
        self._Transport__cursor_up_is_down = False
        self._Transport__cursor_down_is_down = False
        self._Transport__cursor_repeat_delay = 0
        self._Transport__transport_repeat_delay = 0
        self._Transport____fast_forward_counter = 0
        self._Transport__fast___rewind_counter = 0
        self._Transport__jog_step_count_forward = 0
        self._Transport__jog_step_count_backwards = 0
        self._Transport__last_focussed_clip_play_state = CLIP_STATE_INVALID
        self._Transport__update_forward_rewind_leds()
        self._Transport__update_zoom_button_led()
        self._Transport__update_scrub_button_led()

    def session_is_visible(self):
        return self.application().view.is_view_visible('Session')

    def selected_clip_slot(self):
        return self.song().view.highlighted_clip_slot

    def on_update_display_timer(self):
        if self._Transport__transport_repeat_delay > 2:
            if self.alt_is_pressed():
                base_acceleration = 1
            else:
                base_acceleration = self.song().signature_numerator
            if self.song().is_playing:
                base_acceleration *= 4
            if not (self._Transport__forward_button_down and self._Transport____rewind_button_down):
                if self._Transport__forward_button_down:
                    self._Transport____fast_forward_counter += 1
                    self._Transport__fast___rewind_counter -= 4
                    if not self.alt_is_pressed():
                        self._Transport__fast_forward(base_acceleration + max(1, old_div(self._Transport____fast_forward_counter, 4)))
                    else:
                        self._Transport__fast_forward(base_acceleration)
                if self._Transport____rewind_button_down:
                    self._Transport__fast___rewind_counter += 1
                    self._Transport____fast_forward_counter -= 4
                    if not self.alt_is_pressed():
                        self._Transport__rewind(base_acceleration + max(1, old_div(self._Transport__fast___rewind_counter, 4)))
                    else:
                        self._Transport__rewind(base_acceleration)
        else:
            self._Transport__transport_repeat_delay += 1
        if self._Transport__cursor_repeat_delay > 2:
            if self._Transport__cursor_left_is_down:
                self._Transport__on_cursor_left_pressed()
            if self._Transport__cursor_right_is_down:
                self._Transport__on_cursor_right_pressed()
            if self._Transport__cursor_up_is_down:
                self._Transport__on_cursor_up_pressed()
            if self._Transport__cursor_down_is_down:
                self._Transport__on_cursor_down_pressed()
        else:
            self._Transport__cursor_repeat_delay += 1
        if self.session_is_visible():
            self._Transport__update_zoom_led_in_session()

    def handle_marker_switch_ids(self, switch_id, value):
        if switch_id == SID_MARKER_FROM_PREV:
            if value == BUTTON_PRESSED:
                self._Transport__jump_to_prev_cue()
        else:
            if switch_id == SID_MARKER_FROM_NEXT:
                if value == BUTTON_PRESSED:
                    self._Transport__jump_to_next_cue()
            else:
                if switch_id == SID_MARKER_LOOP:
                    if value == BUTTON_PRESSED:
                        self._Transport__toggle_loop()
                else:
                    if switch_id == SID_MARKER_PI:
                        if value == BUTTON_PRESSED:
                            if self.control_is_pressed():
                                self._Transport__set_loopstart_from_cur_position()
                            else:
                                self._Transport__toggle_punch_in()
                    else:
                        if switch_id == SID_MARKER_PO:
                            if value == BUTTON_PRESSED:
                                if self.control_is_pressed():
                                    self._Transport__set_loopend_from_cur_position()
                                else:
                                    self._Transport__toggle_punch_out()
                        else:
                            if switch_id == SID_MARKER_HOME:
                                if value == BUTTON_PRESSED:
                                    self._Transport__goto_home()
                            else:
                                if switch_id == SID_MARKER_END:
                                    if value == BUTTON_PRESSED:
                                        self._Transport__goto_end()

    def handle_transport_switch_ids(self, switch_id, value):
        if switch_id == SID_TRANSPORT_REWIND:
            if value == BUTTON_PRESSED:
                self._Transport__rewind()
                self._Transport____rewind_button_down = True
            else:
                if value == BUTTON_RELEASED:
                    self._Transport____rewind_button_down = False
                    self._Transport__fast___rewind_counter = 0
            self._Transport__update_forward_rewind_leds()
        else:
            if switch_id == SID_TRANSPORT_FAST_FORWARD:
                if value == BUTTON_PRESSED:
                    self._Transport__fast_forward()
                    self._Transport__forward_button_down = True
                else:
                    if value == BUTTON_RELEASED:
                        self._Transport__forward_button_down = False
                        self._Transport____fast_forward_counter = 0
                self._Transport__update_forward_rewind_leds()
            else:
                if switch_id == SID_TRANSPORT_STOP:
                    if value == BUTTON_PRESSED:
                        self._Transport__stop_song()
                else:
                    if switch_id == SID_TRANSPORT_PLAY:
                        if value == BUTTON_PRESSED:
                            self._Transport__start_song()
                    else:
                        if switch_id == SID_TRANSPORT_RECORD:
                            if value == BUTTON_PRESSED:
                                self._Transport__toggle_record()

    def handle_jog_wheel_rotation(self, value):
        backwards = value >= 64
        if self.control_is_pressed():
            if self.alt_is_pressed():
                step = 0.1
            else:
                step = 1.0
            if backwards:
                amount = -(value - 64)
            else:
                amount = value
            tempo = max(20, min(999, self.song().tempo + amount * step))
            self.song().tempo = tempo
        else:
            if self.session_is_visible():
                num_steps_per_session_scroll = 4
                if backwards:
                    self._Transport__jog_step_count_backwards += 1
                    if self._Transport__jog_step_count_backwards >= num_steps_per_session_scroll:
                        self._Transport__jog_step_count_backwards = 0
                        step = -1
                    else:
                        step = 0
                else:
                    self._Transport__jog_step_count_forward += 1
                    if self._Transport__jog_step_count_forward >= num_steps_per_session_scroll:
                        self._Transport__jog_step_count_forward = 0
                        step = 1
                    else:
                        step = 0
                if step:
                    new_index = list(self.song().scenes).index(self.song().view.selected_scene) + step
                    new_index = min(len(self.song().scenes) - 1, max(0, new_index))
                    self.song().view.selected_scene = self.song().scenes[new_index]
            else:
                if backwards:
                    step = max(1.0, (value - 64) / 2.0)
                else:
                    step = max(1.0, value / 2.0)
                if self.song().is_playing:
                    step *= 4.0
                if self.alt_is_pressed():
                    step /= 4.0
                move_current_song_time((self.song()),
                  (-step if backwards else step), truncate_to_beat=False)

    def handle_jog_wheel_switch_ids(self, switch_id, value):
        if switch_id == SID_JOG_CURSOR_UP:
            if value == BUTTON_PRESSED:
                self._Transport__cursor_up_is_down = True
                self._Transport__cursor_repeat_delay = 0
                self._Transport__on_cursor_up_pressed()
            else:
                if value == BUTTON_RELEASED:
                    self._Transport__cursor_up_is_down = False
        else:
            if switch_id == SID_JOG_CURSOR_DOWN:
                if value == BUTTON_PRESSED:
                    self._Transport__cursor_down_is_down = True
                    self._Transport__cursor_repeat_delay = 0
                    self._Transport__on_cursor_down_pressed()
                else:
                    if value == BUTTON_RELEASED:
                        self._Transport__cursor_down_is_down = False
            else:
                if switch_id == SID_JOG_CURSOR_LEFT:
                    if value == BUTTON_PRESSED:
                        self._Transport__cursor_left_is_down = True
                        self._Transport__cursor_repeat_delay = 0
                        self._Transport__on_cursor_left_pressed()
                    else:
                        if value == BUTTON_RELEASED:
                            self._Transport__cursor_left_is_down = False
                else:
                    if switch_id == SID_JOG_CURSOR_RIGHT:
                        if value == BUTTON_PRESSED:
                            self._Transport__cursor_right_is_down = True
                            self._Transport__cursor_repeat_delay = 0
                            self._Transport__on_cursor_right_pressed()
                        else:
                            if value == BUTTON_RELEASED:
                                self._Transport__cursor_right_is_down = False
                    else:
                        if switch_id == SID_JOG_ZOOM:
                            if value == BUTTON_PRESSED:
                                if self.session_is_visible():
                                    if self.selected_clip_slot():
                                        if self.alt_is_pressed():
                                            self.selected_clip_slot().has_stop_button = not self.selected_clip_slot().has_stop_button
                                        else:
                                            if self.option_is_pressed():
                                                self.selected_clip_slot().stop()
                                            else:
                                                self.selected_clip_slot().fire()
                                else:
                                    self._Transport__zoom_button_down = not self._Transport__zoom_button_down
                                    self._Transport__update_zoom_button_led()
                        else:
                            if not switch_id == SID_JOG_SCRUB or value == BUTTON_PRESSED and self.session_is_visible():
                                if self.option_is_pressed():
                                    self.song().stop_all_clips()
                                else:
                                    self.song().view.selected_scene.fire_as_selected()
                            else:
                                self._Transport__scrub_button_down = not self._Transport__scrub_button_down
                                self._Transport__update_scrub_button_led()

    def __on_cursor_up_pressed(self):
        nav = Live.Application.Application.View.NavDirection
        if self._Transport__zoom_button_down:
            self.application().view.zoom_view(nav.up, '', self.alt_is_pressed())
        else:
            self.application().view.scroll_view(nav.up, '', self.alt_is_pressed())

    def __on_cursor_down_pressed(self):
        nav = Live.Application.Application.View.NavDirection
        if self._Transport__zoom_button_down:
            self.application().view.zoom_view(nav.down, '', self.alt_is_pressed())
        else:
            self.application().view.scroll_view(nav.down, '', self.alt_is_pressed())

    def __on_cursor_left_pressed(self):
        nav = Live.Application.Application.View.NavDirection
        if self._Transport__zoom_button_down:
            self.application().view.zoom_view(nav.left, '', self.alt_is_pressed())
        else:
            self.application().view.scroll_view(nav.left, '', self.alt_is_pressed())

    def __on_cursor_right_pressed(self):
        nav = Live.Application.Application.View.NavDirection
        if self._Transport__zoom_button_down:
            self.application().view.zoom_view(nav.right, '', self.alt_is_pressed())
        else:
            self.application().view.scroll_view(nav.right, '', self.alt_is_pressed())

    def __toggle_record(self):
        self.song().record_mode = not self.song().record_mode

    def __rewind(self, acceleration=1):
        beats = acceleration
        self.song().jump_by(-beats)

    def __fast_forward(self, acceleration=1):
        beats = acceleration
        self.song().jump_by(beats)

    def __stop_song(self):
        self.song().stop_playing()

    def __start_song(self):
        if self.shift_is_pressed():
            if not self.song().is_playing:
                self.song().continue_playing()
            else:
                self.song().stop_playing()
        else:
            if self.control_is_pressed():
                self.song().play_selection()
            else:
                self.song().start_playing()

    def __toggle_loop(self):
        self.song().loop = not self.song().loop

    def __toggle_punch_in(self):
        self.song().punch_in = not self.song().punch_in

    def __toggle_punch_out(self):
        self.song().punch_out = not self.song().punch_out

    def __jump_to_prev_cue(self):
        self.song().jump_to_prev_cue()

    def __jump_to_next_cue(self):
        self.song().jump_to_next_cue()

    def __set_loopstart_from_cur_position(self):
        if self.song().current_song_time < self.song().loop_start + self.song().loop_length:
            old_loop_start = self.song().loop_start
            self.song().loop_start = self.song().current_song_time
            self.song().loop_length += old_loop_start - self.song().loop_start

    def __set_loopend_from_cur_position(self):
        if self.song().current_song_time > self.song().loop_start:
            self.song().loop_length = self.song().current_song_time - self.song().loop_start

    def __goto_home(self):
        self.song().current_song_time = 0

    def __goto_end(self):
        self.song().current_song_time = self.song().last_event_time

    def __on_session_is_visible_changed(self):
        self._Transport__last_focussed_clip_play_state = CLIP_STATE_INVALID
        self._Transport__update_zoom_button_led()
        self._Transport__update_scrub_button_led()

    def __update_zoom_led_in_session(self):
        if self.session_is_visible():
            clip_slot = self.selected_clip_slot()
            if clip_slot and clip_slot.clip:
                if clip_slot.clip.is_triggered:
                    state = CLIP_TRIGGERED
                else:
                    if clip_slot.clip.is_playing:
                        state = CLIP_PLAYING
                    else:
                        state = CLIP_STOPPED
            else:
                state = CLIP_STOPPED
            if state != self._Transport__last_focussed_clip_play_state:
                self._Transport__last_focussed_clip_play_state = state
                if state == CLIP_PLAYING:
                    self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_ON))
                else:
                    if state == CLIP_TRIGGERED:
                        self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_BLINKING))
                    else:
                        self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_OFF))

    def __update_forward_rewind_leds(self):
        if self._Transport__forward_button_down:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_FAST_FORWARD, BUTTON_STATE_ON))
            self._Transport__transport_repeat_delay = 0
        else:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_FAST_FORWARD, BUTTON_STATE_OFF))
        if self._Transport____rewind_button_down:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_REWIND, BUTTON_STATE_ON))
            self._Transport__transport_repeat_delay = 0
        else:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_REWIND, BUTTON_STATE_OFF))

    def __update_zoom_button_led(self):
        if self.session_is_visible():
            self._Transport__update_zoom_led_in_session()
        else:
            if self._Transport__zoom_button_down:
                self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_ON))
            else:
                self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_OFF))

    def __update_scrub_button_led(self):
        if self._Transport__scrub_button_down and not self.session_is_visible():
            self.send_midi((NOTE_ON_STATUS, SID_JOG_SCRUB, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_JOG_SCRUB, BUTTON_STATE_OFF))

    def __update_play_button_led(self):
        if self.song().is_playing:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_PLAY, BUTTON_STATE_ON))
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_STOP, BUTTON_STATE_OFF))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_PLAY, BUTTON_STATE_OFF))
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_STOP, BUTTON_STATE_ON))

    def __update_record_button_led(self):
        if self.song().record_mode:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_RECORD, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_RECORD, BUTTON_STATE_OFF))

    def __update_prev_cue_button_led(self):
        if self.song().can_jump_to_prev_cue:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_PREV, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_PREV, BUTTON_STATE_OFF))

    def __update_next_cue_button_led(self):
        if self.song().can_jump_to_next_cue:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_NEXT, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_NEXT, BUTTON_STATE_OFF))

    def __update_loop_button_led(self):
        if self.song().loop:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_LOOP, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_LOOP, BUTTON_STATE_OFF))

    def __update_punch_in_button_led(self):
        if self.song().punch_in:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_PI, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_PI, BUTTON_STATE_OFF))

    def __update_punch_out_button_led(self):
        if self.song().punch_out:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_PO, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_PO, BUTTON_STATE_OFF))