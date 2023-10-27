# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_APC\APC.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 8257 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range, str
import Live
import _Framework.ControlSurface as ControlSurface
MANUFACTURER_ID = 71
ABLETON_MODE = 65
DO_COMBINE = Live.Application.combine_apcs()

class APC(ControlSurface):
    _active_instances = []

    def _combine_active_instances():
        support_devices = False
        for instance in APC._active_instances:
            support_devices |= instance._device_component != None

        track_offset = 0
        if APC._active_instances:
            first_instance = APC._active_instances[0]
            track_offset = first_instance.highlighting_session_component().track_offset()
        for instance in APC._active_instances:
            instance._activate_combination_mode(track_offset, support_devices)
            track_offset += instance.highlighting_session_component().width()

    _combine_active_instances = staticmethod(_combine_active_instances)

    def __init__(self, *a, **k):
        (super(APC, self).__init__)(*a, **k)
        self._suppress_session_highlight = True
        self._suppress_send_midi = True
        self._suggested_input_port = 'Akai ' + self.__class__.__name__
        self._suggested_output_port = 'Akai ' + self.__class__.__name__
        self._device_id = 0
        self._common_channel = 0
        self._dongle_challenge = (
         Live.Application.get_random_int(0, 2000000),
         Live.Application.get_random_int(2000001, 4000000))
        self._identity_response_pending = False

    def disconnect(self):
        self._do_uncombine()
        super(APC, self).disconnect()

    def refresh_state(self):
        super(APC, self).refresh_state()
        self.schedule_message(5, self._update_hardware)

    def handle_sysex(self, midi_bytes):
        self._suppress_send_midi = False
        if midi_bytes[3] == 6 and midi_bytes[4] == 2:
            self._on_identity_response(midi_bytes)
        else:
            if midi_bytes[4] == 81:
                self._on_dongle_response(midi_bytes)
            else:
                pass

    def _on_identity_response(self, midi_bytes):
        if midi_bytes[5] == MANUFACTURER_ID:
            if midi_bytes[6] == self._product_model_id_byte():
                if self._identity_response_pending:
                    self._identity_response_pending = False
                    version_bytes = midi_bytes[9:13]
                    self._device_id = midi_bytes[13]
                    self._send_introduction_message()
                    self.schedule_message(2, self._send_dongle_challenge)
                    self._log_version(version_bytes)

    def _on_dongle_response(self, midi_bytes):
        if midi_bytes[1] == MANUFACTURER_ID:
            if midi_bytes[3] == self._product_model_id_byte():
                if midi_bytes[2] == self._device_id:
                    if midi_bytes[5] == 0:
                        if midi_bytes[6] == 16:
                            response = [
                             int(0), int(0)]
                            for index in range(8):
                                response[0] += int(midi_bytes[7 + index] & 15) << 4 * (7 - index)
                                response[1] += int(midi_bytes[15 + index] & 15) << 4 * (7 - index)

                            expected_response = Live.Application.encrypt_challenge(self._dongle_challenge[0], self._dongle_challenge[1])
                            if [
                             int(expected_response[0]), int(expected_response[1])] == response:
                                self._on_handshake_successful()

    def _on_handshake_successful(self):
        self._suppress_session_highlight = False
        for component in self.components:
            component.set_enabled(True)

        self._on_selected_track_changed()
        self._do_combine()

    def _update_hardware(self):
        self._suppress_send_midi = True
        self._suppress_session_highlight = True
        with self.component_guard():
            for component in self.components:
                component.set_enabled(False)

        self._suppress_send_midi = False
        self._do_uncombine()
        self._send_identity_request()

    def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
        if not self._suppress_session_highlight or (
         track_offset,
         scene_offset,
         width,
         height) == (-1, -1, -1, -1):
            super(APC, self)._set_session_highlight(track_offset, scene_offset, width, height, include_return_tracks)

    def _send_midi(self, midi_bytes, optimized=None):
        if not self._suppress_send_midi:
            return super(APC, self)._send_midi(midi_bytes, optimized=optimized)
        return False

    def _send_identity_request(self):
        self._identity_response_pending = True
        self._send_midi((240, 126, 0, 6, 1, 247))

    def _send_introduction_message(self, mode_byte=ABLETON_MODE):
        self._send_midi((
         240,
         MANUFACTURER_ID,
         self._device_id,
         self._product_model_id_byte(),
         96,
         0,
         4,
         mode_byte,
         self.application().get_major_version(),
         self.application().get_minor_version(),
         self.application().get_bugfix_version(),
         247))

    def _send_dongle_challenge(self):
        challenge1 = [
         0,0,0,0,0,0,0,0]
        challenge2 = [0,0,0,0,0,0,0,0]
        for index in range(8):
            challenge1[index] = self._dongle_challenge[0] >> 4 * (7 - index) & 15
            challenge2[index] = self._dongle_challenge[1] >> 4 * (7 - index) & 15

        dongle_message = (
         240, MANUFACTURER_ID, self._device_id, self._product_model_id_byte(), 80, 0, 16) + tuple(challenge1) + tuple(challenge2) + (247, )
        self._send_midi(dongle_message)

    def _log_version(self, version_bytes):
        message = self.__class__.__name__ + ': Got response from controller, version ' + str((version_bytes[0] << 4) + version_bytes[1]) + '.' + str((version_bytes[2] << 4) + version_bytes[3])
        self.log_message(message)

    def _activate_combination_mode(self, track_offset, support_devices):
        self.highlighting_session_component().link_with_track_offset(track_offset)

    def _should_combine(self):
        return DO_COMBINE

    def _do_combine(self):
        if self._should_combine():
            if self not in APC._active_instances:
                APC._active_instances = sorted((APC._active_instances + [self]),
                  key=(lambda x: x.instance_identifier()
))
                APC._combine_active_instances()

    def _do_uncombine(self):
        if self in APC._active_instances:
            APC._active_instances.remove(self)
            self.highlighting_session_component().unlink()
            APC._combine_active_instances()

    def _product_model_id_byte(self):
        raise AssertionError('Function _product_model_id_byte must be overridden by subclass')