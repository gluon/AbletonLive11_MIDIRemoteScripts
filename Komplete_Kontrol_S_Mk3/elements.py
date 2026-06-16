# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk3\elements.py
# Compiled at: 2023-09-22 09:34:38
# Size of source mod 2**32: 4763 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import nop
from ableton.v3.control_surface import ElementsBase, MapMode, create_encoder
from ableton.v3.control_surface.elements import DiscreteValuesElement, SysexElement
from ableton.v3.control_surface.midi import SYSEX_END
from . import midi

def value_message_generator(header, index):
    return lambda value: header + (value, index, SYSEX_END)


def text_message_generator(header, index):
    return lambda ascii_bytes: header + (index,) + ascii_bytes + (SYSEX_END,)


def create_sysex_display_elements(header, generator):
    return [SysexElement(send_message_generator=(generator(header, i)), optimized=True, is_private=True) for i in range(8)]


def create_value_displays(header):
    return create_sysex_display_elements(header, value_message_generator)


def create_text_displays(header):
    return create_sysex_display_elements(header, text_message_generator)


def create_kk_encoder(*a, **k):
    return create_encoder(a, **k, **{'map_mode':MapMode.LinearTwoCompliment, 
     'encoder_sensitivity':1.0, 
     'mapping_sensitivity':0.1, 
     'feedback_delay':-1})


class Elements(ElementsBase):

    def __init__(self, *a, **k):
        (super().__init__)(a, global_channel=midi.MIDI_CHANNEL, **k)
        self.add_button(16, 'Play_Button')
        self.add_button(17, 'Restart_Button')
        self.add_button(18, 'Record_Button')
        self.add_button(19, 'Count_In_Button')
        self.add_button(20, 'Stop_Button')
        self.add_button(22, 'Loop_Button')
        self.add_button(23, 'Metro_Button')
        self.add_button(24, 'Tempo_Button')
        self.add_button(32, 'Undo_Button')
        self.add_button(33, 'Redo_Button')
        self.add_button(34, 'Quantize_Button')
        self.add_button(35, 'Auto_Button')
        self.add_button(96, 'Clip_Launch_Button')
        self.add_button(97, 'Track_Stop_Button')
        self.add_encoder(48, 'Track_Encoder')
        self.add_encoder(49, 'Track_Bank_Encoder')
        self.add_encoder(50, 'Scene_Encoder')
        self.add_encoder(53, 'Loop_Start_Encoder')
        self.add_encoder(100, 'Track_Volume_Encoder')
        self.add_encoder(101, 'Track_Pan_Encoder')
        self.add_matrix([
         list(range(80, 88))],
          'Volume_Encoders',
          element_factory=create_kk_encoder,
          is_feedback_enabled=True)
        self.add_matrix([
         list(range(88, 96))],
          'Pan_Encoders',
          element_factory=create_kk_encoder,
          is_feedback_enabled=True)
        for name, identifier in (('Track_Mute_Element', 67), ('Track_Solo_Element', 68)):
            self.add_element(name,
              DiscreteValuesElement,
              identifier,
              channel=(midi.MIDI_CHANNEL),
              values=(range(8)))

        self.track_type_displays = create_value_displays(midi.TRACK_TYPE_HEADER)
        self.track_select_displays = create_value_displays(midi.TRACK_SELECT_HEADER)
        self.track_mute_displays = create_value_displays(midi.TRACK_MUTE_HEADER)
        self.track_solo_displays = create_value_displays(midi.TRACK_SOLO_HEADER)
        self.track_mute_via_solo_displays = create_value_displays(midi.TRACK_MUTE_VIA_SOLO_HEADER)
        self.track_arm_displays = create_value_displays(midi.TRACK_ARM_HEADER)
        self.track_name_displays = create_text_displays(midi.TRACK_NAME_HEADER)
        self.track_volume_displays = create_text_displays(midi.TRACK_VOLUME_HEADER)
        self.track_pan_displays = create_text_displays(midi.TRACK_PAN_HEADER)
        self.add_sysex_element((midi.TRACK_METER_HEADER),
          'Track_Meter_Display',
          send_message_generator=(lambda meters: midi.TRACK_METER_HEADER + tuple(meters) + (SYSEX_END,)
),
          optimized=True)
        self.add_sysex_element((midi.FOCUS_FOLLOW_HEADER),
          'Focus_Follow_Element',
          send_message_generator=(lambda value: midi.FOCUS_FOLLOW_HEADER + value + (SYSEX_END,)
))

    def add_button(self, *a, **k):
        (super().add_button)(a, **k, **{'is_momentary': False})

    def add_encoder(self, identifier, name, **k):
        (self.add_element)(
 name, create_kk_encoder, identifier, channel=midi.MIDI_CHANNEL, **k)
        getattr(self, name.lower()).reset = nop