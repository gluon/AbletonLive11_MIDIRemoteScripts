# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL_Classic\EffectController.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 17178 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import object, range, str
from past.utils import old_div
import Live
from .consts import *
from .RemoteSLComponent import RemoteSLComponent

class EffectController(RemoteSLComponent):

    def __init__(self, remote_sl_parent, display_controller):
        RemoteSLComponent.__init__(self, remote_sl_parent)
        self._EffectController__display_controller = display_controller
        self._EffectController__parent = remote_sl_parent
        self._EffectController__last_selected_track = None
        self._EffectController__assigned_device_is_locked = False
        self._EffectController__assigned_device = None
        self._EffectController__change_assigned_device(self._EffectController__parent.song().appointed_device)
        self._EffectController__bank = 0
        self._EffectController__show_bank = False
        self._EffectController__strips = [EffectChannelStrip(self) for x in range(NUM_CONTROLS_PER_ROW)]
        self._EffectController__reassign_strips()

    def disconnect(self):
        self._EffectController__change_assigned_device(None)

    def receive_midi_cc(self, cc_no, cc_value):
        if cc_no in fx_display_button_ccs:
            self._EffectController__handle_page_up_down_ccs(cc_no, cc_value)
        else:
            if cc_no in fx_select_button_ccs:
                self._EffectController__handle_select_button_ccs(cc_no, cc_value)
            else:
                if cc_no in fx_upper_button_row_ccs:
                    strip = self._EffectController__strips[cc_no - FX_UPPER_BUTTON_ROW_BASE_CC]
                    if cc_value == CC_VAL_BUTTON_PRESSED:
                        strip.on_button_pressed()
                else:
                    if cc_no in fx_encoder_row_ccs:
                        strip = self._EffectController__strips[cc_no - FX_ENCODER_ROW_BASE_CC]
                        strip.on_encoder_moved(cc_value)
                    else:
                        if cc_no in fx_lower_button_row_ccs:
                            pass
                        else:
                            if cc_no in fx_poti_row_ccs:
                                pass
                            else:
                                pass

    def receive_midi_note(self, note, velocity):
        if note in fx_drum_pad_row_notes:
            pass
        else:
            pass

    def build_midi_map(self, script_handle, midi_map_handle):
        needs_takeover = True
        for s in self._EffectController__strips:
            strip_index = self._EffectController__strips.index(s)
            cc_no = fx_encoder_row_ccs[strip_index]
            if s.assigned_parameter():
                map_mode = Live.MidiMap.MapMode.relative_smooth_signed_bit
                parameter = s.assigned_parameter()
                if self.support_mkII():
                    feedback_rule = Live.MidiMap.CCFeedbackRule()
                    feedback_rule.cc_no = fx_encoder_feedback_ccs[strip_index]
                    feedback_rule.channel = SL_MIDI_CHANNEL
                    feedback_rule.delay_in_ms = 0
                    feedback_rule.cc_value_map = tuple([int(1.5 + float(index) / 127.0 * 10.0) for index in range(128)])
                    ring_mode_value = FX_RING_VOL_VALUE
                    if parameter.min == -1 * parameter.max:
                        ring_mode_value = FX_RING_PAN_VALUE
                    else:
                        if parameter.is_quantized:
                            ring_mode_value = FX_RING_SIN_VALUE
                    self.send_midi((
                     self.cc_status_byte(),
                     fx_encoder_led_mode_ccs[strip_index],
                     ring_mode_value))
                    Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, parameter, SL_MIDI_CHANNEL, cc_no, map_mode, feedback_rule, not needs_takeover)
                    Live.MidiMap.send_feedback_for_parameter(midi_map_handle, parameter)
                else:
                    Live.MidiMap.map_midi_cc(midi_map_handle, parameter, SL_MIDI_CHANNEL, cc_no, map_mode, not needs_takeover)
            else:
                if self.support_mkII():
                    self.send_midi((
                     self.cc_status_byte(), fx_encoder_led_mode_ccs[strip_index], 0))
                    self.send_midi((
                     self.cc_status_byte(), fx_encoder_feedback_ccs[strip_index], 0))
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, SL_MIDI_CHANNEL, cc_no)

        for cc_no in fx_forwarded_ccs:
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, SL_MIDI_CHANNEL, cc_no)

        for note in fx_forwarded_notes:
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, SL_MIDI_CHANNEL, note)

    def refresh_state(self):
        self._EffectController__update_select_row_leds()
        self._EffectController__reassign_strips()

    def __reassign_strips(self):
        page_up_value = CC_VAL_BUTTON_RELEASED
        page_down_value = CC_VAL_BUTTON_RELEASED
        if not self._EffectController__assigned_device == None:
            param_index = 0
            param_names = []
            parameters = []
            for s in self._EffectController__strips:
                param = None
                name = ''
                new_index = param_index + self._EffectController__bank * 8
                device_parameters = self._EffectController__assigned_device.parameters[1:]
                if new_index < len(device_parameters):
                    param = device_parameters[new_index]
                else:
                    if param:
                        name = param.name
                    s.set_assigned_parameter(param)
                    parameters.append(param)
                    param_names.append(name)
                    param_index += 1

            if self._EffectController__bank > 0:
                page_down_value = CC_VAL_BUTTON_PRESSED
            if self._EffectController__bank + 1 < self._EffectController__number_of_parameter_banks():
                page_up_value = CC_VAL_BUTTON_PRESSED
            self._EffectController__report_bank()
        else:
            for s in self._EffectController__strips:
                s.set_assigned_parameter(None)

            param_names = [
             'Please select a Device in Live to edit it...']
            parameters = [None for x in range(NUM_CONTROLS_PER_ROW)]
        self._EffectController__display_controller.setup_left_display(param_names, parameters)
        self.request_rebuild_midi_map()
        if self.support_mkII():
            self.send_midi((self.cc_status_byte(), FX_DISPLAY_PAGE_DOWN, page_down_value))
            self.send_midi((self.cc_status_byte(), FX_DISPLAY_PAGE_UP, page_up_value))
            for cc_no in fx_upper_button_row_ccs:
                self.send_midi((self.cc_status_byte(), cc_no, CC_VAL_BUTTON_RELEASED))

    def __handle_page_up_down_ccs(self, cc_no, cc_value):
        if self._EffectController__assigned_device != None:
            new_bank = self._EffectController__bank
            if cc_value == CC_VAL_BUTTON_PRESSED:
                if cc_no == FX_DISPLAY_PAGE_UP:
                    new_bank = min(self._EffectController__bank + 1, self._EffectController__number_of_parameter_banks() - 1)
                else:
                    if cc_no == FX_DISPLAY_PAGE_DOWN:
                        new_bank = max(self._EffectController__bank - 1, 0)
                    else:
                        pass
                self._EffectController__show_bank = self._EffectController__bank == new_bank or True
                if not self._EffectController__assigned_device_is_locked:
                    self._EffectController__bank = new_bank
                    self._EffectController__reassign_strips()
                else:
                    self._EffectController__assigned_device.store_chosen_bank(self._EffectController__parent.instance_identifier(), new_bank)

    def __handle_select_button_ccs(self, cc_no, cc_value):
        if cc_no == FX_SELECT_FIRST_BUTTON_ROW:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self._EffectController__parent.toggle_lock()
        else:
            if cc_no == FX_SELECT_ENCODER_ROW:
                if cc_value == CC_VAL_BUTTON_PRESSED:
                    new_index = min(len(self.song().scenes) - 1, max(0, list(self.song().scenes).index(self.song().view.selected_scene) - 1))
                    self.song().view.selected_scene = self.song().scenes[new_index]
            else:
                if cc_no == FX_SELECT_SECOND_BUTTON_ROW:
                    if cc_value == CC_VAL_BUTTON_PRESSED:
                        new_index = min(len(self.song().scenes) - 1, max(0, list(self.song().scenes).index(self.song().view.selected_scene) + 1))
                        self.song().view.selected_scene = self.song().scenes[new_index]
                else:
                    if cc_no == FX_SELECT_POTIE_ROW:
                        if cc_value == CC_VAL_BUTTON_PRESSED:
                            self.song().view.selected_scene.fire_as_selected()
                    else:
                        if cc_no == FX_SELECT_DRUM_PAD_ROW and cc_value == CC_VAL_BUTTON_PRESSED:
                            self.song().stop_all_clips()
                        else:
                            pass

    def __update_select_row_leds(self):
        if self._EffectController__assigned_device_is_locked:
            self.send_midi((
             self.cc_status_byte(), FX_SELECT_FIRST_BUTTON_ROW, CC_VAL_BUTTON_PRESSED))
        else:
            self.send_midi((
             self.cc_status_byte(),
             FX_SELECT_FIRST_BUTTON_ROW,
             CC_VAL_BUTTON_RELEASED))

    def lock_to_device(self, device):
        if device:
            self._EffectController__assigned_device_is_locked = True
            self._EffectController__change_assigned_device(device)
            self._EffectController__update_select_row_leds()
            self._EffectController__reassign_strips()

    def unlock_from_device(self, device):
        if device:
            if device == self._EffectController__assigned_device:
                self._EffectController__assigned_device_is_locked = False
                self._EffectController__update_select_row_leds()
                if not self._EffectController__parent.song().appointed_device == self._EffectController__assigned_device:
                    self._EffectController__reassign_strips()

    def set_appointed_device(self, device):
        if not self._EffectController__assigned_device_is_locked:
            self._EffectController__change_assigned_device(device)
            self._EffectController__update_select_row_leds()
            self._EffectController__reassign_strips()

    def __report_bank(self):
        if self._EffectController__show_bank:
            self._EffectController__show_bank = False
            self._EffectController__show_bank_select('Bank' + str(self._EffectController__bank + 1))

    def __show_bank_select(self, bank_name):
        if self._EffectController__assigned_device:
            self._EffectController__parent.show_message(str(self._EffectController__assigned_device.name + ' Bank: ' + bank_name))

    def restore_bank(self, bank):
        if self._EffectController__assigned_device_is_locked:
            self._EffectController__bank = bank
            self._EffectController__reassign_strips()

    def __change_assigned_device(self, device):
        if not device == self._EffectController__assigned_device:
            self._EffectController__bank = 0
            if not self._EffectController__assigned_device == None:
                self._EffectController__assigned_device.remove_parameters_listener(self._EffectController__parameter_list_of_device_changed)
            self._EffectController__show_bank = False
            self._EffectController__assigned_device = device
            if not self._EffectController__assigned_device == None:
                self._EffectController__assigned_device.add_parameters_listener(self._EffectController__parameter_list_of_device_changed)

    def __parameter_list_of_device_changed(self):
        self._EffectController__reassign_strips()

    def __number_of_parameter_banks(self):
        result = 0
        if self._EffectController__assigned_device != None:
            param_count = len(self._EffectController__assigned_device.parameters)
            result = int(old_div(param_count, 8)) + int(param_count % 8 != 0)
        return result


class EffectChannelStrip(object):

    def __init__(self, mixer_controller_parent):
        self._EffectChannelStrip__mixer_controller = mixer_controller_parent
        self._EffectChannelStrip__assigned_parameter = None

    def assigned_parameter(self):
        return self._EffectChannelStrip__assigned_parameter

    def set_assigned_parameter(self, parameter):
        self._EffectChannelStrip__assigned_parameter = parameter

    def on_button_pressed(self):
        if self._EffectChannelStrip__assigned_parameter:
            if self._EffectChannelStrip__assigned_parameter.is_enabled:
                if self._EffectChannelStrip__assigned_parameter.is_quantized:
                    if self._EffectChannelStrip__assigned_parameter.value + 1 > self._EffectChannelStrip__assigned_parameter.max:
                        self._EffectChannelStrip__assigned_parameter.value = self._EffectChannelStrip__assigned_parameter.min
                    else:
                        self._EffectChannelStrip__assigned_parameter.value = self._EffectChannelStrip__assigned_parameter.value + 1
                else:
                    self._EffectChannelStrip__assigned_parameter.value = self._EffectChannelStrip__assigned_parameter.default_value

    def on_encoder_moved(self, cc_value):
        pass