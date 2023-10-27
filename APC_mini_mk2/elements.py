# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_mini_mk2\elements.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 1639 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import MIDI_NOTE_TYPE, ElementsBase, create_matrix_identifiers
from ableton.v3.control_surface.midi import SYSEX_END, SYSEX_START
from .colors import FULL_BRIGHTNESS_CHANNEL
PAD_MODE_HEADER = (
 SYSEX_START, 71, 127, 79, 98, 0, 1)

class Elements(ElementsBase):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self.add_modifier_button(122, 'Shift_Button', msg_type=MIDI_NOTE_TYPE)
        self.add_button_matrix(create_matrix_identifiers(0, 64, width=8, flip_rows=True),
          'Clip_Launch_Buttons',
          msg_type=MIDI_NOTE_TYPE,
          led_channel=FULL_BRIGHTNESS_CHANNEL)
        self.add_button_matrix(create_matrix_identifiers(64, 128, width=8, flip_rows=True),
          'Drum_Pads',
          msg_type=MIDI_NOTE_TYPE,
          channels=9)
        self.add_button_matrix([
         range(100, 108)],
          'Track_Buttons', msg_type=MIDI_NOTE_TYPE)
        self.add_button_matrix([
         range(112, 120)],
          'Scene_Launch_Buttons', msg_type=MIDI_NOTE_TYPE)
        self.add_encoder(56, 'Master_Fader')
        self.add_encoder_matrix([range(48, 56)], 'Faders')
        self.add_sysex_element(PAD_MODE_HEADER,
          'Pad_Mode_Control',
          (lambda v: PAD_MODE_HEADER + (v, SYSEX_END)
),
          use_first_byte_as_value=True)