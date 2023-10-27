# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_3rd_Gen\Oxygen_3rd_Gen.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6855 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.ChannelStripComponent as ChannelStripComponent
import _Framework.ClipSlotComponent as ClipSlotComponent
import _Framework.ControlElement as ControlElement
import _Framework.ControlSurface as ControlSurface
import _Framework.DeviceComponent as DeviceComponent
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import *
import _Framework.ModeSelectorComponent as ModeSelectorComponent
import _Framework.SceneComponent as SceneComponent
import _Framework.SessionComponent as SessionComponent
import _Framework.SliderElement as SliderElement
import _Framework.TransportComponent as TransportComponent
from .SpecialMixerComponent import SpecialMixerComponent
from .TransportViewModeSelector import TransportViewModeSelector
IDENTITY_REQUEST = (240, 126, 127, 6, 1, 247)
IDENTITY_RESPONSE = (240, 126, 127, 6, 2)
NUM_TRACKS = 8
GLOBAL_CHANNEL = 15

class Oxygen_3rd_Gen(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            is_momentary = True
            self._suggested_input_port = 'Oxygen'
            self._suggested_output_port = 'Oxygen'
            self._has_slider_section = True
            self._shift_button = ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 57)
            self._shift_button.add_value_listener(self._shift_value)
            self._mixer = SpecialMixerComponent(NUM_TRACKS)
            self._mute_solo_buttons = []
            self._track_up_button = ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 111)
            self._track_down_button = ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 110)
            self._master_slider = SliderElement(MIDI_CC_TYPE, GLOBAL_CHANNEL, 41)
            for index in range(NUM_TRACKS):
                self._mute_solo_buttons.append(ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 49 + index))
                self._mixer.channel_strip(index).set_volume_control(SliderElement(MIDI_CC_TYPE, GLOBAL_CHANNEL, 33 + index))

            self._shift_value(0)
            self._mixer.master_strip().set_volume_control(self._master_slider)
            self._mixer.selected_strip().set_volume_control(None)
            device = DeviceComponent(device_selection_follows_track_selection=True)
            device.set_parameter_controls(tuple([EncoderElement(MIDI_CC_TYPE, GLOBAL_CHANNEL, 17 + index, Live.MidiMap.MapMode.absolute) for index in range(8)]))
            self.set_device_component(device)
            ffwd_button = ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 115)
            rwd_button = ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 114)
            loop_button = ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 113)
            transport = TransportComponent()
            transport.set_stop_button(ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 116))
            transport.set_play_button(ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 117))
            transport.set_record_button(ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, 118))
            session = SessionComponent(0, 0)
            transport_view_modes = TransportViewModeSelector(transport, session, ffwd_button, rwd_button, loop_button)

    def disconnect(self):
        self._shift_button.remove_value_listener(self._shift_value)
        self._shift_button = None
        ControlSurface.disconnect(self)

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._send_midi, IDENTITY_REQUEST)

    def handle_sysex(self, midi_bytes):
        if midi_bytes[0:5] == IDENTITY_RESPONSE:
            if midi_bytes[10] == 38:
                self._mixer.master_strip().set_volume_control(None)
                self._mixer.selected_strip().set_volume_control(self._master_slider)

    def _shift_value(self, value):
        for index in range(NUM_TRACKS):
            if value == 0:
                self._mixer.channel_strip(index).set_solo_button(None)
                self._mixer.channel_strip(index).set_mute_button(self._mute_solo_buttons[index])
                self._mixer.set_bank_buttons(None, None)
                self._mixer.set_select_buttons(self._track_up_button, self._track_down_button)
            else:
                self._mixer.channel_strip(index).set_mute_button(None)
                self._mixer.channel_strip(index).set_solo_button(self._mute_solo_buttons[index])
                self._mixer.set_select_buttons(None, None)
                self._mixer.set_bank_buttons(self._track_up_button, self._track_down_button)