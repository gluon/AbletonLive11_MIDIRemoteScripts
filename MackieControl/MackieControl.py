# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\MackieControl.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 14004 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
import Live, MidiRemoteScript
from .ChannelStrip import ChannelStrip, MasterChannelStrip
from .ChannelStripController import ChannelStripController
from .consts import *
from .MainDisplay import MainDisplay
from .MainDisplayController import MainDisplayController
from .SoftwareController import SoftwareController
from .TimeDisplay import TimeDisplay
from .Transport import Transport

class MackieControl(object):

    def __init__(self, c_instance):
        self._MackieControl__c_instance = c_instance
        self._MackieControl__components = []
        self._MackieControl__main_display = MainDisplay(self)
        self._MackieControl__components.append(self._MackieControl__main_display)
        self._MackieControl__main_display_controller = MainDisplayController(self, self._MackieControl__main_display)
        self._MackieControl__components.append(self._MackieControl__main_display_controller)
        self._MackieControl__time_display = TimeDisplay(self)
        self._MackieControl__components.append(self._MackieControl__time_display)
        self._MackieControl__software_controller = SoftwareController(self)
        self._MackieControl__components.append(self._MackieControl__software_controller)
        self._MackieControl__transport = Transport(self)
        self._MackieControl__components.append(self._MackieControl__transport)
        self._MackieControl__channel_strips = [ChannelStrip(self, i) for i in range(NUM_CHANNEL_STRIPS)]
        for s in self._MackieControl__channel_strips:
            self._MackieControl__components.append(s)

        self._MackieControl__master_strip = MasterChannelStrip(self)
        self._MackieControl__components.append(self._MackieControl__master_strip)
        self._MackieControl__channel_strip_controller = ChannelStripController(self, self._MackieControl__channel_strips, self._MackieControl__master_strip, self._MackieControl__main_display_controller)
        self._MackieControl__components.append(self._MackieControl__channel_strip_controller)
        self._MackieControl__shift_is_pressed = False
        self._MackieControl__option_is_pressed = False
        self._MackieControl__ctrl_is_pressed = False
        self._MackieControl__alt_is_pressed = False
        self.is_pro_version = False
        self._received_firmware_version = False
        self._refresh_state_next_time = 0

    def disconnect(self):
        for c in self._MackieControl__components:
            c.destroy()

    def connect_script_instances(self, instanciated_scripts):
        try:
            import MackieControlXT.MackieControlXT as MackieControlXT
        except:
            print('failed to load the MackieControl XT script (might not be installed)')

        found_self = False
        right_extensions = []
        left_extensions = []
        for s in instanciated_scripts:
            if s is self:
                found_self = True
            if isinstance(s, MackieControlXT):
                s.set_mackie_control_main(self)
                if found_self:
                    right_extensions.append(s)
                else:
                    left_extensions.append(s)

        self._MackieControl__main_display_controller.set_controller_extensions(left_extensions, right_extensions)
        self._MackieControl__channel_strip_controller.set_controller_extensions(left_extensions, right_extensions)

    def request_firmware_version(self):
        if not self._received_firmware_version:
            self.send_midi((240, 0, 0, 102, SYSEX_DEVICE_TYPE, 19, 0, 247))

    def application(self):
        return Live.Application.get_application()

    def song(self):
        return self._MackieControl__c_instance.song()

    def handle(self):
        return self._MackieControl__c_instance.handle()

    def refresh_state(self):
        for c in self._MackieControl__components:
            c.refresh_state()

        self.request_firmware_version()
        self._refresh_state_next_time = 30

    def is_extension(self):
        return False

    def request_rebuild_midi_map(self):
        self._MackieControl__c_instance.request_rebuild_midi_map()

    def build_midi_map(self, midi_map_handle):
        for s in self._MackieControl__channel_strips:
            s.build_midi_map(midi_map_handle)

        self._MackieControl__master_strip.build_midi_map(midi_map_handle)
        for i in range(SID_FIRST, SID_LAST + 1):
            if i not in function_key_control_switch_ids:
                Live.MidiMap.forward_midi_note(self.handle(), midi_map_handle, 0, i)

        Live.MidiMap.forward_midi_cc(self.handle(), midi_map_handle, 0, JOG_WHEEL_CC_NO)

    def update_display(self):
        if self._refresh_state_next_time > 0:
            self._refresh_state_next_time -= 1
            if self._refresh_state_next_time == 0:
                for c in self._MackieControl__components:
                    c.refresh_state()

                self.request_firmware_version()
        for c in self._MackieControl__components:
            c.on_update_display_timer()

    def send_midi(self, midi_event_bytes):
        self._MackieControl__c_instance.send_midi(midi_event_bytes)

    def receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS or midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            note = midi_bytes[1]
            value = BUTTON_PRESSED if midi_bytes[2] > 0 else BUTTON_RELEASED
            if note in range(SID_FIRST, SID_LAST + 1):
                if note in display_switch_ids:
                    self._MackieControl__handle_display_switch_ids(note, value)
                if note in channel_strip_switch_ids + fader_touch_switch_ids:
                    for s in self._MackieControl__channel_strips:
                        s.handle_channel_strip_switch_ids(note, value)

                if note in channel_strip_control_switch_ids:
                    self._MackieControl__channel_strip_controller.handle_assignment_switch_ids(note, value)
                if note in function_key_control_switch_ids:
                    self._MackieControl__software_controller.handle_function_key_switch_ids(note, value)
                if note in software_controls_switch_ids:
                    self._MackieControl__software_controller.handle_software_controls_switch_ids(note, value)
                if note in transport_control_switch_ids:
                    self._MackieControl__transport.handle_transport_switch_ids(note, value)
                if note in marker_control_switch_ids:
                    self._MackieControl__transport.handle_marker_switch_ids(note, value)
                if note in jog_wheel_switch_ids:
                    self._MackieControl__transport.handle_jog_wheel_switch_ids(note, value)
        else:
            if midi_bytes[0] & 240 == CC_STATUS:
                cc_no = midi_bytes[1]
                cc_value = midi_bytes[2]
                if cc_no == JOG_WHEEL_CC_NO:
                    self._MackieControl__transport.handle_jog_wheel_rotation(cc_value)
                else:
                    if cc_no in range(FID_PANNING_BASE, FID_PANNING_BASE + NUM_CHANNEL_STRIPS):
                        for s in self._MackieControl__channel_strips:
                            s.handle_vpot_rotation(cc_no - FID_PANNING_BASE, cc_value)

            else:
                if midi_bytes[0] == 240:
                    if len(midi_bytes) == 12:
                        if midi_bytes[5] == 20:
                            version_bytes = midi_bytes[6:-2]
                            major_version = version_bytes[1]
                            self.is_pro_version = major_version > 50
                            self._received_firmware_version = True

    def can_lock_to_devices(self):
        return False

    def suggest_input_port(self):
        return ''

    def suggest_output_port(self):
        return ''

    def suggest_map_mode(self, cc_no, channel):
        result = Live.MidiMap.MapMode.absolute
        if cc_no in range(FID_PANNING_BASE, FID_PANNING_BASE + NUM_CHANNEL_STRIPS):
            result = Live.MidiMap.MapMode.relative_signed_bit
        return result

    def shift_is_pressed(self):
        return self._MackieControl__shift_is_pressed

    def set_shift_is_pressed(self, pressed):
        self._MackieControl__shift_is_pressed = pressed

    def option_is_pressed(self):
        return self._MackieControl__option_is_pressed

    def set_option_is_pressed(self, pressed):
        self._MackieControl__option_is_pressed = pressed

    def control_is_pressed(self):
        return self._MackieControl__control_is_pressed

    def set_control_is_pressed(self, pressed):
        self._MackieControl__control_is_pressed = pressed

    def alt_is_pressed(self):
        return self._MackieControl__alt_is_pressed

    def set_alt_is_pressed(self, pressed):
        self._MackieControl__alt_is_pressed = pressed

    def __handle_display_switch_ids(self, switch_id, value):
        if switch_id == SID_DISPLAY_NAME_VALUE:
            if value == BUTTON_PRESSED:
                self._MackieControl__channel_strip_controller.toggle_meter_mode()
        else:
            if switch_id == SID_DISPLAY_SMPTE_BEATS:
                if value == BUTTON_PRESSED:
                    self._MackieControl__time_display.toggle_mode()