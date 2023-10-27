# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_Mini32\AxiomAirMini32.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 5765 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.ChannelStripComponent as ChannelStripComponent
import _Framework.ControlSurface as ControlSurface
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
import _Framework.MixerComponent as MixerComponent
import _Framework.ModeSelectorComponent as ModeSelectorComponent
import _Framework.SessionComponent as SessionComponent
import _Framework.TransportComponent as TransportComponent
import Axiom_DirectLink.BestBankDeviceComponent as BestBankDeviceComponent
from .DeviceNavComponent import DeviceNavComponent
from .EncoderMixerModeSelector import EncoderMixerModeSelector
from .MixerOrDeviceModeSelector import MixerOrDeviceModeSelector
SYSEX_START = (240, 0, 1, 5, 32, 127)
ENGAGE_HYPERCONTROL = (32, 60, 247)
DISABLE_HYPERCONTROL = (32, 0, 247)
NUM_TRACKS = 8
GLOBAL_CHANNEL = 15
PAD_TRANSLATIONS = ((0, 0, 85, 14), (1, 0, 86, 14), (2, 0, 87, 14), (3, 0, 88, 14),
                    (0, 1, 81, 14), (1, 1, 82, 14), (2, 1, 83, 14), (3, 1, 84, 14),
                    (0, 2, 85, 15), (1, 2, 86, 15), (2, 2, 87, 15), (3, 2, 88, 15),
                    (0, 3, 81, 15), (1, 3, 82, 15), (2, 3, 83, 15), (3, 3, 84, 15))

def make_button(cc_no):
    is_momentary = True
    return ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, cc_no)


def make_encoder(cc_no):
    return EncoderElement(MIDI_CC_TYPE, GLOBAL_CHANNEL, cc_no, Live.MidiMap.MapMode.absolute)


class AxiomAirMini32(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self._suggested_input_port = 'HyperControl'
            self._suggested_output_port = 'HyperControl'
            self.set_pad_translations(PAD_TRANSLATIONS)
            stop_button = make_button(116)
            play_button = make_button(117)
            record_button = make_button(118)
            select_button = make_button(98)
            nav_left_button = make_button(99)
            nav_right_button = make_button(100)
            nav_up_button = make_button(101)
            nav_down_button = make_button(102)
            mixer_modes_toggle = make_button(58)
            mixer_or_device_toggle = make_button(59)
            hypercontrol_mode_toggle = make_button(60)
            encoders = tuple([make_encoder(33 + index) for index in range(8)])
            transport = TransportComponent()
            transport.set_stop_button(stop_button)
            transport.set_play_button(play_button)
            transport.set_record_button(record_button)
            session = SessionComponent(8, 0)
            device = BestBankDeviceComponent(device_selection_follows_track_selection=True)
            self.set_device_component(device)
            device_nav = DeviceNavComponent()
            mixer = SpecialMixerComponent(NUM_TRACKS)
            session.set_mixer(mixer)
            mixer_encoder_modes = EncoderMixerModeSelector(mixer)
            mixer_encoder_modes.set_mode_toggle(mixer_modes_toggle)
            mixer_or_device = MixerOrDeviceModeSelector(encoders, select_button, nav_up_button, nav_down_button, nav_left_button, nav_right_button, mixer, session, device, mixer_encoder_modes, device_nav)
            mixer_or_device.set_mode_buttons((
             mixer_modes_toggle, mixer_or_device_toggle, hypercontrol_mode_toggle))

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._send_midi, SYSEX_START + ENGAGE_HYPERCONTROL)
        for component in self.components:
            if isinstance(component, ModeSelectorComponent):
                component.set_mode(0)

    def handle_sysex(self, midi_bytes):
        pass

    def disconnect(self):
        ControlSurface.disconnect(self)
        self._send_midi(SYSEX_START + DISABLE_HYPERCONTROL)


class SpecialMixerComponent(MixerComponent):

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        return SpecialChanStripComponent()


class SpecialChanStripComponent(ChannelStripComponent):

    def set_arm_button(self, button):
        if button != self._arm_button:
            if self._arm_button != None:
                self._arm_button.remove_value_listener(self._arm_value)
                self._arm_button.reset()
            self._arm_pressed = False
            self._arm_button = button
            if self._arm_button != None:
                self._arm_button.add_value_listener(self._arm_value)
            self.update()