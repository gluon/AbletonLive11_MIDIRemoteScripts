# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\elements.py
# Compiled at: 2022-12-08 12:23:09
# Size of source mod 2**32: 2476 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import MIDI_NOTE_TYPE, ElementsBase, MapMode, create_sysex_sending_button
from .encoder import EncoderElement, RealigningEncoderElement
from .midi import LED_HEADER, PAD_ID_TO_SYSEX_ID, SYSEX_HEADER
from .sysex import SysexElement
NUM_TRACKS = 8
NUM_SCENES = 1

def create_rgb_pad(identifier, name, **k):
    return create_sysex_sending_button(
 identifier, name, LED_HEADER + (PAD_ID_TO_SYSEX_ID[identifier],), is_rgb=True, **k)


class Elements(ElementsBase):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self.add_button(27, 'Shift_Button')
        self.add_encoder(28, 'Display_Encoder', map_mode=(MapMode.LinearBinaryOffset))
        self.add_encoder(29,
          'Shifted_Display_Encoder', map_mode=(MapMode.LinearBinaryOffset))
        self.add_button(118, 'Display_Encoder_Button')
        self.add_button(119, 'Shifted_Display_Encoder_Button')
        self.add_matrix([
         [
          86,87,89,90,110,111,116,117]],
          'Encoders',
          element_factory=RealigningEncoderElement)
        self.add_element('Volume_Fader', EncoderElement, 14)
        self.add_element('Send_A_Fader', EncoderElement, 15)
        self.add_element('Send_B_Fader', EncoderElement, 30)
        self.add_element('Pan_Fader', EncoderElement, 31)
        self.add_matrix([
         range(36, 44)],
          'Pad_Bank_A',
          msg_type=MIDI_NOTE_TYPE,
          channels=9,
          element_factory=create_rgb_pad)
        self.add_matrix([
         range(44, 52)],
          'Pad_Bank_B',
          msg_type=MIDI_NOTE_TYPE,
          channels=9,
          element_factory=create_rgb_pad)
        self.add_element('Loop_Button', create_rgb_pad, 105)
        self.add_element('Stop_Button', create_rgb_pad, 106)
        self.add_element('Play_Button', create_rgb_pad, 107)
        self.add_element('Record_Button', create_rgb_pad, 108)
        self.add_element('Tap_Tempo_Button', create_rgb_pad, 109)
        self.add_element('Firmware_Element',
          SysexElement,
          sysex_identifier=(SYSEX_HEADER + (2, 0, 64)),
          is_private=True)