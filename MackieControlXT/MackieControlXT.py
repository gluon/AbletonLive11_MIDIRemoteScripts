# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControlXT\MackieControlXT.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 8475 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
import Live
import MackieControl.ChannelStrip as ChannelStrip
from MackieControl.consts import *
import MackieControl.MainDisplay as MainDisplay

class MackieControlXT(object):

    def __init__(self, c_instance):
        self._MackieControlXT__c_instance = c_instance
        self._MackieControlXT__components = []
        self._MackieControlXT__main_display = MainDisplay(self)
        self._MackieControlXT__components.append(self._MackieControlXT__main_display)
        self._MackieControlXT__channel_strips = [ChannelStrip(self, i) for i in range(NUM_CHANNEL_STRIPS)]
        for s in self._MackieControlXT__channel_strips:
            self._MackieControlXT__components.append(s)

        self._MackieControlXT__mackie_control_main = None
        self.is_pro_version = False
        self._received_firmware_version = False
        self._refresh_state_next_time = 0

    def disconnect(self):
        for c in self._MackieControlXT__components:
            c.destroy()

    def connect_script_instances(self, instanciated_scripts):
        pass

    def request_firmware_version(self):
        if not self._received_firmware_version:
            self.send_midi((
             240, 0, 0, 102, SYSEX_DEVICE_TYPE_XT, 19, 0, 247))

    def is_extension(self):
        return True

    def mackie_control_main(self, mackie_control_main):
        return self._MackieControlXT__mackie_control_main

    def set_mackie_control_main(self, mackie_control_main):
        self._MackieControlXT__mackie_control_main = mackie_control_main

    def channel_strips(self):
        return self._MackieControlXT__channel_strips

    def main_display(self):
        return self._MackieControlXT__main_display

    def shift_is_pressed(self):
        is_pressed = False
        if self._MackieControlXT__mackie_control_main != None:
            is_pressed = self._MackieControlXT__mackie_control_main.shift_is_pressed()
        return is_pressed

    def option_is_pressed(self):
        is_pressed = False
        if self._MackieControlXT__mackie_control_main != None:
            is_pressed = self._MackieControlXT__mackie_control_main.option_is_pressed()
        return is_pressed

    def control_is_pressed(self):
        is_pressed = False
        if self._MackieControlXT__mackie_control_main != None:
            is_pressed = self._MackieControlXT__mackie_control_main.control_is_pressed()
        return is_pressed

    def alt_is_pressed(self):
        is_pressed = False
        if self._MackieControlXT__mackie_control_main != None:
            is_pressed = self._MackieControlXT__mackie_control_main.alt_is_pressed()
        return is_pressed

    def application(self):
        return Live.Application.get_application()

    def song(self):
        return self._MackieControlXT__c_instance.song()

    def handle(self):
        return self._MackieControlXT__c_instance.handle()

    def refresh_state(self):
        for c in self._MackieControlXT__components:
            c.refresh_state()

        self.request_firmware_version()
        self._refresh_state_next_time = 30

    def request_rebuild_midi_map(self):
        self._MackieControlXT__c_instance.request_rebuild_midi_map()

    def build_midi_map(self, midi_map_handle):
        for s in self._MackieControlXT__channel_strips:
            s.build_midi_map(midi_map_handle)

        for i in channel_strip_switch_ids + fader_touch_switch_ids:
            Live.MidiMap.forward_midi_note(self.handle(), midi_map_handle, 0, i)

    def update_display(self):
        if self._refresh_state_next_time > 0:
            self._refresh_state_next_time -= 1
            if self._refresh_state_next_time == 0:
                for c in self._MackieControlXT__components:
                    c.refresh_state()

                self.request_firmware_version()
        for c in self._MackieControlXT__components:
            c.on_update_display_timer()

    def send_midi(self, midi_event_bytes):
        self._MackieControlXT__c_instance.send_midi(midi_event_bytes)

    def receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS or midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            note = midi_bytes[1]
            value = BUTTON_PRESSED if midi_bytes[2] > 0 else BUTTON_RELEASED
            if note in range(SID_FIRST, SID_LAST + 1):
                if note in channel_strip_switch_ids + fader_touch_switch_ids:
                    for s in self._MackieControlXT__channel_strips:
                        s.handle_channel_strip_switch_ids(note, value)

        else:
            if midi_bytes[0] & 240 == CC_STATUS:
                cc_no = midi_bytes[1]
                cc_value = midi_bytes[2]
                if cc_no in range(FID_PANNING_BASE, FID_PANNING_BASE + NUM_CHANNEL_STRIPS):
                    for s in self._MackieControlXT__channel_strips:
                        s.handle_vpot_rotation(cc_no - FID_PANNING_BASE, cc_value)

            else:
                pass
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