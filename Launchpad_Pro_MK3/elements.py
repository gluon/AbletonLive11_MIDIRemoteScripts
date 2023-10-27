# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro_MK3\elements.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 7425 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.control_surface import PrioritizedResource
from ableton.v2.control_surface.elements import ButtonMatrixElement, ComboElement, SysexElement
from novation import sysex
from novation.launchpad_elements import BUTTON_FADER_COLOR_CHANNEL, SESSION_WIDTH, LaunchpadElements, create_button, create_slider
from . import sysex_ids as ids
FADER_MODES = [
 'volume', 'pan', 'sends', 'device']

def create_modifier_button(identifier, name):
    return create_button(identifier,
      ('{}_Button'.format(name)), resource_type=PrioritizedResource)


class Elements(LaunchpadElements):
    model_id = ids.LP_PRO_MK3_ID
    default_layout = ids.NOTE_LAYOUT_BYTES

    def __init__(self, *a, **k):
        (super(Elements, self).__init__)(a, arrow_button_identifiers=(80, 70, 91, 92), session_mode_button_identifier=93, **k)
        self._create_drum_pads()
        self._create_scale_pads()
        self._create_scale_feedback_switch()
        self.quantize_button = create_modifier_button(40, 'Quantize')
        self.duplicate_button = create_modifier_button(50, 'Duplicate')
        self.clear_button = create_modifier_button(60, 'Clear')
        self.shift_button = create_modifier_button(90, 'Shift')
        self.record_arm_button = create_button(1, 'Record_Arm_Button')
        self.mute_button = create_button(2, 'Mute_Button')
        self.solo_button = create_button(3, 'Solo_Button')
        self.volume_button = create_button(4, 'Volume_Button')
        self.pan_button = create_button(5, 'Pan_Button')
        self.sends_button = create_button(6, 'Sends_Button')
        self.device_button = create_button(7, 'Device_Button')
        self.stop_clip_button = create_button(8, 'Stop_Clip_Button')
        self.record_button = create_button(10, 'Record_Button')
        self.play_button = create_button(20, 'Play_Button')
        self.fixed_length_button = create_button(30, 'Fixed_Length_Button')
        self.track_select_buttons_raw = [create_button(index + 101, 'Track_Select_Button_{}'.format(index)) for index in range(SESSION_WIDTH)]
        self.track_select_buttons = ButtonMatrixElement(rows=[
         self.track_select_buttons_raw],
          name='Track_Select_Buttons')
        for bank, bank_name in enumerate(FADER_MODES):
            capitalized_name = bank_name.capitalize()
            control_elements_name = '{}_button_faders'.format(bank_name)
            setattr(self, control_elements_name, ButtonMatrixElement(rows=[
             [create_slider(index + bank * SESSION_WIDTH, '{}_Button_Fader_{}'.format(capitalized_name, index)) for index in range(SESSION_WIDTH)]],
              name=('{}_Button_Faders'.format(capitalized_name))))
            color_elements_name = '{}_button_fader_color_elements'.format(bank_name)
            setattr(self, color_elements_name, ButtonMatrixElement(rows=[
             [create_button((index + bank * SESSION_WIDTH), ('{}_Button_Fader_Color_Element_{}'.format(capitalized_name, index)), channel=BUTTON_FADER_COLOR_CHANNEL) for index in range(SESSION_WIDTH)]],
              name=('{}_Button_Fader_Color_Elements'.format(capitalized_name))))

        def with_shift(button):
            return ComboElement(control=button,
              modifier=(self.shift_button),
              name=('{}_With_Shift'.format(button.name)))

        self.track_select_buttons_with_shift = ButtonMatrixElement(rows=[
         [with_shift(button) for button in self.track_select_buttons_raw]],
          name='Track_Select_Buttons_With_Shift')
        self.up_button_with_shift = with_shift(self.up_button)
        self.down_button_with_shift = with_shift(self.down_button)
        self.left_button_with_shift = with_shift(self.left_button)
        self.right_button_with_shift = with_shift(self.right_button)
        self.quantize_button_with_shift = with_shift(self.quantize_button)
        self.duplicate_button_with_shift = with_shift(self.duplicate_button)
        self.clear_button_with_shift = with_shift(self.clear_button)
        self.record_arm_button_with_shift = with_shift(self.record_arm_button)
        self.mute_button_with_shift = with_shift(self.mute_button)
        self.solo_button_with_shift = with_shift(self.solo_button)
        self.sends_button_with_shift = with_shift(self.sends_button)
        self.volume_button_with_shift = with_shift(self.volume_button)
        self.pan_button_with_shift = with_shift(self.pan_button)
        self.device_button_with_shift = with_shift(self.device_button)
        self.stop_clip_button_with_shift = with_shift(self.stop_clip_button)
        self.record_button_with_shift = with_shift(self.record_button)
        self.play_button_with_shift = with_shift(self.play_button)
        self.fixed_length_button_with_shift = with_shift(self.fixed_length_button)
        print_to_clip_identifier = sysex.STD_MSG_HEADER + (
         self.model_id,
         sysex.PRINT_COMMAND_BYTE)
        self.print_to_clip_element = SysexElement(name='Print_To_Clip_Element',
          sysex_identifier=print_to_clip_identifier,
          send_message_generator=(lambda v: print_to_clip_identifier + (
         v, sysex.SYSEX_END_BYTE)
))
        self.print_to_clip_enabler_element = SysexElement(name='Print_To_Clip_Enabler',
          send_message_generator=(lambda v: sysex.STD_MSG_HEADER + (
         self.model_id, sysex.PRINT_ENABLE_COMMAND_BYTE, v, sysex.SYSEX_END_BYTE)
),
          default_value=0)
        self.fader_setup_element = SysexElement(name='Fader_Setup_Element',
          send_message_generator=(self._fader_setup_message_generator))
        self.stop_fader_element = SysexElement(name='Stop_Fader_Element',
          send_message_generator=(self._stop_fader_message_generator),
          sysex_identifier=(sysex.STD_MSG_HEADER + (
         self.model_id, sysex.STOP_FADER_COMMAND_BYTE)))

    def _stop_fader_message_generator(self, bank):
        return sysex.STD_MSG_HEADER + (
         self.model_id,
         sysex.STOP_FADER_COMMAND_BYTE,
         bank,
         sysex.SYSEX_END_BYTE)