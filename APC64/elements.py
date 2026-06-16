# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\elements.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 6147 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.control_surface import MIDI_NOTE_TYPE, MIDI_PB_TYPE, ElementsBase, MapMode, PrioritizedResource, create_matrix_identifiers
from ableton.v3.control_surface.display import Text
from ableton.v3.control_surface.elements import ButtonElement
from . import midi
from .firmware_mode import FirmwareModeElement
from .touch_strip import TouchStripElement, TouchStripTouchElement

class TrackColorElement(ButtonElement):

    def reset(self):
        pass


class Elements(ElementsBase):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        add_button = partial((self.add_button),
          msg_type=MIDI_NOTE_TYPE,
          led_channel=(midi.FULL_BRIGHTNESS_LED_CHANNEL))
        add_modifier_button = partial((self.add_modifier_button),
          msg_type=MIDI_NOTE_TYPE,
          led_channel=(midi.FULL_BRIGHTNESS_LED_CHANNEL))
        add_button_matrix = partial((self.add_button_matrix),
          msg_type=MIDI_NOTE_TYPE,
          led_channel=(midi.FULL_BRIGHTNESS_LED_CHANNEL))
        add_button(72, 'Tempo_Button', resource_type=PrioritizedResource)
        add_modifier_button(73, 'Clear_Button')
        add_modifier_button(74, 'Duplicate_Button')
        add_modifier_button(75, 'Quantize_Button')
        add_modifier_button(76, 'Fixed_Length_Button')
        add_modifier_button(120, 'Shift_Button')
        add_modifier_button(121, 'Device_Button')
        self.add_modified_control(self.tempo_button, self.shift_button)
        self.add_modified_control(self.quantize_button, self.shift_button)
        add_button(77, 'Undo_Button')
        add_button(90, 'Encoder_Button')
        add_button(91, 'Play_Button')
        add_button(92, 'Record_Button')
        add_button(93, 'Stop_Button')
        add_button(108, 'Record_Arm_Button')
        add_button(109, 'Mute_Button')
        add_button(110, 'Solo_Button')
        add_button(111, 'Clip_Stop_Button')
        add_button(122, 'Volume_Button')
        add_button(123, 'Pan_Button')
        add_button(124, 'Send_Button')
        add_button(125, 'Channel_Strip_Button')
        add_button(126, 'Off_Button')
        self.add_element('Track_Color_Element', TrackColorElement, 89, is_private=True)
        for index, direction in enumerate(('up', 'down', 'left', 'right')):
            button_name = '{}_button'.format(direction)
            add_button(94 + index, button_name.title())
            button_obj = getattr(self, button_name)
            self.add_modified_control(control=button_obj, modifier=(self.shift_button))
            self.add_modified_control(control=button_obj, modifier=(self.device_button))

        add_button_matrix(create_matrix_identifiers(0, 64, width=8, flip_rows=True),
          'Pads',
          channels=(midi.FULL_BRIGHTNESS_LED_CHANNEL))
        add_button_matrix([range(64, 72)], 'Track_State_Buttons')
        add_button_matrix([range(100, 108)], 'Track_Select_Buttons')
        add_button_matrix([range(112, 120)], 'Scene_Launch_Buttons')
        self.add_encoder(90, 'Encoder', map_mode=(MapMode.LinearTwoCompliment))
        self.add_modified_control(control=(self.encoder), modifier=(self.shift_button))
        self.add_matrix([
         range(16, 24)],
          'Touch_Strips',
          msg_type=MIDI_PB_TYPE,
          channels=[
         range(0, 8)],
          element_factory=TouchStripElement,
          sensitivity_modifier=(self.shift_button))
        self.add_submatrix((self.touch_strips), 'Touch_Strips_2_thru_7', columns=(2,
                                                                                  8))
        self.add_matrix([
         range(82, 90)],
          'Touch_Elements',
          msg_type=MIDI_NOTE_TYPE,
          element_factory=(lambda identifier, **k: TouchStripTouchElement(
 identifier, encoder=self.touch_strips_raw[identifier - 82], **k)
))
        self.add_element('Firmware_Mode_Element',
          FirmwareModeElement,
          sysex_identifier=(midi.make_message(midi.MODE_MESSAGE_ID, 0)[:-2]),
          send_message_generator=(lambda v: midi.make_message(midi.MODE_MESSAGE_ID, v)
),
          use_first_byte_as_value=True)
        self.add_sysex_element(midi.make_message(midi.TRACK_TYPE_MESSAGE_ID, 0)[:-2], 'Track_Type_Element', lambda v: midi.make_message(midi.TRACK_TYPE_MESSAGE_ID, v)
)
        self.add_sysex_element(midi.make_message(midi.RTC_START_MESSAGE_ID, 0)[:-4], 'Render_To_Clip_Start_Element')
        self.add_sysex_element(midi.make_message(midi.RTC_DATA_MESSAGE_ID, 0)[:-4], 'Render_To_Clip_Data_Element')
        self.add_sysex_element(midi.make_message(midi.RTC_END_MESSAGE_ID, 0)[:-4], 'Render_To_Clip_End_Element')
        self.add_sysex_element((midi.make_message(midi.SET_DISPLAY_OWNER_ID, 0)[:-2]),
          'Display_Ownership_Command',
          (lambda v: midi.make_message(midi.SET_DISPLAY_OWNER_ID, v)
),
          optimized=True,
          use_first_byte_as_value=True)

        def generate_display_message(index, text):
            return (midi.make_message)(midi.DISPLAY_MESSAGE_ID, index, *text + (0, ))

        for i in range(3):
            self.add_sysex_display_line((midi.make_message(midi.DISPLAY_MESSAGE_ID, i)[:-1]),
              ('Display_Line_{}'.format(i + 1)),
              (partial(generate_display_message, i)),
              default_formatting=Text(max_width=8,
              justification=(Text.Justification.CENTER)))