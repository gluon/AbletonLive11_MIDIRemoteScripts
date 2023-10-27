# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\VCM600.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 8740 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.ChannelStripComponent as ChannelStripComponent
import _Framework.ChannelTranslationSelector as ChannelTranslationSelector
import _Framework.ClipSlotComponent as ClipSlotComponent
import _Framework.ControlSurface as ControlSurface
import _Framework.DeviceComponent as DeviceComponent
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import *
import _Framework.SceneComponent as SceneComponent
import _Framework.SessionComponent as SessionComponent
import _Framework.SliderElement as SliderElement
from .MixerComponent import MixerComponent
from .TransportComponent import TransportComponent
from .ViewTogglerComponent import ViewTogglerComponent
NUM_TRACKS = 12

class VCM600(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self._setup_session_control()
            self._setup_mixer_control()
            self._setup_device_control()
            self._setup_transport_control()
            self._setup_view_control()

    def _setup_session_control(self):
        is_momentary = True
        down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 89)
        up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 90)
        session = SessionComponent(NUM_TRACKS, 0)
        session.set_select_buttons(down_button, up_button)
        session.selected_scene().set_launch_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 87))
        track_stop_buttons = [ButtonElement(is_momentary, MIDI_NOTE_TYPE, index, 68) for index in range(NUM_TRACKS)]
        session.set_stop_track_clip_buttons(tuple(track_stop_buttons))
        for index in range(NUM_TRACKS):
            session.selected_scene().clip_slot(index).set_launch_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, index, 69))

    def _setup_mixer_control(self):
        is_momentary = True
        mixer = MixerComponent(NUM_TRACKS, 2)
        for track in range(NUM_TRACKS):
            strip = mixer.channel_strip(track)
            strip.set_volume_control(SliderElement(MIDI_CC_TYPE, track, 23))
            strip.set_pan_control(EncoderElement(MIDI_CC_TYPE, track, 10, Live.MidiMap.MapMode.absolute))
            strip.set_send_controls((
             EncoderElement(MIDI_CC_TYPE, track, 19, Live.MidiMap.MapMode.absolute),
             EncoderElement(MIDI_CC_TYPE, track, 20, Live.MidiMap.MapMode.absolute)))
            strip.set_solo_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 64))
            strip.set_mute_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 63))
            strip.set_crossfade_toggle(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 65))
            eq = mixer.track_eq(track)
            eq.set_gain_controls(tuple([EncoderElement(MIDI_CC_TYPE, track, 18 - index, Live.MidiMap.MapMode.absolute) for index in range(3)]))
            eq.set_cut_buttons(tuple([ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 62 - index) for index in range(3)]))
            filter = mixer.track_filter(track)
            filter.set_filter_controls(EncoderElement(MIDI_CC_TYPE, track, 22, Live.MidiMap.MapMode.absolute), EncoderElement(MIDI_CC_TYPE, track, 21, Live.MidiMap.MapMode.absolute))

        for ret_track in range(2):
            strip = mixer.return_strip(ret_track)
            strip.set_volume_control(SliderElement(MIDI_CC_TYPE, 12, 22 + ret_track))
            strip.set_pan_control(EncoderElement(MIDI_CC_TYPE, 12, 20 + ret_track, Live.MidiMap.MapMode.absolute))
            strip.set_mute_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 78 + ret_track))

        mixer.set_crossfader_control(SliderElement(MIDI_CC_TYPE, 12, 8))
        mixer.set_prehear_volume_control(EncoderElement(MIDI_CC_TYPE, 12, 24, Live.MidiMap.MapMode.absolute))
        mixer.master_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, 12, 7))
        mixer.master_strip().set_pan_control(EncoderElement(MIDI_CC_TYPE, 12, 10, Live.MidiMap.MapMode.absolute))
        return mixer

    def _setup_device_control(self):
        is_momentary = True
        device_bank_buttons = []
        device_param_controls = []
        for index in range(8):
            device_bank_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 70 + index))
            device_param_controls.append(EncoderElement(MIDI_CC_TYPE, 12, 12 + index, Live.MidiMap.MapMode.absolute))

        device = DeviceComponent()
        device.set_bank_buttons(tuple(device_bank_buttons))
        device.set_parameter_controls(tuple(device_param_controls))
        device_translation_selector = ChannelTranslationSelector()
        device_translation_selector.set_controls_to_translate(tuple(device_param_controls))
        device_translation_selector.set_mode_buttons(tuple(device_bank_buttons))
        self.set_device_component(device)

    def _setup_transport_control(self):
        is_momentary = True
        transport = TransportComponent()
        transport.set_play_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 80))
        transport.set_record_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 81))
        transport.set_nudge_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 86), ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 85))
        transport.set_loop_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 84))
        transport.set_punch_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 82), ButtonElement(is_momentary, MIDI_NOTE_TYPE, 12, 83))
        transport.set_tempo_control(SliderElement(MIDI_CC_TYPE, 12, 26), SliderElement(MIDI_CC_TYPE, 12, 25))

    def _setup_view_control(self):
        is_momentary = True
        view = ViewTogglerComponent(NUM_TRACKS)
        view.set_buttons(tuple([ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 67) for track in range(NUM_TRACKS)]), tuple([ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 66) for track in range(NUM_TRACKS)]))