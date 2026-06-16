# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL\MixerController.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 24946 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range, str
import Live
from .consts import *
from .RemoteSLComponent import RemoteSLComponent
SLIDER_MODE_VOLUME = 0
SLIDER_MODE_PAN = 1
SLIDER_MODE_SEND = 2
FORW_REW_JUMP_BY_AMOUNT = 1

class MixerController(RemoteSLComponent):

    def __init__(self, remote_sl_parent, display_controller):
        RemoteSLComponent.__init__(self, remote_sl_parent)
        self._MixerController__display_controller = display_controller
        self._MixerController__parent = remote_sl_parent
        self._MixerController__forward_button_down = False
        self._MixerController__rewind_button_down = False
        self._MixerController__strip_offset = 0
        self._MixerController__slider_mode = SLIDER_MODE_VOLUME
        self._MixerController__strips = [MixerChannelStrip(self, i) for i in range(NUM_CONTROLS_PER_ROW)]
        self._MixerController__assigned_tracks = []
        self._MixerController__transport_locked = False
        self._MixerController__lock_enquiry_delay = 0
        self.song().add_visible_tracks_listener(self._MixerController__on_tracks_added_or_deleted)
        self.song().add_record_mode_listener(self._MixerController__on_record_mode_changed)
        self.song().add_is_playing_listener(self._MixerController__on_is_playing_changed)
        self.song().add_loop_listener(self._MixerController__on_loop_changed)
        self._MixerController__reassign_strips()

    def disconnect(self):
        self.song().remove_visible_tracks_listener(self._MixerController__on_tracks_added_or_deleted)
        self.song().remove_record_mode_listener(self._MixerController__on_record_mode_changed)
        self.song().remove_is_playing_listener(self._MixerController__on_is_playing_changed)
        self.song().remove_loop_listener(self._MixerController__on_loop_changed)
        for strip in self._MixerController__strips:
            strip.set_assigned_track(None)

        for track in self._MixerController__assigned_tracks:
            if track:
                if track.name_has_listener(self._MixerController__on_track_name_changed):
                    track.remove_name_listener(self._MixerController__on_track_name_changed)

    def remote_sl_parent(self):
        return self._MixerController__parent

    def slider_mode(self):
        return self._MixerController__slider_mode

    def receive_midi_cc(self, cc_no, cc_value):
        if cc_no in mx_display_button_ccs:
            self._MixerController__handle_page_up_down_ccs(cc_no, cc_value)
        else:
            if cc_no in mx_select_button_ccs:
                self._MixerController__handle_select_button_ccs(cc_no, cc_value)
            else:
                if cc_no in mx_first_button_row_ccs:
                    channel_strip = self._MixerController__strips[cc_no - MX_FIRST_BUTTON_ROW_BASE_CC]
                    if cc_value == CC_VAL_BUTTON_PRESSED:
                        channel_strip.first_button_pressed()
                else:
                    if cc_no in mx_second_button_row_ccs:
                        channel_strip = self._MixerController__strips[cc_no - MX_SECOND_BUTTON_ROW_BASE_CC]
                        if cc_value == CC_VAL_BUTTON_PRESSED:
                            channel_strip.second_button_pressed()
                    else:
                        if cc_no in mx_slider_row_ccs:
                            channel_strip = self._MixerController__strips[cc_no - MX_SLIDER_ROW_BASE_CC]
                            channel_strip.slider_moved(cc_value)
                        else:
                            if cc_no in ts_ccs:
                                self._MixerController__handle_transport_ccs(cc_no, cc_value)
                            else:
                                pass

    def build_midi_map(self, script_handle, midi_map_handle):
        needs_takeover = True
        for s in self._MixerController__strips:
            cc_no = MX_SLIDER_ROW_BASE_CC + self._MixerController__strips.index(s)
            if s.assigned_track() and s.slider_parameter():
                map_mode = Live.MidiMap.MapMode.absolute
                parameter = s.slider_parameter()
                Live.MidiMap.map_midi_cc(midi_map_handle, parameter, SL_MIDI_CHANNEL, cc_no, map_mode, not needs_takeover)
            else:
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, SL_MIDI_CHANNEL, cc_no)

        for cc_no in mx_forwarded_ccs + ts_ccs:
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, SL_MIDI_CHANNEL, cc_no)

        for note in mx_forwarded_notes + ts_notes:
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, SL_MIDI_CHANNEL, note)

    def refresh_state(self):
        self._MixerController__update_selected_row_leds()
        self._MixerController__reassign_strips()
        self._MixerController__lock_enquiry_delay = 3

    def update_display(self):
        if self._MixerController__lock_enquiry_delay > 0:
            self._MixerController__lock_enquiry_delay -= 1
            if self._MixerController__lock_enquiry_delay == 0:
                self.send_midi((176, 103, 1))
        if self._MixerController__rewind_button_down:
            self.song().jump_by(-FORW_REW_JUMP_BY_AMOUNT)
        if self._MixerController__forward_button_down:
            self.song().jump_by(FORW_REW_JUMP_BY_AMOUNT)

    def __reassign_strips(self):
        track_index = self._MixerController__strip_offset
        track_names = []
        parameters = []
        for track in self._MixerController__assigned_tracks:
            if track:
                if track.name_has_listener(self._MixerController__on_track_name_changed):
                    track.remove_name_listener(self._MixerController__on_track_name_changed)

        self._MixerController__assigned_tracks = []
        all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
        for s in self._MixerController__strips:
            if track_index < len(all_tracks):
                track = all_tracks[track_index]
                s.set_assigned_track(track)
                track_names.append(track.name)
                parameters.append(s.slider_parameter())
                track.add_name_listener(self._MixerController__on_track_name_changed)
                self._MixerController__assigned_tracks.append(track)
            else:
                s.set_assigned_track(None)
                track_names.append('')
                parameters.append(None)
            track_index += 1

        self._MixerController__display_controller.setup_right_display(track_names, parameters)
        self.request_rebuild_midi_map()
        if self.support_mkII():
            page_up_value = CC_VAL_BUTTON_RELEASED
            page_down_value = CC_VAL_BUTTON_RELEASED
            if len(all_tracks) > NUM_CONTROLS_PER_ROW:
                if self._MixerController__strip_offset < len(all_tracks) - NUM_CONTROLS_PER_ROW:
                    page_up_value = CC_VAL_BUTTON_PRESSED
            if self._MixerController__strip_offset > 0:
                page_down_value = CC_VAL_BUTTON_PRESSED
            self.send_midi((self.cc_status_byte(), MX_DISPLAY_PAGE_UP, page_up_value))
            self.send_midi((self.cc_status_byte(), MX_DISPLAY_PAGE_DOWN, page_down_value))

    def __handle_page_up_down_ccs(self, cc_no, cc_value):
        all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
        if cc_no == MX_DISPLAY_PAGE_UP:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                if len(all_tracks) > NUM_CONTROLS_PER_ROW:
                    if self._MixerController__strip_offset < len(all_tracks) - NUM_CONTROLS_PER_ROW:
                        self._MixerController__strip_offset += NUM_CONTROLS_PER_ROW
                        self._MixerController__validate_strip_offset()
                        self._MixerController__reassign_strips()
        if cc_no == MX_DISPLAY_PAGE_DOWNand cc_value == CC_VAL_BUTTON_PRESSED and cc_value == CC_VAL_BUTTON_PRESSED and self._MixerController__strip_offset > 0:
            self._MixerController__strip_offset -= NUM_CONTROLS_PER_ROW
            self._MixerController__validate_strip_offset()
            self._MixerController__reassign_strips()
        else:
            pass

    def __handle_select_button_ccs(self, cc_no, cc_value):
        if cc_no == MX_SELECT_SLIDER_ROW:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self._MixerController__set_slider_mode(SLIDER_MODE_VOLUME)
        else:
            if cc_no == MX_SELECT_FIRST_BUTTON_ROW:
                if cc_value == CC_VAL_BUTTON_PRESSED:
                    self._MixerController__set_slider_mode(SLIDER_MODE_PAN)
            else:
                if cc_no == MX_SELECT_SECOND_BUTTON_ROW and cc_value == CC_VAL_BUTTON_PRESSED:
                    self._MixerController__set_slider_mode(SLIDER_MODE_SEND)
                else:
                    pass

    def __handle_transport_ccs(self, cc_no, cc_value):
        if cc_no == TS_REWIND_CC:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self._MixerController__rewind_button_down = True
                self.song().jump_by(-FORW_REW_JUMP_BY_AMOUNT)
            else:
                self._MixerController__rewind_button_down = False
        else:
            if cc_no == TS_FORWARD_CC:
                if cc_value == CC_VAL_BUTTON_PRESSED:
                    self._MixerController__forward_button_down = True
                    self.song().jump_by(FORW_REW_JUMP_BY_AMOUNT)
                else:
                    self._MixerController__forward_button_down = False
            else:
                if cc_no == TS_STOP_CC:
                    if cc_value == CC_VAL_BUTTON_PRESSED:
                        self.song().stop_playing()
                else:
                    if cc_no == TS_PLAY_CC:
                        if cc_value == CC_VAL_BUTTON_PRESSED:
                            self.song().start_playing()
                    else:
                        if cc_no == TS_LOOP_CC:
                            if cc_value == CC_VAL_BUTTON_PRESSED:
                                self.song().loop = not self.song().loop
                        else:
                            if cc_no == TS_RECORD_CC:
                                if cc_value == CC_VAL_BUTTON_PRESSED:
                                    self.song().record_mode = not self.song().record_mode
                            else:
                                if cc_no == TS_LOCK:
                                    self._MixerController__transport_locked = cc_value != CC_VAL_BUTTON_RELEASED
                                    self._MixerController__on_transport_lock_changed()
                                else:
                                    pass

    def __on_transport_lock_changed(self):
        for strip in self._MixerController__strips:
            strip.take_control_of_second_button(not self._MixerController__transport_locked)

        if self._MixerController__transport_locked:
            self._MixerController__on_is_playing_changed()
            self._MixerController__on_loop_changed()
            self._MixerController__on_record_mode_changed()

    def __on_tracks_added_or_deleted(self):
        self._MixerController__validate_strip_offset()
        self._MixerController__validate_slider_mode()
        self._MixerController__reassign_strips()

    def __on_track_name_changed(self):
        self._MixerController__reassign_strips()

    def __validate_strip_offset(self):
        all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
        self._MixerController__strip_offset = min(self._MixerController__strip_offset, len(all_tracks) - 1)
        self._MixerController__strip_offset = max(0, self._MixerController__strip_offset)

    def __validate_slider_mode(self):
        if self._MixerController__slider_mode - SLIDER_MODE_SEND >= len(self.song().return_tracks):
            self._MixerController__slider_mode = SLIDER_MODE_VOLUME

    def __set_slider_mode(self, new_mode):
        if self._MixerController__slider_mode >= SLIDER_MODE_SEND and new_mode >= SLIDER_MODE_SEND:
            if self._MixerController__slider_mode - SLIDER_MODE_SEND + 1 < len(self.song().return_tracks):
                self._MixerController__slider_mode += 1
            else:
                self._MixerController__slider_mode = SLIDER_MODE_SEND
            self._MixerController__update_selected_row_leds()
            self._MixerController__reassign_strips()
        else:
            if self._MixerController__slider_mode != new_mode:
                self._MixerController__slider_mode = new_mode
                self._MixerController__update_selected_row_leds()
                self._MixerController__reassign_strips()

    def __update_selected_row_leds(self):
        if self._MixerController__slider_mode == SLIDER_MODE_VOLUME:
            self.send_midi((
             self.cc_status_byte(), MX_SELECT_SLIDER_ROW, CC_VAL_BUTTON_PRESSED))
            self.send_midi((
             self.cc_status_byte(),
             MX_SELECT_FIRST_BUTTON_ROW,
             CC_VAL_BUTTON_RELEASED))
            self.send_midi((
             self.cc_status_byte(),
             MX_SELECT_SECOND_BUTTON_ROW,
             CC_VAL_BUTTON_RELEASED))
        else:
            if self._MixerController__slider_mode == SLIDER_MODE_PAN:
                self.send_midi((
                 self.cc_status_byte(), MX_SELECT_SLIDER_ROW, CC_VAL_BUTTON_RELEASED))
                self.send_midi((
                 self.cc_status_byte(), MX_SELECT_FIRST_BUTTON_ROW, CC_VAL_BUTTON_PRESSED))
                self.send_midi((
                 self.cc_status_byte(),
                 MX_SELECT_SECOND_BUTTON_ROW,
                 CC_VAL_BUTTON_RELEASED))
            else:
                if self._MixerController__slider_mode >= SLIDER_MODE_SEND:
                    self.send_midi((
                     self.cc_status_byte(), MX_SELECT_SLIDER_ROW, CC_VAL_BUTTON_RELEASED))
                    self.send_midi((
                     self.cc_status_byte(),
                     MX_SELECT_FIRST_BUTTON_ROW,
                     CC_VAL_BUTTON_RELEASED))
                    self.send_midi((
                     self.cc_status_byte(),
                     MX_SELECT_SECOND_BUTTON_ROW,
                     CC_VAL_BUTTON_PRESSED))

    def __on_record_mode_changed(self):
        if not (self._MixerController__transport_locked or self.support_mkII()):
            record_cc = TS_RECORD_CC
            if self.support_mkII():
                record_cc = 53
            record_value = CC_VAL_BUTTON_PRESSED
            if not self.song().record_mode:
                record_value = CC_VAL_BUTTON_RELEASED
            self.send_midi((self.cc_status_byte(), record_cc, record_value))

    def __on_is_playing_changed(self):
        if self._MixerController__transport_locked:
            if self.support_mkII():
                if self.song().is_playing:
                    self.send_midi((self.cc_status_byte(), 51, CC_VAL_BUTTON_PRESSED))
                    self.send_midi((self.cc_status_byte(), 50, CC_VAL_BUTTON_RELEASED))
                else:
                    self.send_midi((self.cc_status_byte(), 51, CC_VAL_BUTTON_RELEASED))
                    self.send_midi((self.cc_status_byte(), 50, CC_VAL_BUTTON_PRESSED))

    def __on_loop_changed(self):
        if self._MixerController__transport_locked:
            if self.support_mkII():
                if self.song().loop:
                    self.send_midi((self.cc_status_byte(), 52, CC_VAL_BUTTON_PRESSED))
                else:
                    self.send_midi((self.cc_status_byte(), 52, CC_VAL_BUTTON_RELEASED))

    def is_arm_exclusive(self):
        return self._MixerController__parent.song().exclusive_arm

    def set_selected_track(self, track):
        if track:
            self._MixerController__parent.song().view.selected_track = track

    def track_about_to_arm(self, track):
        if track:
            if self._MixerController__parent.song().exclusive_arm:
                for t in self._MixerController__parent.song().tracks:
                    if t.can_be_armed:
                        if t.arm:
                            if not t == track:
                                t.arm = False


