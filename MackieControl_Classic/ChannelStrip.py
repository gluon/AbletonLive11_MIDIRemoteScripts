# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl_Classic\ChannelStrip.py
# Compiled at: 2023-03-08 07:29:56
# Size of source mod 2**32: 23708 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from itertools import chain
from ableton.v2.base import liveobj_valid
from .MackieControlComponent import *

class ChannelStrip(MackieControlComponent):

    def __init__(self, main_script, strip_index):
        MackieControlComponent.__init__(self, main_script)
        self._ChannelStrip__channel_strip_controller = None
        self._ChannelStrip__is_touched = False
        self._ChannelStrip__strip_index = strip_index
        self._ChannelStrip__stack_offset = 0
        self._ChannelStrip__bank_and_channel_offset = 0
        self._ChannelStrip__assigned_track = None
        self._ChannelStrip__v_pot_parameter = None
        self._ChannelStrip__v_pot_display_mode = VPOT_DISPLAY_SINGLE_DOT
        self._ChannelStrip__fader_parameter = None
        self._ChannelStrip__meters_enabled = False
        self._ChannelStrip__last_meter_value = -1
        self._ChannelStrip__send_meter_mode()
        self._ChannelStrip__within_track_added_or_deleted = False
        self._ChannelStrip__within_destroy = False
        self.set_bank_and_channel_offset(offset=0,
          show_return_tracks=False,
          within_track_added_or_deleted=False)

    def destroy(self):
        self._ChannelStrip__within_destroy = True
        if self._ChannelStrip__assigned_track:
            self._ChannelStrip__remove_listeners()
        self._ChannelStrip__assigned_track = None
        self.send_midi((208, 0 + (self._ChannelStrip__strip_index << 4)))
        self._ChannelStrip__meters_enabled = False
        self._ChannelStrip__send_meter_mode()
        self.refresh_state()
        MackieControlComponent.destroy(self)
        self._ChannelStrip__within_destroy = False

    def set_channel_strip_controller(self, channel_strip_controller):
        self._ChannelStrip__channel_strip_controller = channel_strip_controller

    def strip_index(self):
        return self._ChannelStrip__strip_index

    def assigned_track(self):
        return self._ChannelStrip__assigned_track

    def is_touched(self):
        return self._ChannelStrip__is_touched

    def set_is_touched(self, touched):
        self._ChannelStrip__is_touched = touched

    def stack_offset(self):
        return self._ChannelStrip__stack_offset

    def set_stack_offset(self, offset):
        self._ChannelStrip__stack_offset = offset

    def set_bank_and_channel_offset(self, offset, show_return_tracks, within_track_added_or_deleted):
        final_track_index = self._ChannelStrip__strip_index + self._ChannelStrip__stack_offset + offset
        self._ChannelStrip__within_track_added_or_deleted = within_track_added_or_deleted
        if show_return_tracks:
            tracks = self.song().return_tracks
        else:
            tracks = self.song().visible_tracks
        if final_track_index < len(tracks):
            new_track = tracks[final_track_index]
        else:
            new_track = None
        if new_track != self._ChannelStrip__assigned_track:
            if self._ChannelStrip__assigned_track:
                self._ChannelStrip__remove_listeners()
            self._ChannelStrip__assigned_track = new_track
            if self._ChannelStrip__assigned_track:
                self._ChannelStrip__add_listeners()
        self.refresh_state()
        self._ChannelStrip__within_track_added_or_deleted = False

    def v_pot_parameter(self):
        return self._ChannelStrip__v_pot_parameter

    def set_v_pot_parameter(self, parameter, display_mode=VPOT_DISPLAY_SINGLE_DOT):
        self._ChannelStrip__v_pot_display_mode = display_mode
        self._ChannelStrip__v_pot_parameter = parameter
        if not parameter:
            self.unlight_vpot_leds()

    def fader_parameter(self):
        return self._ChannelStrip__fader_parameter

    def set_fader_parameter(self, parameter):
        self._ChannelStrip__fader_parameter = parameter
        if not parameter:
            self.reset_fader()

    def enable_meter_mode(self, Enabled, needs_to_send_meter_mode=True):
        self._ChannelStrip__meters_enabled = Enabled
        if needs_to_send_meter_mode or Enabled:
            self._ChannelStrip__send_meter_mode()

    def reset_fader(self):
        self.send_midi((PB_STATUS + self._ChannelStrip__strip_index, 0, 0))

    def unlight_vpot_leds(self):
        self.send_midi((CC_STATUS + 0, 48 + self._ChannelStrip__strip_index, 32))

    def show_full_enlighted_poti(self):
        self.send_midi((
         CC_STATUS + 0, 48 + self._ChannelStrip__strip_index, VPOT_DISPLAY_WRAP * 16 + 11))

    def handle_channel_strip_switch_ids(self, sw_id, value):
        if sw_id in range(SID_RECORD_ARM_BASE, SID_RECORD_ARM_BASE + NUM_CHANNEL_STRIPS):
            if sw_id - SID_RECORD_ARM_BASE is self._ChannelStrip__strip_index:
                if value == BUTTON_PRESSED:
                    if self.song().exclusive_arm:
                        exclusive = not self.control_is_pressed()
                    else:
                        exclusive = self.control_is_pressed()
                    self._ChannelStrip__toggle_arm_track(exclusive)
        else:
            if sw_id in range(SID_SOLO_BASE, SID_SOLO_BASE + NUM_CHANNEL_STRIPS):
                if sw_id - SID_SOLO_BASE is self._ChannelStrip__strip_index:
                    if value == BUTTON_PRESSED:
                        if self.song().exclusive_solo:
                            exclusive = not self.control_is_pressed()
                        else:
                            exclusive = self.control_is_pressed()
                        self._ChannelStrip__toggle_solo_track(exclusive)
            else:
                if sw_id in range(SID_MUTE_BASE, SID_MUTE_BASE + NUM_CHANNEL_STRIPS):
                    if sw_id - SID_MUTE_BASE is self._ChannelStrip__strip_index:
                        if value == BUTTON_PRESSED:
                            self._ChannelStrip__toggle_mute_track()
                else:
                    if sw_id in range(SID_SELECT_BASE, SID_SELECT_BASE + NUM_CHANNEL_STRIPS):
                        if not sw_id - SID_SELECT_BASE is self._ChannelStrip__strip_index or value == BUTTON_PRESSED:
                            self._ChannelStrip__select_track()
                    else:
                        if sw_id in range(SID_VPOD_PUSH_BASE, SID_VPOD_PUSH_BASE + NUM_CHANNEL_STRIPS):
                            if not sw_id - SID_VPOD_PUSH_BASE is self._ChannelStrip__strip_index or value == BUTTON_PRESSED:
                                self._ChannelStrip__channel_strip_controller.handle_pressed_v_pot(self._ChannelStrip__strip_index, self._ChannelStrip__stack_offset)
                        else:
                            if not sw_id in fader_touch_switch_ids or sw_id - SID_FADER_TOUCH_SENSE_BASE is self._ChannelStrip__strip_index:
                                if value == BUTTON_PRESSED or value == BUTTON_RELEASED:
                                    touched = value == BUTTON_PRESSED
                                    self.set_is_touched(touched)
                                    self._ChannelStrip__channel_strip_controller.handle_fader_touch(self._ChannelStrip__strip_index, self._ChannelStrip__stack_offset, touched)

    def handle_vpot_rotation(self, strip_index, cc_value):
        if strip_index is self._ChannelStrip__strip_index:
            self._ChannelStrip__channel_strip_controller.handle_vpot_rotation(self._ChannelStrip__strip_index, self._ChannelStrip__stack_offset, cc_value)

    def refresh_state(self):
        if not self._ChannelStrip__within_track_added_or_deleted:
            self._ChannelStrip__update_track_is_selected_led()
        self._ChannelStrip__update_solo_led()
        self._ChannelStrip__update_mute_led()
        self._ChannelStrip__update_arm_led()
        if not self._ChannelStrip__within_destroy:
            if self._ChannelStrip__assigned_track != None:
                self._ChannelStrip__send_meter_mode()
                self._ChannelStrip__last_meter_value = -1
        if not self._ChannelStrip__assigned_track:
            self.reset_fader()
            self.unlight_vpot_leds()

    def on_update_display_timer(self):
        if not self.main_script().is_pro_version and self._ChannelStrip__meters_enabled or self._ChannelStrip__channel_strip_controller.assignment_mode() == CSM_VOLPAN and self._ChannelStrip__assigned_track:
            if self._ChannelStrip__assigned_track.can_be_armed and self._ChannelStrip__assigned_track.arm:
                meter_value = self._ChannelStrip__assigned_track.input_meter_level
            else:
                meter_value = self._ChannelStrip__assigned_track.output_meter_level
        else:
            meter_value = 0.0
        meter_byte = int(meter_value * 12.0) + (self._ChannelStrip__strip_index << 4)
        if self._ChannelStrip__last_meter_value != meter_value or meter_value != 0.0:
            self._ChannelStrip__last_meter_value = meter_value
            self.send_midi((208, meter_byte))

    def build_midi_map(self, midi_map_handle):
        needs_takeover = False
        if self._ChannelStrip__fader_parameter:
            feeback_rule = Live.MidiMap.PitchBendFeedbackRule()
            feeback_rule.channel = self._ChannelStrip__strip_index
            feeback_rule.value_pair_map = tuple()
            feeback_rule.delay_in_ms = 200.0
            Live.MidiMap.map_midi_pitchbend_with_feedback_map(midi_map_handle, self._ChannelStrip__fader_parameter, self._ChannelStrip__strip_index, feeback_rule, not needs_takeover)
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, self._ChannelStrip__fader_parameter)
        else:
            channel = self._ChannelStrip__strip_index
            Live.MidiMap.forward_midi_pitchbend(self.script_handle(), midi_map_handle, channel)
        if self._ChannelStrip__v_pot_parameter:
            if self._ChannelStrip__v_pot_display_mode == VPOT_DISPLAY_SPREAD:
                range_end = 7
            else:
                range_end = 12
            feeback_rule = Live.MidiMap.CCFeedbackRule()
            feeback_rule.channel = 0
            feeback_rule.cc_no = 48 + self._ChannelStrip__strip_index
            feeback_rule.cc_value_map = tuple([self._ChannelStrip__v_pot_display_mode * 16 + x for x in range(1, range_end)])
            feeback_rule.delay_in_ms = -1.0
            Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, self._ChannelStrip__v_pot_parameter, 0, FID_PANNING_BASE + self._ChannelStrip__strip_index, Live.MidiMap.MapMode.relative_signed_bit, feeback_rule, needs_takeover)
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, self._ChannelStrip__v_pot_parameter)
        else:
            channel = 0
            cc_no = FID_PANNING_BASE + self._ChannelStrip__strip_index
            Live.MidiMap.forward_midi_cc(self.script_handle(), midi_map_handle, channel, cc_no)

    def __assigned_track_index(self):
        index = 0
        for t in chain(self.song().visible_tracks, self.song().return_tracks):
            if t == self._ChannelStrip__assigned_track:
                return index
            else:
                index += 1

        if self._ChannelStrip__assigned_track:
            pass

    def __add_listeners(self):
        if self._ChannelStrip__assigned_track:
            if self._ChannelStrip__assigned_track in self.song().tracks:
                self._ChannelStrip__assigned_track.add_input_routing_type_listener(self._ChannelStrip__update_arm_led)
                if self._ChannelStrip__assigned_track.can_be_armed:
                    self._ChannelStrip__assigned_track.add_arm_listener(self._ChannelStrip__update_arm_led)
        self._ChannelStrip__assigned_track.add_mute_listener(self._ChannelStrip__update_mute_led)
        self._ChannelStrip__assigned_track.add_solo_listener(self._ChannelStrip__update_solo_led)
        if not self.song().view.selected_track_has_listener(self._ChannelStrip__update_track_is_selected_led):
            self.song().view.add_selected_track_listener(self._ChannelStrip__update_track_is_selected_led)

    def __remove_listeners(self):
        if liveobj_valid(self._ChannelStrip__assigned_track):
            if self._ChannelStrip__assigned_track in self.song().tracks:
                self._ChannelStrip__remove_listener(self._ChannelStrip__assigned_track, 'input_routing_type', self._ChannelStrip__update_arm_led)
                if self._ChannelStrip__assigned_track.can_be_armed:
                    self._ChannelStrip__remove_listener(self._ChannelStrip__assigned_track, 'arm', self._ChannelStrip__update_arm_led)
            self._ChannelStrip__remove_listener(self._ChannelStrip__assigned_track, 'mute', self._ChannelStrip__update_mute_led)
            self._ChannelStrip__remove_listener(self._ChannelStrip__assigned_track, 'solo', self._ChannelStrip__update_solo_led)
            self._ChannelStrip__remove_listener(self.song().view, 'selected_track', self._ChannelStrip__update_track_is_selected_led)

    def __remove_listener(self, object, property, listener):
        if getattr(object, '{}_has_listener'.format(property))(listener):
            getattr(object, 'remove_{}_listener'.format(property))(listener)

    def __send_meter_mode(self):
        on_mode = 1
        off_mode = 0
        if self._ChannelStrip__meters_enabled:
            on_mode = on_mode | 2
        if self._ChannelStrip__assigned_track:
            mode = on_mode
        else:
            mode = off_mode
        if self.main_script().is_extension():
            device_type = SYSEX_DEVICE_TYPE_XT
        else:
            device_type = SYSEX_DEVICE_TYPE
        self.send_midi((
         240, 0, 0, 102, device_type, 32, self._ChannelStrip__strip_index, mode, 247))

    def __toggle_arm_track(self, exclusive):
        if self._ChannelStrip__assigned_track:
            if self._ChannelStrip__assigned_track.can_be_armed:
                self._ChannelStrip__assigned_track.arm = not self._ChannelStrip__assigned_track.arm
                if exclusive:
                    for t in self.song().tracks:
                        if t != self._ChannelStrip__assigned_track:
                            if t.can_be_armed:
                                t.arm = False

    def __toggle_mute_track(self):
        if self._ChannelStrip__assigned_track:
            self._ChannelStrip__assigned_track.mute = not self._ChannelStrip__assigned_track.mute

    def __toggle_solo_track(self, exclusive):
        if self._ChannelStrip__assigned_track:
            self._ChannelStrip__assigned_track.solo = not self._ChannelStrip__assigned_track.solo
            if exclusive:
                for t in chain(self.song().tracks, self.song().return_tracks):
                    if t != self._ChannelStrip__assigned_track:
                        t.solo = False

    def __select_track(self):
        if self._ChannelStrip__assigned_track:
            all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)
            if self.song().view.selected_track != all_tracks[self._ChannelStrip__assigned_track_index()]:
                self.song().view.selected_track = all_tracks[self._ChannelStrip__assigned_track_index()]
            else:
                if self.application().view.is_view_visible('Arranger'):
                    if self._ChannelStrip__assigned_track:
                        self._ChannelStrip__assigned_track.view.is_collapsed = not self._ChannelStrip__assigned_track.view.is_collapsed

    def __update_arm_led(self):
        track = self._ChannelStrip__assigned_track
        if track and track.can_be_armed and track.arm:
            self.send_midi((
             NOTE_ON_STATUS,
             SID_RECORD_ARM_BASE + self._ChannelStrip__strip_index,
             BUTTON_STATE_ON))
        else:
            self.send_midi((
             NOTE_ON_STATUS,
             SID_RECORD_ARM_BASE + self._ChannelStrip__strip_index,
             BUTTON_STATE_OFF))

    def __update_mute_led(self):
        if self._ChannelStrip__assigned_track and self._ChannelStrip__assigned_track.mute:
            self.send_midi((
             NOTE_ON_STATUS, SID_MUTE_BASE + self._ChannelStrip__strip_index, BUTTON_STATE_ON))
        else:
            self.send_midi((
             NOTE_ON_STATUS, SID_MUTE_BASE + self._ChannelStrip__strip_index, BUTTON_STATE_OFF))

    def __update_solo_led(self):
        if self._ChannelStrip__assigned_track and self._ChannelStrip__assigned_track.solo:
            self.send_midi((
             NOTE_ON_STATUS, SID_SOLO_BASE + self._ChannelStrip__strip_index, BUTTON_STATE_ON))
        else:
            self.send_midi((
             NOTE_ON_STATUS, SID_SOLO_BASE + self._ChannelStrip__strip_index, BUTTON_STATE_OFF))

    def __update_track_is_selected_led(self):
        if self.song().view.selected_track == self._ChannelStrip__assigned_track:
            self.send_midi((
             NOTE_ON_STATUS, SID_SELECT_BASE + self._ChannelStrip__strip_index, BUTTON_STATE_ON))
        else:
            self.send_midi((
             NOTE_ON_STATUS, SID_SELECT_BASE + self._ChannelStrip__strip_index, BUTTON_STATE_OFF))


