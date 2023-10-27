# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\elements.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3053 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from functools import partial
from ableton.v2.base import depends
from ableton.v2.control_surface.elements import ButtonMatrixElement, ColorSysexElement, SysexElement
from novation import sysex
from novation.launchpad_elements import BUTTON_FADER_COLOR_CHANNEL, SESSION_WIDTH, LaunchpadElements, create_button, create_slider
from . import sysex_ids as ids

class Elements(LaunchpadElements):
    model_id = ids.LP_X_ID
    default_layout = sysex.NOTE_LAYOUT_BYTE
    button_fader_cc_offset = 21

    @depends(skin=None)
    def __init__(self, skin=None, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self._create_drum_pads()
        self._create_scale_pads()
        self._create_scale_feedback_switch()
        self.note_mode_button = create_button(96, 'Note_Mode_Button')
        self.custom_mode_button = create_button(97, 'Custom_Mode_Button')
        self.record_button = create_button(98, 'Record_Button')
        self.button_faders = ButtonMatrixElement(rows=[
         [create_slider(index + self.button_fader_cc_offset, 'Button_Fader_{}'.format(index)) for index in range(SESSION_WIDTH)]],
          name='Button_Faders')
        self.button_fader_color_elements_raw = [create_button((index + self.button_fader_cc_offset), ('Button_Fader_Color_Element_{}'.format(index)), channel=BUTTON_FADER_COLOR_CHANNEL) for index in range(SESSION_WIDTH)]
        self.button_fader_color_elements = ButtonMatrixElement(rows=[
         self.button_fader_color_elements_raw],
          name='Button_Fader_Color_Elements')
        self.note_layout_switch = SysexElement(name='Note_Layout_Switch',
          send_message_generator=(lambda v: sysex.STD_MSG_HEADER + (
         ids.LP_X_ID, sysex.NOTE_LAYOUT_COMMAND_BYTE, v, sysex.SYSEX_END_BYTE)
),
          default_value=(sysex.SCALE_LAYOUT_BYTE))
        session_button_color_identifier = sysex.STD_MSG_HEADER + (ids.LP_X_ID, 20)
        self.session_button_color_element = ColorSysexElement(name='Session_Button_Color_Element',
          sysex_identifier=session_button_color_identifier,
          send_message_generator=(lambda v: session_button_color_identifier + v + (sysex.SYSEX_END_BYTE,)
),
          skin=skin)
        self.button_fader_setup_element = SysexElement(name='Button_Fader_Setup_Element',
          send_message_generator=(partial(self._fader_setup_message_generator, 0)))