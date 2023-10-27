# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL_Classic\RemoteSL.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 11556 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, str
import Live, MidiRemoteScript
from _Generic.util import DeviceAppointer
from .consts import *
from .DisplayController import DisplayController
from .EffectController import EffectController
from .MixerController import MixerController

class RemoteSL(object):

    def __init__(self, c_instance):
        self._RemoteSL__c_instance = c_instance
        self._RemoteSL__automap_has_control = False
        self._RemoteSL__display_controller = DisplayController(self)
        self._RemoteSL__effect_controller = EffectController(self, self._RemoteSL__display_controller)
        self._RemoteSL__mixer_controller = MixerController(self, self._RemoteSL__display_controller)
        self._RemoteSL__components = [
         self._RemoteSL__effect_controller,
         self._RemoteSL__mixer_controller,
         self._RemoteSL__display_controller]
        self._RemoteSL__update_hardware_delay = -1
        self._device_appointer = DeviceAppointer(song=(self.song()),
          appointed_device_setter=(self._set_appointed_device))

    def disconnect(self):
        for c in self._RemoteSL__components:
            c.disconnect()

        self._device_appointer.disconnect()
        self.send_midi(ALL_LEDS_OFF_MESSAGE)
        self.send_midi(GOOD_BYE_SYSEX_MESSAGE)

    def application(self):
        return Live.Application.get_application()

    def song(self):
        return self._RemoteSL__c_instance.song()

    def suggest_input_port(self):
        return 'RemoteSL'

    def suggest_output_port(self):
        return 'RemoteSL'

    def can_lock_to_devices(self):
        return True

    def lock_to_device(self, device):
        self._RemoteSL__effect_controller.lock_to_device(device)

    def unlock_from_device(self, device):
        self._RemoteSL__effect_controller.unlock_from_device(device)

    def _set_appointed_device(self, device):
        self._RemoteSL__effect_controller.set_appointed_device(device)

    def toggle_lock(self):
        self._RemoteSL__c_instance.toggle_lock()

    def suggest_map_mode(self, cc_no, channel):
        result = Live.MidiMap.MapMode.absolute
        if cc_no in fx_encoder_row_ccs:
            result = Live.MidiMap.MapMode.relative_smooth_signed_bit
        return result

    def restore_bank(self, bank):
        self._RemoteSL__effect_controller.restore_bank(bank)

    def supports_pad_translation(self):
        return True

    def show_message(self, message):
        self._RemoteSL__c_instance.show_message(message)

    def instance_identifier(self):
        return self._RemoteSL__c_instance.instance_identifier()

    def connect_script_instances(self, instanciated_scripts):
        pass

    def request_rebuild_midi_map(self):
        self._RemoteSL__c_instance.request_rebuild_midi_map()

    def send_midi(self, midi_event_bytes):
        if not self._RemoteSL__automap_has_control:
            self._RemoteSL__c_instance.send_midi(midi_event_bytes)

    def refresh_state(self):
        self._RemoteSL__update_hardware_delay = 5

    def __update_hardware(self):
        self._RemoteSL__automap_has_control = False
        self.send_midi(WELCOME_SYSEX_MESSAGE)
        for c in self._RemoteSL__components:
            c.refresh_state()

    def build_midi_map(self, midi_map_handle):
        if not self._RemoteSL__automap_has_control:
            for c in self._RemoteSL__components:
                c.build_midi_map(self._RemoteSL__c_instance.handle(), midi_map_handle)

        self._RemoteSL__c_instance.set_pad_translation(PAD_TRANSLATION)

    def update_display(self):
        if self._RemoteSL__update_hardware_delay > 0:
            self._RemoteSL__update_hardware_delay -= 1
            if self._RemoteSL__update_hardware_delay == 0:
                self._RemoteSL__update_hardware()
                self._RemoteSL__update_hardware_delay = -1
        for c in self._RemoteSL__components:
            c.update_display()

    def receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 in (NOTE_ON_STATUS, NOTE_OFF_STATUS):
            channel = midi_bytes[0] & 15
            note = midi_bytes[1]
            velocity = midi_bytes[2]
            if note in fx_notes:
                self._RemoteSL__effect_controller.receive_midi_note(note, velocity)
            else:
                if note in mx_notes:
                    self._RemoteSL__mixer_controller.receive_midi_note(note, velocity)
                else:
                    print('unknown MIDI message %s' % str(midi_bytes))
        else:
            if midi_bytes[0] & 240 == CC_STATUS:
                channel = midi_bytes[0] & 15
                cc_no = midi_bytes[1]
                cc_value = midi_bytes[2]
                if cc_no in fx_ccs:
                    self._RemoteSL__effect_controller.receive_midi_cc(cc_no, cc_value)
                else:
                    if cc_no in mx_ccs:
                        self._RemoteSL__mixer_controller.receive_midi_cc(cc_no, cc_value)
                    else:
                        print('unknown MIDI message %s' % str(midi_bytes))
            else:
                if midi_bytes[0] == 240:
                    if len(midi_bytes) == 13:
                        if midi_bytes[1:4] == (0, 32, 41):
                            if not midi_bytes[8] == ABLETON_PID or midi_bytes[10] == 1:
                                self._RemoteSL__automap_has_control = midi_bytes[11] == 0
                                support_mkII = midi_bytes[6] * 100 + midi_bytes[7] >= 1800
                                if not self._RemoteSL__automap_has_control:
                                    self.send_midi(ALL_LEDS_OFF_MESSAGE)
                                for c in self._RemoteSL__components:
                                    c.set_support_mkII(support_mkII)
                                    if not self._RemoteSL__automap_has_control:
                                        c.refresh_state()

                                self.request_rebuild_midi_map()
                else:
                    print('unknown MIDI message %s' % str(midi_bytes))