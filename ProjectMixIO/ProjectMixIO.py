# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ProjectMixIO\ProjectMixIO.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 10214 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
import Live
from MackieControl.ChannelStrip import ChannelStrip, MasterChannelStrip
import MackieControl.ChannelStripController as ChannelStripController
from MackieControl.consts import *
import MackieControl.MainDisplay as MainDisplay
import MackieControl.MainDisplayController as MainDisplayController
import MackieControl.SoftwareController as SoftwareController
import MackieControl.Transport as Transport

class ProjectMixIO(object):

    def __init__(self, c_instance):
        self._ProjectMixIO__c_instance = c_instance
        self._ProjectMixIO__components = []
        self._ProjectMixIO__main_display = MainDisplay(self)
        self._ProjectMixIO__components.append(self._ProjectMixIO__main_display)
        self._ProjectMixIO__main_display_controller = MainDisplayController(self, self._ProjectMixIO__main_display)
        self._ProjectMixIO__components.append(self._ProjectMixIO__main_display_controller)
        self._ProjectMixIO__software_controller = SoftwareController(self)
        self._ProjectMixIO__components.append(self._ProjectMixIO__software_controller)
        self._ProjectMixIO__transport = Transport(self)
        self._ProjectMixIO__components.append(self._ProjectMixIO__transport)
        self._ProjectMixIO__channel_strips = [ChannelStrip(self, i) for i in range(NUM_CHANNEL_STRIPS)]
        for s in self._ProjectMixIO__channel_strips:
            self._ProjectMixIO__components.append(s)

        self._ProjectMixIO__master_strip = MasterChannelStrip(self)
        self._ProjectMixIO__components.append(self._ProjectMixIO__master_strip)
        self._ProjectMixIO__channel_strip_controller = ChannelStripController(self, self._ProjectMixIO__channel_strips, self._ProjectMixIO__master_strip, self._ProjectMixIO__main_display_controller)
        self._ProjectMixIO__components.append(self._ProjectMixIO__channel_strip_controller)
        self._ProjectMixIO__shift_is_pressed = False
        self._ProjectMixIO__option_is_pressed = False
        self._ProjectMixIO__ctrl_is_pressed = False
        self._ProjectMixIO__alt_is_pressed = False
        self.is_pro_version = False

    def disconnect(self):
        for c in self._ProjectMixIO__components:
            c.destroy()

    def disconnect(self):
        for c in self._ProjectMixIO__components:
            c.destroy()

    def connect_script_instances(self, instanciated_scripts):
        pass

    def application(self):
        return Live.Application.get_application()

    def song(self):
        return self._ProjectMixIO__c_instance.song()

    def handle(self):
        return self._ProjectMixIO__c_instance.handle()

    def refresh_state(self):
        for c in self._ProjectMixIO__components:
            c.refresh_state()

    def is_extension(self):
        return False

    def request_rebuild_midi_map(self):
        self._ProjectMixIO__c_instance.request_rebuild_midi_map()

    def can_lock_to_devices(self):
        return False

    def build_midi_map(self, midi_map_handle):
        for s in self._ProjectMixIO__channel_strips:
            s.build_midi_map(midi_map_handle)

        self._ProjectMixIO__master_strip.build_midi_map(midi_map_handle)
        for i in range(SID_FIRST, SID_LAST + 1):
            if i not in function_key_control_switch_ids:
                Live.MidiMap.forward_midi_note(self.handle(), midi_map_handle, 0, i)

        Live.MidiMap.forward_midi_cc(self.handle(), midi_map_handle, 0, JOG_WHEEL_CC_NO)

    def update_display(self):
        for c in self._ProjectMixIO__components:
            c.on_update_display_timer()

    def send_midi(self, midi_event_bytes):
        self._ProjectMixIO__c_instance.send_midi(midi_event_bytes)

    def receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS or midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            note = midi_bytes[1]
            value = BUTTON_PRESSED if midi_bytes[2] > 0 else BUTTON_RELEASED
            if note in range(SID_FIRST, SID_LAST + 1):
                if note in display_switch_ids:
                    self.handle_display_switch_ids(note, value)
                if note in channel_strip_switch_ids + fader_touch_switch_ids:
                    for s in self._ProjectMixIO__channel_strips:
                        s.handle_channel_strip_switch_ids(note, value)

                if note in channel_strip_control_switch_ids:
                    self._ProjectMixIO__channel_strip_controller.handle_assignment_switch_ids(note, value)
                if note in function_key_control_switch_ids:
                    self._ProjectMixIO__software_controller.handle_function_key_switch_ids(note, value)
                if note in software_controls_switch_ids:
                    self._ProjectMixIO__software_controller.handle_software_controls_switch_ids(note, value)
                if note in transport_control_switch_ids:
                    self._ProjectMixIO__transport.handle_transport_switch_ids(note, value)
                if note in marker_control_switch_ids:
                    self._ProjectMixIO__transport.handle_marker_switch_ids(note, value)
                if note in jog_wheel_switch_ids:
                    self._ProjectMixIO__transport.handle_jog_wheel_switch_ids(note, value)
        else:
            if midi_bytes[0] & 240 == CC_STATUS:
                cc_no = midi_bytes[1]
                cc_value = midi_bytes[2]
                if cc_no == JOG_WHEEL_CC_NO:
                    self._ProjectMixIO__transport.handle_jog_wheel_rotation(cc_value)
                else:
                    if cc_no in range(FID_PANNING_BASE, FID_PANNING_BASE + NUM_CHANNEL_STRIPS):
                        for s in self._ProjectMixIO__channel_strips:
                            s.handle_vpot_rotation(cc_no - FID_PANNING_BASE, cc_value)

    def shift_is_pressed(self):
        return self._ProjectMixIO__shift_is_pressed

    def set_shift_is_pressed(self, pressed):
        self._ProjectMixIO__shift_is_pressed = pressed

    def option_is_pressed(self):
        return self._ProjectMixIO__option_is_pressed

    def set_option_is_pressed(self, pressed):
        self._ProjectMixIO__option_is_pressed = pressed

    def control_is_pressed(self):
        return self._ProjectMixIO__control_is_pressed or self._ProjectMixIO__option_is_pressed

    def set_control_is_pressed(self, pressed):
        self._ProjectMixIO__control_is_pressed = pressed

    def alt_is_pressed(self):
        return self._ProjectMixIO__alt_is_pressed

    def set_alt_is_pressed(self, pressed):
        self._ProjectMixIO__alt_is_pressed = pressed

    def force_time_display_update(self):
        pass

    def handle_display_switch_ids(self, switch_id, value):
        if switch_id == SID_DISPLAY_NAME_VALUE:
            if value == BUTTON_PRESSED:
                self._ProjectMixIO__channel_strip_controller.toggle_meter_mode()