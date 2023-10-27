# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Tranzport\Tranzport.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 47286 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import object, range, str
from past.utils import old_div
from itertools import chain
import Live
from ableton.v2.base import move_current_song_time
from .consts import *

class Tranzport(object):

    def __init__(self, c_instance):
        self._Tranzport__c_instance = c_instance
        self._Tranzport__current_track = self.song().view.selected_track
        self._Tranzport__last_message = ()
        self.song().view.add_selected_scene_listener(self._Tranzport__on_selected_scene_changed)
        self.song().add_record_mode_listener(self._Tranzport__set_record_mode_led)
        self.song().view.add_selected_track_listener(self._Tranzport__on_selected_track_changed)
        self.song().add_loop_listener(self._Tranzport__set_loop_led)
        self.song().add_tracks_listener(self._Tranzport__on_tracks_changed)
        self.application().view.add_is_view_visible_listener('Session', self._Tranzport__on_view_changed)
        for i in chain(self.song().tracks, self.song().return_tracks):
            i.add_solo_listener(self._Tranzport__set_any_solo_led)

        if self._Tranzport__current_track in self.song().visible_tracks:
            if self._Tranzport__current_track.can_be_armed:
                self._Tranzport__current_track.add_arm_listener(self._Tranzport__set_track_armed_led)
        if self._Tranzport__current_track in chain(self.song().visible_tracks, self.song().return_tracks):
            self._Tranzport__current_track.add_mute_listener(self._Tranzport__set_track_muted_led)
            self._Tranzport__current_track.add_solo_listener(self._Tranzport__set_track_soloed_led)
            self._Tranzport__current_track.add_name_listener(self._Tranzport__current_track_name_changed)
        self._Tranzport__sends_in_current_track = len(self._Tranzport__current_track.mixer_device.sends)
        self._Tranzport__current_send_index = 0
        self._Tranzport__rewind_pressed = False
        self._Tranzport__ffwd_pressed = False
        self._Tranzport__shift_pressed = False
        self._Tranzport__nexttrack_pressed = False
        self._Tranzport__prevtrack_pressed = False
        self._Tranzport__nextmarker_pressed = False
        self._Tranzport__prevmarker_pressed = False
        self._Tranzport__showing_page_list = False
        self._Tranzport__selected_page = 0
        self._Tranzport__spooling_factor = 1.0
        self._Tranzport__timer_count = 0
        self._Tranzport__display_line_one = ()
        self._Tranzport__display_line_two = ()
        self._Tranzport__last_line_one = ()
        self._Tranzport__last_line_two = ()
        self.send_midi(TRANZ_NATIVE_MODE)
        self._Tranzport__display_line_one = self._Tranzport__translate_string('    Ableton Live    ')
        self._Tranzport__display_line_two = self._Tranzport__translate_string('                    ')

    def application(self):
        return Live.Application.get_application()

    def song(self):
        return self._Tranzport__c_instance.song()

    def disconnect(self):
        NOTE_OFF_STATUS = 128
        TRANZ_REC = 95
        TRANZ_ARM_TRACK = 0
        TRANZ_MUTE_TRACK = 16
        TRANZ_SOLO_TRACK = 8
        TRANZ_ANY_SOLO = 115
        TRANZ_LOOP = 86
        TRANZ_PUNCH = 120
        SYSEX_START = (240, 0, 1, 64, 16, 0)
        SYSEX_END = (247, )
        CLEAR_LINE = (32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
                      32, 32, 32, 32)
        LED_OFF = 0
        self.send_midi(SYSEX_START + (0, ) + CLEAR_LINE + CLEAR_LINE + SYSEX_END)
        self.song().view.remove_selected_scene_listener(self._Tranzport__on_selected_scene_changed)
        self.song().remove_record_mode_listener(self._Tranzport__set_record_mode_led)
        self.song().view.remove_selected_track_listener(self._Tranzport__on_selected_track_changed)
        self.song().remove_loop_listener(self._Tranzport__set_loop_led)
        self.song().remove_tracks_listener(self._Tranzport__on_tracks_changed)
        if Live:
            self.application().view.remove_is_view_visible_listener('Session', self._Tranzport__on_view_changed)
        for i in chain(self.song().tracks, self.song().return_tracks):
            i.remove_solo_listener(self._Tranzport__set_any_solo_led)

        self.send_midi((NOTE_OFF_STATUS, TRANZ_REC, LED_OFF))
        self.send_midi((NOTE_OFF_STATUS, TRANZ_ARM_TRACK, LED_OFF))
        self.send_midi((NOTE_OFF_STATUS, TRANZ_MUTE_TRACK, LED_OFF))
        self.send_midi((NOTE_OFF_STATUS, TRANZ_SOLO_TRACK, LED_OFF))
        self.send_midi((NOTE_OFF_STATUS, TRANZ_ANY_SOLO, LED_OFF))
        self.send_midi((NOTE_OFF_STATUS, TRANZ_LOOP, LED_OFF))
        self.send_midi((NOTE_OFF_STATUS, TRANZ_PUNCH, LED_OFF))
        if (list(self.song().visible_tracks) + list(self.song().return_tracks)).count(self._Tranzport__current_track) > 0:
            self._Tranzport__current_track.remove_mute_listener(self._Tranzport__set_track_muted_led)
            self._Tranzport__current_track.remove_solo_listener(self._Tranzport__set_track_soloed_led)
            self._Tranzport__current_track.remove_name_listener(self._Tranzport__current_track_name_changed)
            if self._Tranzport__current_track in self.song().visible_tracks:
                if self._Tranzport__current_track.can_be_armed:
                    self._Tranzport__current_track.remove_arm_listener(self._Tranzport__set_track_armed_led)

    def suggest_input_port(self):
        return 'TranzPort'

    def suggest_output_port(self):
        return 'TranzPort'

    def suggest_map_mode(self, *_):
        return Live.MidiMap.MapMode.relative_signed_bit

    def can_lock_to_devices(self):
        return False

    def connect_script_instances(self, instanciated_scripts):
        pass

    def request_rebuild_midi_map(self):
        self._Tranzport__c_instance.request_rebuild_midi_map()

    def send_midi(self, midi_event_bytes):
        self._Tranzport__c_instance.send_midi(midi_event_bytes)

    def refresh_state(self):
        self._Tranzport__last_line_one = ()
        self._Tranzport__last_line_two = ()
        if self._Tranzport__timer_count >= 20:
            self._Tranzport__show_track_and_scene()
        self._Tranzport__set_record_mode_led()
        self._Tranzport__set_track_armed_led()
        self._Tranzport__set_track_muted_led()
        self._Tranzport__set_track_soloed_led()
        self._Tranzport__set_any_solo_led()
        self._Tranzport__set_loop_led()

    def build_midi_map(self, midi_map_handle):
        script_handle = self._Tranzport__c_instance.handle()
        for i in range(NUM_NOTES):
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, 0, i)

        for channel in range(NUM_CHANNELS):
            for cc_no in range(NUM_CC_NO):
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, cc_no)

    def update_display(self):
        if self._Tranzport__timer_count < 21:
            self._Tranzport__timer_count = self._Tranzport__timer_count + 1
        if self._Tranzport__timer_count == 10:
            self._Tranzport__show_pos_and_tempo()
        if self._Tranzport__timer_count == 20:
            self._Tranzport__on_selected_track_changed()
        if self._Tranzport__ffwd_pressed or self._Tranzport__rewind_pressed:
            self._Tranzport__spooling_factor = self._Tranzport__spooling_factor + 0.2
            if self._Tranzport__ffwd_pressed:
                self.song().jump_by(1 * self._Tranzport__spooling_factor)
            if self._Tranzport__rewind_pressed:
                self.song().jump_by(-1 * self._Tranzport__spooling_factor)
        if not self._Tranzport__display_line_one == self._Tranzport__last_line_one:
            self.send_midi(SYSEX_START + (0, ) + self._Tranzport__display_line_one + SYSEX_END)
            self._Tranzport__last_line_one = self._Tranzport__display_line_one
        self._Tranzport__show_selected_page()
        if not self._Tranzport__display_line_two == self._Tranzport__last_line_two:
            self.send_midi(SYSEX_START + (20, ) + self._Tranzport__display_line_two + SYSEX_END)
            self._Tranzport__last_line_two = self._Tranzport__display_line_two

    def receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS or midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            note = midi_bytes[1]
            velocity = midi_bytes[2]
            if note == TRANZ_SHIFT:
                self._Tranzport__shift_status_changed(velocity)
            else:
                if note in TRANZ_TRANS_SECTION:
                    self._Tranzport__on_transport_button_pressed(note, velocity)
                else:
                    if note in TRANZ_TRACK_SECTION:
                        self._Tranzport__on_track_button_pressed(note, velocity)
                    else:
                        if note in TRANZ_LOOP_SECTION:
                            self._Tranzport__on_loop_button_pressed(note, velocity)
                        else:
                            if note in TRANZ_CUE_SECTION:
                                self._Tranzport__on_cue_button_pressed(note, velocity)
                            else:
                                if note == TRANZ_UNDO:
                                    self._Tranzport__on_undo_pressed(velocity)
        else:
            if midi_bytes[0] & 240 == CC_STATUS:
                cc_no = midi_bytes[1]
                cc_value = midi_bytes[2]
                if midi_bytes[0] == 176:
                    if cc_no == 60:
                        self._Tranzport__on_jogdial_changed(cc_value)

    def __on_transport_button_pressed(self, button, status):
        if button == TRANZ_PLAY:
            if status > 0:
                if not self._Tranzport__shift_pressed:
                    self.song().is_playing = True
                else:
                    self.song().continue_playing()
        else:
            if button == TRANZ_STOP:
                if status > 0:
                    self.song().is_playing = False
            else:
                if button == TRANZ_REC:
                    if status > 0:
                        self.song().record_mode = self._Tranzport__shift_pressed or not self.song().record_mode
                    else:
                        pass
                else:
                    if button == TRANZ_FFWD:
                        if status > 0:
                            if self._Tranzport__shift_pressed:
                                self.song().jump_by(self.song().signature_denominator)
                            else:
                                self.song().jump_by(1)
                                self._Tranzport__ffwd_pressed = True
                        else:
                            self._Tranzport__ffwd_pressed = False
                            self._Tranzport__spooling_factor = 1.0
                    else:
                        if button == TRANZ_RWD:
                            if status > 0:
                                if self._Tranzport__shift_pressed:
                                    self.song().jump_by(-1 * self.song().signature_denominator)
                                else:
                                    self.song().jump_by(-1)
                                    self._Tranzport__rewind_pressed = True
                            else:
                                self._Tranzport__rewind_pressed = False
                                self._Tranzport__spooling_factor = 1.0

    def __on_track_button_pressed(self, button, status):
        all_tracks = list(tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,))
        index = all_tracks.index(self._Tranzport__current_track)
        if button == TRANZ_PREV_TRACK:
            if status > 0:
                if self._Tranzport__shift_pressed:
                    self._Tranzport__handle_page_select(-1)
                else:
                    self._Tranzport__prevtrack_pressed = True
                    if index > 0:
                        index = index - 1
                        self.song().view.selected_track = all_tracks[index]
            else:
                self._Tranzport__prevtrack_pressed = False
        else:
            if button == TRANZ_NEXT_TRACK:
                if status > 0:
                    if self._Tranzport__shift_pressed:
                        self._Tranzport__handle_page_select(1)
                    else:
                        self._Tranzport__nexttrack_pressed = True
                        if index < len(all_tracks) - 1:
                            index = index + 1
                            self.song().view.selected_track = all_tracks[index]
                else:
                    self._Tranzport__nexttrack_pressed = False
            else:
                if button == TRANZ_ARM_TRACK:
                    if not status > 0 or list(self.song().visible_tracks).count(self._Tranzport__current_track) > 0:
                        if not self.song().exclusive_arm or self._Tranzport__shift_pressed:
                            if not (self._Tranzport__shift_pressed and self.song().exclusive_arm):
                                for i in self.song().tracks:
                                    if i != self._Tranzport__current_track:
                                        if i.can_be_armed:
                                            i.arm = False

                            if not self._Tranzport__current_track or self._Tranzport__current_track.can_be_armed:
                                self._Tranzport__current_track.arm = not self._Tranzport__current_track.arm
                else:
                    if button == TRANZ_MUTE_TRACK:
                        if not status > 0 or (list(self.song().visible_tracks) + list(self.song().return_tracks)).count(self._Tranzport__current_track) > 0:
                            if not self._Tranzport__shift_pressed:
                                self._Tranzport__current_track.mute = not self._Tranzport__current_track.mute
                            else:
                                for i in chain(self.song().tracks, self.song().return_tracks):
                                    i.mute = False

                    else:
                        if button == TRANZ_SOLO_TRACK:
                            if status > 0:
                                if (list(self.song().visible_tracks) + list(self.song().return_tracks)).count(self._Tranzport__current_track) > 0:
                                    if not self.song().exclusive_solo or self._Tranzport__shift_pressed:
                                        if not (self._Tranzport__shift_pressed and self.song().exclusive_solo):
                                            for i in chain(self.song().tracks, self.song().return_tracks):
                                                if i.solo:
                                                    if not i == self._Tranzport__current_track:
                                                        i.solo = False

                                        if self._Tranzport__current_track:
                                            self._Tranzport__current_track.solo = not self._Tranzport__current_track.solo

    def __on_loop_button_pressed(self, button, status):
        current_pos = self.song().current_song_time
        loop_start = self.song().loop_start
        loop_end = loop_start + self.song().loop_length
        if status > 0:
            if button == TRANZ_LOOP:
                if not self._Tranzport__shift_pressed:
                    self.song().loop = not self.song().loop
                else:
                    if self.application().view.is_view_visible('Session'):
                        self.application().view.show_view('Arranger')
                    else:
                        if self.application().view.is_view_visible('Arranger'):
                            self.application().view.show_view('Session')
            else:
                if button == TRANZ_PUNCH_IN:
                    if not self._Tranzport__shift_pressed:
                        self.song().punch_in = not self.song().punch_in
                    else:
                        if current_pos < loop_end:
                            self.song().loop_start = current_pos
                            self.song().loop_length = loop_end - current_pos
                else:
                    if button == TRANZ_PUNCH_OUT:
                        if not self._Tranzport__shift_pressed:
                            self.song().punch_out = not self.song().punch_out
                        else:
                            if current_pos > loop_start:
                                self.song().loop_length = current_pos - loop_start
                    else:
                        if button == TRANZ_PUNCH:
                            if self.application().view.is_view_visible('Session'):
                                current_slot = self.song().view.highlighted_clip_slot
                                if not self._Tranzport__shift_pressed or list(self.song().visible_tracks).count(self._Tranzport__current_track) > 0:
                                    current_slot.fire()
                                else:
                                    self.song().view.selected_scene.fire_as_selected()

    def __on_cue_button_pressed(self, button, status):
        if status > 0:
            if button == TRANZ_PREV_CUE:
                if not self._Tranzport__shift_pressed:
                    self._Tranzport__prevmarker_pressed = True
                    if self.song().can_jump_to_prev_cue:
                        self.song().jump_to_prev_cue()
                else:
                    self.song().current_song_time = 0
            else:
                if button == TRANZ_ADD_CUE:
                    if not self._Tranzport__shift_pressed:
                        self.song().set_or_delete_cue()
                else:
                    if button == TRANZ_NEXT_CUE:
                        if not self._Tranzport__shift_pressed:
                            self._Tranzport__nextmarker_pressed = True
                            if self.song().can_jump_to_next_cue:
                                self.song().jump_to_next_cue()
                        else:
                            self.song().current_song_time = self.song().last_event_time
        else:
            if status == 0:
                if button == TRANZ_PREV_CUE:
                    self._Tranzport__prevmarker_pressed = False
                else:
                    if button == TRANZ_NEXT_CUE:
                        self._Tranzport__nextmarker_pressed = False

    def __on_jogdial_changed(self, value):
        neg_value = value - 64
        all_tracks = list(tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,))
        index = all_tracks.index(self._Tranzport__current_track)
        if value in range(1, 64):
            if not self._Tranzport__shift_pressed:
                if self._Tranzport__prevtrack_pressed or self._Tranzport__nexttrack_pressed:
                    if index < len(all_tracks) - 1:
                        index = index + 1
                        self.song().view.selected_track = all_tracks[index]
                else:
                    if self._Tranzport__prevmarker_pressed or self._Tranzport__nextmarker_pressed:
                        if self.song().can_jump_to_next_cue:
                            self.song().jump_to_next_cue()
                    else:
                        if self._Tranzport__selected_page == 0:
                            if self.application().view.is_view_visible('Session'):
                                index = list(self.song().scenes).index(self.song().view.selected_scene)
                                if index < len(self.song().scenes) - 1:
                                    index = index + 1
                                    self.song().view.selected_scene = self.song().scenes[index]
                            else:
                                move_current_song_time(self.song(), value)
                        else:
                            if self._Tranzport__selected_page == 1:
                                if self._Tranzport__current_track.mixer_device.volume.value <= self._Tranzport__current_track.mixer_device.volume.max - 0.01 * value:
                                    self._Tranzport__current_track.mixer_device.volume.value = self._Tranzport__current_track.mixer_device.volume.value + 0.01 * value
                                else:
                                    self._Tranzport__current_track.mixer_device.volume.value = self._Tranzport__current_track.mixer_device.volume.max
                            else:
                                if self._Tranzport__selected_page == 2:
                                    self.song().loop_start = self.song().loop_start + value
                                else:
                                    if self._Tranzport__selected_page == 3:
                                        if self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].value <= self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].max - 0.01 * value:
                                            self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].value = self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].value + 0.01 * value
                                        else:
                                            self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].value = self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].max
            else:
                if self._Tranzport__selected_page == 0:
                    self.song().tempo = self.song().tempo + 0.1 * value
                else:
                    if self._Tranzport__selected_page == 1:
                        if self._Tranzport__current_track.mixer_device.panning.value <= self._Tranzport__current_track.mixer_device.panning.max - 0.02 * value:
                            self._Tranzport__current_track.mixer_device.panning.value = self._Tranzport__current_track.mixer_device.panning.value + 0.02 * value
                        else:
                            self._Tranzport__current_track.mixer_device.panning.value = self._Tranzport__current_track.mixer_device.panning.max
                    else:
                        if self._Tranzport__selected_page == 2:
                            self.song().loop_length = self.song().loop_length + value
                        else:
                            if self._Tranzport__selected_page == 3:
                                if self._Tranzport__current_send_index < len(self._Tranzport__current_track.mixer_device.sends) - 1:
                                    self._Tranzport__current_send_index = self._Tranzport__current_send_index + 1
                                else:
                                    self._Tranzport__current_send_index = len(self._Tranzport__current_track.mixer_device.sends) - 1
        else:
            if value in range(65, 128):
                if not self._Tranzport__shift_pressed:
                    if self._Tranzport__prevtrack_pressed or self._Tranzport__nexttrack_pressed:
                        if index > 0:
                            index = index - 1
                            self.song().view.selected_track = all_tracks[index]
                    else:
                        if self._Tranzport__prevmarker_pressed or self._Tranzport__nextmarker_pressed:
                            if self.song().can_jump_to_prev_cue:
                                self.song().jump_to_prev_cue()
                        else:
                            if self._Tranzport__selected_page == 0:
                                if self.application().view.is_view_visible('Session'):
                                    index = list(self.song().scenes).index(self.song().view.selected_scene)
                                    if index > 0:
                                        index = index - 1
                                    self.song().view.selected_scene = self.song().scenes[index]
                                else:
                                    move_current_song_time(self.song(), -1 * neg_value)
                            else:
                                if self._Tranzport__selected_page == 1:
                                    if self._Tranzport__current_track.mixer_device.volume.value >= self._Tranzport__current_track.mixer_device.volume.min + 0.01 * neg_value:
                                        self._Tranzport__current_track.mixer_device.volume.value = self._Tranzport__current_track.mixer_device.volume.value - 0.01 * neg_value
                                    else:
                                        self._Tranzport__current_track.mixer_device.volume.value = self._Tranzport__current_track.mixer_device.volume.min
                                else:
                                    if self._Tranzport__selected_page == 2:
                                        if self.song().loop_start >= neg_value:
                                            self.song().loop_start = self.song().loop_start - neg_value
                                    else:
                                        if self._Tranzport__selected_page == 3:
                                            if self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].value >= self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].min + 0.01 * neg_value:
                                                self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].value = self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].value - 0.01 * neg_value
                                            else:
                                                self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].value = self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index].min
                else:
                    if self._Tranzport__selected_page == 0:
                        self.song().tempo = self.song().tempo - 0.1 * neg_value
                    else:
                        if self._Tranzport__selected_page == 1:
                            if self._Tranzport__current_track.mixer_device.panning.value >= self._Tranzport__current_track.mixer_device.panning.min + 0.02 * neg_value:
                                self._Tranzport__current_track.mixer_device.panning.value = self._Tranzport__current_track.mixer_device.panning.value - 0.02 * neg_value
                            else:
                                self._Tranzport__current_track.mixer_device.panning.value = self._Tranzport__current_track.mixer_device.panning.min
                        else:
                            if self._Tranzport__selected_page == 2:
                                if self.song().loop_length > neg_value:
                                    self.song().loop_length = self.song().loop_length - neg_value
                            else:
                                if self._Tranzport__selected_page == 3:
                                    if self._Tranzport__current_send_index > 0:
                                        self._Tranzport__current_send_index = self._Tranzport__current_send_index - 1
                                    else:
                                        self._Tranzport__current_send_index = 0

    def __on_undo_pressed(self, status):
        if not status > 0 or (self._Tranzport__shift_pressed or self.song()).can_undo:
            self.song().undo()
        else:
            if self.song().can_redo:
                self.song().redo()

    def __on_selected_scene_changed(self):
        if self.application().view.is_view_visible('Session'):
            self._Tranzport__show_track_and_scene()

    def __on_current_song_time_changed(self):
        if self._Tranzport__selected_page == 0:
            self._Tranzport__show_selected_page()

    def __on_current_song_tempo_changed(self):
        if self._Tranzport__selected_page == 0:
            self._Tranzport__show_selected_page()

    def __on_current_track_volume_changed(self):
        if self._Tranzport__selected_page == 1:
            self._Tranzport__show_selected_page()

    def __on_current_track_panning_changed(self):
        if self._Tranzport__selected_page == 1:
            self._Tranzport__show_selected_page()

    def __on_song_loop_start_changed(self):
        if self._Tranzport__selected_page == 2:
            self._Tranzport__show_selected_page()

    def __on_song_loop_length_changed(self):
        if self._Tranzport__selected_page == 2:
            self._Tranzport__show_selected_page()

    def __on_view_changed(self):
        self._Tranzport__show_track_and_scene()
        self._Tranzport__show_selected_page()

    def __on_tracks_changed(self):
        for i in chain(self.song().tracks, self.song().return_tracks):
            if not i.solo_has_listener(self._Tranzport__set_any_solo_led):
                i.add_solo_listener(self._Tranzport__set_any_solo_led)

    def __show_track_and_scene(self):
        line = ()
        if self.application().view.is_view_visible('Session'):
            line = self._Tranzport__translate_string(self._Tranzport__bring_string_to_length(self._Tranzport__current_track.name, 11))
            line = line + self._Tranzport__translate_string('  Scene%2d' % (list(self.song().scenes).index(self.song().view.selected_scene) + 1))
        else:
            if self.application().view.is_view_visible('Arranger'):
                line = self._Tranzport__translate_string(self._Tranzport__bring_string_to_length(self._Tranzport__current_track.name, 20))
        self._Tranzport__display_line_one = line

    def __show_selected_page--- This code section failed: ---

 L. 837         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _Tranzport__showing_page_list
                4  POP_JUMP_IF_TRUE     94  'to 94'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _Tranzport__timer_count
               10  LOAD_CONST               20
               12  COMPARE_OP               >
               14  POP_JUMP_IF_FALSE    94  'to 94'

 L. 838        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _Tranzport__selected_page
               20  STORE_FAST               'index'

 L. 840        22  LOAD_FAST                'index'
               24  LOAD_CONST               0
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L. 841        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _Tranzport__show_pos_and_tempo
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  POP_TOP          
               38  JUMP_FORWARD        108  'to 108'
             40_0  COME_FROM            28  '28'

 L. 842        40  LOAD_FAST                'index'
               42  LOAD_CONST               1
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    58  'to 58'

 L. 843        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _Tranzport__show_vol_and_pan
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  POP_TOP          
               56  JUMP_FORWARD        108  'to 108'
             58_0  COME_FROM            46  '46'

 L. 844        58  LOAD_FAST                'index'
               60  LOAD_CONST               2
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    76  'to 76'

 L. 845        66  LOAD_FAST                'self'
               68  LOAD_METHOD              _Tranzport__show_loop_settings
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  POP_TOP          
               74  JUMP_FORWARD        108  'to 108'
             76_0  COME_FROM            64  '64'

 L. 846        76  LOAD_FAST                'index'
               78  LOAD_CONST               3
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   108  'to 108'

 L. 847        84  LOAD_FAST                'self'
               86  LOAD_METHOD              _Tranzport__show_send_settings
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  POP_TOP          
               92  JUMP_FORWARD        108  'to 108'
             94_0  COME_FROM            14  '14'
             94_1  COME_FROM             4  '4'

 L. 849        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _Tranzport__showing_page_list
               98  POP_JUMP_IF_FALSE   108  'to 108'

 L. 850       100  LOAD_FAST                'self'
              102  LOAD_METHOD              _Tranzport__show_page_select
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  POP_TOP          
            108_0  COME_FROM            98  '98'
            108_1  COME_FROM            92  '92'
            108_2  COME_FROM            82  '82'
            108_3  COME_FROM            74  '74'
            108_4  COME_FROM            56  '56'
            108_5  COME_FROM            38  '38'