class MixerChannelStrip(object):

    def __init__(self, mixer_controller_parent, index):
        self._MixerChannelStrip__mixer_controller = mixer_controller_parent
        self._MixerChannelStrip__index = index
        self._MixerChannelStrip__assigned_track = None
        self._MixerChannelStrip__control_second_button = True

    def song(self):
        return self._MixerChannelStrip__mixer_controller.song()

    def assigned_track(self):
        return self._MixerChannelStrip__assigned_track

    def set_assigned_track(self, track):
        if self._MixerChannelStrip__assigned_track != None:
            if self._MixerChannelStrip__assigned_track != self.song().master_track:
                self._MixerChannelStrip__assigned_track.remove_mute_listener(self._on_mute_changed)
            if self._MixerChannelStrip__assigned_track.can_be_armed:
                self._MixerChannelStrip__assigned_track.remove_arm_listener(self._on_arm_changed)
        self._MixerChannelStrip__assigned_track = track
        if self._MixerChannelStrip__assigned_track != None:
            if self._MixerChannelStrip__assigned_track != self.song().master_track:
                self._MixerChannelStrip__assigned_track.add_mute_listener(self._on_mute_changed)
            if self._MixerChannelStrip__assigned_track.can_be_armed:
                self._MixerChannelStrip__assigned_track.add_arm_listener(self._on_arm_changed)
        self._on_mute_changed()
        self._on_arm_changed()

    def slider_parameter(self):
        slider_mode = self._MixerChannelStrip__mixer_controller.slider_mode()
        if self._MixerChannelStrip__assigned_track:
            if slider_mode == SLIDER_MODE_VOLUME:
                return self._MixerChannelStrip__assigned_track.mixer_device.volume
            if slider_mode == SLIDER_MODE_PAN:
                return self._MixerChannelStrip__assigned_track.mixer_device.panning
            if slider_mode >= SLIDER_MODE_SEND:
                send_index = slider_mode - SLIDER_MODE_SEND
                if send_index < len(self._MixerChannelStrip__assigned_track.mixer_device.sends):
                    return self._MixerChannelStrip__assigned_track.mixer_device.sends[send_index]
                return
        else:
            return

    def slider_moved(self, cc_value):
        pass

    def take_control_of_second_button(self, take_control):
        if self._MixerChannelStrip__mixer_controller.support_mkII():
            self._MixerChannelStrip__mixer_controller.remote_sl_parent().send_midi((
             self._MixerChannelStrip__mixer_controller.cc_status_byte(),
             self._MixerChannelStrip__index + MX_SECOND_BUTTON_ROW_BASE_CC,
             0))
        self._MixerChannelStrip__control_second_button = take_control
        self._on_mute_changed()
        self._on_arm_changed()

    def first_button_pressed(self):
        if self._MixerChannelStrip__assigned_track:
            if self._MixerChannelStrip__assigned_track in tuple(self.song().visible_tracks) + tuple(self.song().return_tracks):
                self._MixerChannelStrip__assigned_track.mute = not self._MixerChannelStrip__assigned_track.mute

    def second_button_pressed(self):
        if self._MixerChannelStrip__assigned_track in self.song().visible_tracks:
            if self._MixerChannelStrip__assigned_track.can_be_armed:
                self._MixerChannelStrip__mixer_controller.track_about_to_arm(self._MixerChannelStrip__assigned_track)
                self._MixerChannelStrip__assigned_track.arm = not self._MixerChannelStrip__assigned_track.arm
                if self._MixerChannelStrip__assigned_track.arm:
                    if self._MixerChannelStrip__assigned_track.view.select_instrument():
                        self._MixerChannelStrip__mixer_controller.set_selected_track(self._MixerChannelStrip__assigned_track)

    def _on_mute_changed(self):
        if self._MixerChannelStrip__mixer_controller.support_mkII():
            value = 0
            if self._MixerChannelStrip__assigned_track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
                if not self._MixerChannelStrip__assigned_track.mute:
                    value = 1
                self._MixerChannelStrip__mixer_controller.remote_sl_parent().send_midi((
                 self._MixerChannelStrip__mixer_controller.cc_status_byte(),
                 self._MixerChannelStrip__index + MX_FIRST_BUTTON_ROW_BASE_CC,
                 value))

    def _on_arm_changed(self):
        if self._MixerChannelStrip__control_second_button:
            if self._MixerChannelStrip__mixer_controller.support_mkII():
                value = 0
                if self._MixerChannelStrip__assigned_track:
                    if self._MixerChannelStrip__assigned_track in self.song().tracks:
                        if self._MixerChannelStrip__assigned_track.can_be_armed:
                            if self._MixerChannelStrip__assigned_track.arm:
                                value = 1
                self._MixerChannelStrip__mixer_controller.remote_sl_parent().send_midi((
                 self._MixerChannelStrip__mixer_controller.cc_status_byte(),
                 self._MixerChannelStrip__index + MX_SECOND_BUTTON_ROW_BASE_CC,
                 value))