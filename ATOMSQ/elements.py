# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\elements.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 5008 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.control_surface import MIDI_NOTE_TYPE, MIDI_PB_TYPE, ElementsBase, MapMode, create_button
from ableton.v3.control_surface.display import Text
from . import midi
from .touch_strip import TouchStripElement
SESSION_WIDTH = 16
SESSION_HEIGHT = 1
BANK_BUTTON_NAMES = ['bank_{}_button'.format(ltr) for ltr in 'abcdefgh']
TOUCH_STRIP_LED_CC_RANGE = range(55, 80)

class Elements(ElementsBase):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self.add_encoder(29, 'Display_Encoder', map_mode=(MapMode.LinearSignedBit))
        self.add_modifier_button(31, 'Shift_Button')
        self.add_button(0, 'Plus_Button', msg_type=MIDI_NOTE_TYPE, is_rgb=True)
        self.add_button(1, 'Minus_Button', msg_type=MIDI_NOTE_TYPE, is_rgb=True)
        self.add_button(32, 'Song_Mode_Button')
        self.add_button(33, 'Instrument_Mode_Button')
        self.add_button(34, 'Editor_Mode_Button')
        self.add_button(35, 'User_Mode_Button')
        self.add_button(42, 'Display_Left_Button')
        self.add_button(43, 'Display_Right_Button')
        self.add_button(87, 'Up_Button')
        self.add_button(89, 'Down_Button')
        self.add_button(90, 'Left_Button')
        self.add_button(102, 'Right_Button')
        self.add_button(105, 'Click_Button')
        self.add_button(107, 'Record_Button')
        self.add_button(109, 'Play_Button', is_rgb=True)
        self.add_button(111, 'Stop_Button')
        for i, name in enumerate(BANK_BUTTON_NAMES):
            self.add_button(i, (name.title()), is_rgb=True)

        self.add_modified_control(control=(self.play_button), modifier=(self.shift_button))
        self.add_modified_control(control=(self.stop_button), modifier=(self.shift_button))
        self.add_modified_control(control=(self.record_button), modifier=(self.shift_button))
        self.add_modified_control(control=(self.up_button), modifier=(self.shift_button))
        self.add_modified_control(control=(self.down_button), modifier=(self.shift_button))
        self.add_modified_control(control=(self.display_encoder),
          modifier=(self.shift_button))
        self.add_button_matrix([[i + 36 for i in range(6)]], 'Display_Buttons')
        self.add_button_matrix([
         [i + 36 for i in range(SESSION_WIDTH)]],
          'Lower_Pads',
          msg_type=MIDI_NOTE_TYPE,
          is_rgb=True)
        self.add_button_matrix([
         [i + 52 for i in range(SESSION_WIDTH)]],
          'Upper_Pads',
          msg_type=MIDI_NOTE_TYPE,
          is_rgb=True)
        self.add_encoder_matrix([
         [i + 14 for i in range(8)]],
          'Encoders',
          map_mode=(MapMode.LinearSignedBit),
          sensitivity_modifier=(self.shift_button))
        self.add_submatrix((self.encoders), 'Encoders_2_thru_7', columns=(2, 8))
        self.add_sysex_element(midi.LOWER_FIRMWARE_TOGGLE_HEADER, 'Lower_Firmware_Toggle_Switch', lambda v: midi.LOWER_FIRMWARE_TOGGLE_HEADER + (v, midi.SYSEX_END_BYTE)
)
        self.add_sysex_element(midi.UPPER_FIRMWARE_TOGGLE_HEADER, 'Upper_Firmware_Toggle_Switch', lambda v: midi.UPPER_FIRMWARE_TOGGLE_HEADER + (v, midi.SYSEX_END_BYTE)
)
        self.add_element('Touch_Strip',
          TouchStripElement,
          msg_type=MIDI_PB_TYPE,
          channel=15,
          needs_takeover=False,
          leds=[create_button(led_id, name=('Touch_Strip_LED_{}'.format(index))) for index, led_id in enumerate(TOUCH_STRIP_LED_CC_RANGE)])

        def make_display_line(name, display_id, default_formatting):

            def generate_display_message(display_id, ascii_bytes):
                return midi.DISPLAY_HEADER + (display_id, 0, 91, 91, 1) + ascii_bytes + (midi.SYSEX_END_BYTE,)

            self.add_sysex_display_line((midi.DISPLAY_HEADER + (display_id, 0, 91, 91, 1)),
              name,
              (partial(generate_display_message, display_id)),
              default_formatting=default_formatting)

        make_display_line('Track_Name_Display', 6, Text(max_width=18))
        make_display_line('Device_Name_Display', 7, Text(max_width=18))
        for i, display_id in enumerate((0, 1, 2, 11, 12, 13)):
            make_display_line('Button_Label_Display_{}'.format(i), display_id, Text(max_width=14, justification=(Text.Justification.CENTER)))