Parse error at or near `COME_FROM' instruction at offset 108_4

    def __show_pos_and_tempo(self):
        beat_time = self.song().get_current_beats_song_time()
        position_str = ()
        if self.application().view.is_view_visible('Session'):
            current_slot = self.song().view.highlighted_clip_slot
            position_str = self._Tranzport__translate_string('[No Clip]  ')
            if not current_slot or current_slot.clip:
                if current_slot.clip.name == '':
                    position_str = self._Tranzport__translate_string('[No Name]  ')
                else:
                    position_str = self._Tranzport__translate_string(self._Tranzport__bring_string_to_length(current_slot.clip.name, 9)) + self._Tranzport__translate_string('  ')
        else:
            position_str = self._Tranzport__translate_string(str('%3d.' % beat_time.bars)) + self._Tranzport__translate_string(str('%02d.' % beat_time.beats)) + self._Tranzport__translate_string(str('%02d  ' % beat_time.ticks))
        tempo_str = self._Tranzport__translate_string('%3.2fbpm' % self.song().tempo)
        if len(tempo_str) == 8:
            tempo_str = (32, ) + tempo_str
        self._Tranzport__display_line_two = position_str + tempo_str

    def __show_vol_and_pan(self):
        volume = self._Tranzport__current_track.mixer_device.volume
        panning = self._Tranzport__current_track.mixer_device.panning
        if self._Tranzport__current_track.has_audio_output:
            self._Tranzport__display_line_two = self._Tranzport__translate_string(self._Tranzport__string_from_number_with_length(volume, 9)) + self._Tranzport__translate_string('       ') + self._Tranzport__translate_string(self._Tranzport__string_from_number_with_length(panning, 3))
        else:
            self._Tranzport__display_line_two = self._Tranzport__translate_string('  No Audio Output   ')

    def __show_loop_settings(self):
        start_time = self.song().get_beats_loop_start()
        length_time = self.song().get_beats_loop_length()
        self._Tranzport__display_line_two = self._Tranzport__translate_string('S%3d.' % start_time.bars) + self._Tranzport__translate_string('%02d.' % start_time.beats) + self._Tranzport__translate_string('%02d ' % start_time.ticks) + self._Tranzport__translate_string('L%2d.' % length_time.bars) + self._Tranzport__translate_string('%02d.' % length_time.beats) + self._Tranzport__translate_string('%02d' % length_time.ticks)

    def __show_send_settings(self):
        result = ()
        if len(self._Tranzport__current_track.mixer_device.sends) > 0 and self._Tranzport__current_track.has_audio_output:
            if self._Tranzport__current_send_index >= len(self._Tranzport__current_track.mixer_device.sends):
                self._Tranzport__current_send_index = len(self._Tranzport__current_track.mixer_device.sends) - 1
            else:
                if self._Tranzport__current_send_index < 0:
                    self._Tranzport__current_send_index = 0
            current_send = self._Tranzport__current_track.mixer_device.sends[self._Tranzport__current_send_index]
            result = self._Tranzport__translate_string(self._Tranzport__string_from_number_with_length(current_send, 8)) + self._Tranzport__translate_string('  in  ') + self._Tranzport__translate_string(current_send.name)
        else:
            result = self._Tranzport__translate_string(' No Sends Available ')
        self._Tranzport__display_line_two = result

    def __show_page_select(self):
        index = self._Tranzport__selected_page
        if self.application().view.is_view_visible('Session') or index > 0:
            index = index + 1
        pages_list = ('<', ) + PAGES_NAMES[index] + ('>', )
        position = 10 - old_div(len(pages_list), 2)
        message = ()
        for i in range(position):
            message = message + (32, )

        message = message + self._Tranzport__translate_string(pages_list)
        for i in range(position):
            message = message + (32, )

        self._Tranzport__display_line_two = message

    def __set_record_mode_led(self):
        if self.song().record_mode:
            self.send_midi((NOTE_ON_STATUS, TRANZ_REC, LED_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, TRANZ_REC, LED_OFF))

    def __set_track_armed_led(self):
        status = LED_OFF
        if list(self.song().visible_tracks).count(self._Tranzport__current_track) > 0:
            if self.song().view.selected_track.arm:
                status = LED_ON
        self.send_midi((NOTE_ON_STATUS, TRANZ_ARM_TRACK, status))

    def is_track_visible(self, track):
        return (list(self.song().visible_tracks) + list(self.song().return_tracks)).count(track) > 0

    def __set_track_muted_led(self):
        status = LED_OFF
        if self.is_track_visible(self._Tranzport__current_track):
            if self.song().view.selected_track.mute:
                status = LED_ON
        self.send_midi((NOTE_ON_STATUS, TRANZ_MUTE_TRACK, status))

    def __set_track_soloed_led(self):
        status = LED_OFF
        if self.is_track_visible(self._Tranzport__current_track):
            if self.song().view.selected_track.solo:
                status = LED_ON
        self.send_midi((NOTE_ON_STATUS, TRANZ_SOLO_TRACK, status))

    def __set_any_solo_led(self):
        status = LED_OFF
        for i in chain(self.song().tracks, self.song().return_tracks):
            if i.solo:
                status = LED_ON
                break

        self.send_midi((NOTE_ON_STATUS, TRANZ_ANY_SOLO, status))

    def __set_loop_led(self):
        status = LED_OFF
        if self.song().loop:
            status = LED_ON
        self.send_midi((NOTE_ON_STATUS, TRANZ_LOOP, status))

    def __current_track_name_changed(self):
        self._Tranzport__show_track_and_scene()

    def __on_selected_track_changed(self):
        if self.is_track_visible(self._Tranzport__current_track):
            self._Tranzport__current_track.remove_mute_listener(self._Tranzport__set_track_muted_led)
            self._Tranzport__current_track.remove_solo_listener(self._Tranzport__set_track_soloed_led)
            self._Tranzport__current_track.remove_name_listener(self._Tranzport__current_track_name_changed)
            if self._Tranzport__current_track in self.song().tracks:
                if self._Tranzport__current_track.can_be_armed:
                    self._Tranzport__current_track.remove_arm_listener(self._Tranzport__set_track_armed_led)
        self._Tranzport__current_track = self.song().view.selected_track
        if (list(self.song().visible_tracks) + list(self.song().return_tracks)).count(self._Tranzport__current_track) > 0:
            self._Tranzport__current_track.add_solo_listener(self._Tranzport__set_track_soloed_led)
            self._Tranzport__current_track.add_mute_listener(self._Tranzport__set_track_muted_led)
            self._Tranzport__current_track.add_name_listener(self._Tranzport__current_track_name_changed)
            if self._Tranzport__current_track in self.song().visible_tracks:
                if self._Tranzport__current_track.can_be_armed:
                    self._Tranzport__current_track.add_arm_listener(self._Tranzport__set_track_armed_led)
        self._Tranzport__sends_in_current_track = len(self._Tranzport__current_track.mixer_device.sends)
        self._Tranzport__current_send_index = 0
        self.refresh_state()

    def __handle_page_select(self, direction):
        if self._Tranzport__showing_page_list:
            self._Tranzport__selected_page = self._Tranzport__selected_page + direction
            if self._Tranzport__selected_page >= NUM_PAGES:
                self._Tranzport__selected_page = 0
            else:
                if self._Tranzport__selected_page < 0:
                    self._Tranzport__selected_page = NUM_PAGES - 1
        else:
            self._Tranzport__showing_page_list = True
        self._Tranzport__show_page_select()

    def __shift_status_changed(self, status):
        if status == 0:
            self._Tranzport__shift_pressed = False
            self._Tranzport__showing_page_list = False
        else:
            self._Tranzport__shift_pressed = True
        self._Tranzport__show_selected_page()

    def __translate_string(self, text):
        result = ()
        length = len(text)
        for i in range(0, length):
            char_code = self._Tranzport__character_code(text[i])
            if char_code < 0:
                char_code = 32
            else:
                result = result + (char_code,)

        return result

    def __character_code(self, character):
        result = -1
        try:
            result = TRANZ_DICT[character]
        finally:
            return result

    def __bring_string_to_length(self, text, length):
        result = ()
        string_length = len(text)
        for i in range(length):
            if i < string_length:
                if i == length - 1:
                    result = result + ('>', )
                else:
                    result = result + (text[i],)
            else:
                result = result + (' ', )

        return result

    def __string_from_number_with_length(self, number, length):
        result = ()
        text = str(number)
        for i in range(len(text)):
            result = result + (text[i],)

        if len(result) < length:
            for i in range(length - len(result)):
                result = (' ', ) + result

        return result