class MasterChannelStrip(MackieControlComponent):

    def __init__(self, main_script):
        MackieControlComponent.__init__(self, main_script)
        self._MasterChannelStrip__strip_index = MASTER_CHANNEL_STRIP_INDEX
        self._MasterChannelStrip__assigned_track = self.song().master_track

    def destroy(self):
        self.reset_fader()
        MackieControlComponent.destroy(self)

    def set_channel_strip_controller(self, channel_strip_controller):
        pass

    def handle_channel_strip_switch_ids(self, sw_id, value):
        pass

    def refresh_state(self):
        pass

    def on_update_display_timer(self):
        pass

    def enable_meter_mode(self, Enabled):
        pass

    def reset_fader(self):
        self.send_midi((PB_STATUS + self._MasterChannelStrip__strip_index, 0, 0))

    def build_midi_map(self, midi_map_handle):
        needs_takeover = False
        if self._MasterChannelStrip__assigned_track:
            volume = self._MasterChannelStrip__assigned_track.mixer_device.volume
            feeback_rule = Live.MidiMap.PitchBendFeedbackRule()
            feeback_rule.channel = self._MasterChannelStrip__strip_index
            feeback_rule.value_pair_map = tuple()
            feeback_rule.delay_in_ms = 200.0
            Live.MidiMap.map_midi_pitchbend_with_feedback_map(midi_map_handle, volume, self._MasterChannelStrip__strip_index, feeback_rule, not needs_takeover)
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, volume)