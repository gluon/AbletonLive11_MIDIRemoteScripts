# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\elements.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 39100 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement
from ableton.v2.control_surface.elements import ButtonMatrixElement as ButtonMatrixElementBase
from ableton.v2.control_surface.elements import ComboElement, EncoderElement, SliderElement, SysexElement, TouchEncoderElement
from . import sysex
from .multi_element import MultiElement
from .physical_display import PhysicalDisplayElement
MAX_NUM_SENDS = 4
NUM_SCENE_CONTROLS = 8
NUM_TRACK_CONTROLS = 8
NUM_PARAM_CONTROLS = 8

class ButtonMatrixElement(ButtonMatrixElementBase):

    def rows(self):
        for row in self._buttons:
            yield row


class Elements(object):
    msg_header_length = len(sysex.SYSEX_MSG_HEADER) + 1
    physical_clip_launch_button_id_offset = None
    duplicate_button_id = None
    undo_button_id = None
    shift_button_id = None
    up_button_id = None
    down_button_id = None
    left_button_id = None
    right_button_id = None
    play_button_id = None
    stop_button_id = None
    session_record_button_id = None
    tap_tempo_button_id = None
    delete_button_id = None
    pad_identifier_offset = None

    @depends(skin=None)
    def __init__(self, product_id=None, skin=None, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self._product_id = product_id
        self._skin = skin
        volume_encoder_touch_elements = [self._make_note_button(13, index, 'Volume_Encoder_Touch_Element_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]
        tui_volume_sliders = [SliderElement(MIDI_CC_TYPE, (index + 1), 0, name=('TUI_Volume_Slider_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]
        for slider in tui_volume_sliders:
            slider.set_feedback_delay(1)

        physical_volume_encoders = [TouchEncoderElement(MIDI_CC_TYPE, 13, index, (Live.MidiMap.MapMode.relative_smooth_two_compliment), name=('Physical_Volume_Encoder_{}'.format(index)), touch_element=(volume_encoder_touch_elements[index])) for index in range(NUM_TRACK_CONTROLS)]
        for encoder in physical_volume_encoders:
            encoder.set_feedback_delay(1)

        self.volume_sliders = ButtonMatrixElement(rows=[
         [MultiElement(tui_volume_sliders[index], physical_volume_encoders[index]) for index in range(NUM_TRACK_CONTROLS)]],
          name='Volume_Controls')
        self.pan_sliders = ButtonMatrixElement(rows=[
         [SliderElement(MIDI_CC_TYPE, (index + 1), 1, name=('TUI_Pan_Slider_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]],
          name='TUI_Pan_Sliders')
        tui_device_controls = [SliderElement(MIDI_CC_TYPE, 9, index, name=('TUI_Device_Control_{}'.format(index))) for index in range(NUM_PARAM_CONTROLS)]
        for slider in tui_device_controls:
            slider.set_feedback_delay(1)

        self.tui_device_controls = ButtonMatrixElement(rows=[
         tui_device_controls],
          name='TUI_Device_Controls')
        self.physical_device_control_touch_elements = ButtonMatrixElement(rows=[
         [self._make_note_button(13, index + 8, 'Physical_Device_Control_Touch_Element_{}'.format(index)) for index in range(NUM_PARAM_CONTROLS)]],
          name='Physical_Device_Control_Touch_Elements')
        physical_device_controls = [EncoderElement(MIDI_CC_TYPE, 13, (index + 8), (Live.MidiMap.MapMode.relative_smooth_two_compliment), name=('Physical_Device_Control_{}'.format(index))) for index in range(NUM_PARAM_CONTROLS)]
        for encoder in physical_device_controls:
            encoder.set_feedback_delay(1)

        self.physical_device_controls = ButtonMatrixElement(rows=[
         physical_device_controls],
          name='Physical_Device_Controls')
        self.device_parameter_enable_controls = ButtonMatrixElement(rows=[
         [self._make_note_button(9, index + 112, 'Device_Parameter_Enable_Control_{}'.format(index)) for index in range(NUM_PARAM_CONTROLS)]],
          name='Device_Parameter_Enable_Controls')
        self.solo_buttons_raw = [MultiElement((self._make_note_button(index + 1, 0, 'TUI_Solo_Button_{}'.format(index))), name=('Solo_Button_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]
        self.solo_buttons = ButtonMatrixElement(rows=[
         self.solo_buttons_raw],
          name='Solo_Buttons')
        self.mute_buttons_raw = [MultiElement((self._make_note_button(index + 1, 1, 'TUI_Mute_Button_{}'.format(index))), name=('Mute_Button_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]
        self.mute_buttons = ButtonMatrixElement(rows=[
         self.mute_buttons_raw],
          name='Mute_Buttons')
        self.solo_mute_buttons_raw = [MultiElement((self._make_note_button(index + 1, 2, 'TUI_Solo_Mute_Button_{}'.format(index))), name=('Solo_Mute_Button_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]
        self.solo_mute_buttons = ButtonMatrixElement(rows=[
         self.solo_mute_buttons_raw],
          name='Solo_Mute_Buttons')
        self.arm_buttons_raw = [MultiElement((self._make_note_button(index + 1, 5, 'TUI_Arm_Button_{}'.format(index))), name=('Arm_Button_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]
        self.arm_buttons = ButtonMatrixElement(rows=[
         self.arm_buttons_raw],
          name='Arm_Buttons')
        self.clip_stop_buttons_raw = [MultiElement((self._make_note_button(0, index + 16, 'Clip_Stop_TUI_Button_{}'.format(index))), name=('Clip_Stop_Button_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]
        self.clip_stop_buttons = ButtonMatrixElement(rows=[
         self.clip_stop_buttons_raw],
          name='Clip_Stop_Buttons')
        self.stop_all_clips_button = MultiElement(self._make_note_button(12, 89, name='Physical_Stop_All_Clips_Button'),
          self._make_note_button(10, 20, name='TUI_Stop_All_Clips_Button'),
          name='Stop_All_Clips_Button')
        self.send_encoders = ButtonMatrixElement(rows=[[EncoderElement(MIDI_CC_TYPE, (row_index + 1), (col_index + 3), (Live.MidiMap.MapMode.absolute), name=('TUI_Send_Encoder_{}_{}'.format(row_index, col_index))) for col_index in range(MAX_NUM_SENDS)] for row_index in range(NUM_TRACK_CONTROLS)],
          name='TUI_Send_Encoders')
        self.send_value_displays = ButtonMatrixElement(rows=[[self._create_text_display_element((1, row_index + col_index * NUM_TRACK_CONTROLS + 24), 'Send_Value_Display_{}_{}'.format(row_index, col_index)) for col_index in range(MAX_NUM_SENDS)] for row_index in range(NUM_TRACK_CONTROLS)],
          name='Send_Value_Displays')
        self.track_type_controls = ButtonMatrixElement(rows=[
         [self._make_note_button(0, index + 8, 'Track_Type_Control_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]],
          name='Track_Type_Controls')
        self.mute_button = self._make_note_button(12, 100, 'Mute_Button')
        self.solo_button = self._make_note_button(12, 101, 'Solo_Button')
        self.rec_arm_button = self._make_note_button(12, 102, 'Rec_Arm_Button')
        self.clip_stop_button = self._make_note_button(12, 103, 'Clip_Stop_Button')
        self.meter_controls_left = ButtonMatrixElement(rows=[
         [SliderElement(MIDI_CC_TYPE, (index + 1), 124, send_should_depend_on_forwarding=False, name=('Output_Meter_Display_Left_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]],
          name='Output_Meter_Displays_Left')
        self.meter_controls_right = ButtonMatrixElement(rows=[
         [SliderElement(MIDI_CC_TYPE, (index + 1), 125, send_should_depend_on_forwarding=False, name=('Output_Meter_Display_Right_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]],
          name='Output_Meter_Displays_Right')
        self._tui_track_select_buttons_raw = [self._make_note_button(0, index, 'TUI_Track_Select_Button_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]
        self.track_name_displays = ButtonMatrixElement(rows=[
         [self._create_text_display_element((0, index), 'Track_Name_Display_{}'.index) for index in range(NUM_TRACK_CONTROLS)]],
          name='Track_Name_Display')
        self.num_sends_control = ButtonElement(True,
          MIDI_CC_TYPE,
          1,
          2,
          name='Num_Sends_Control',
          send_should_depend_on_forwarding=False)
        self.tui_track_color_controls = ButtonMatrixElement(rows=[
         [ButtonElement(True, MIDI_CC_TYPE, 0, (index + 16), skin=skin, name=('TUI_Track_Color_Control_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]],
          name='TUI_Track_Color_Controls')
        self.oled_display_style_controls_bank_1 = ButtonMatrixElement(rows=[
         [self._make_note_button(13, index + 16, 'OLED_Display_Style_Control_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]],
          name='OLED_Display_Style_Controls_Bank_1')
        self.oled_display_style_controls_bank_2 = ButtonMatrixElement(rows=[
         [self._make_note_button(13, index + 24, 'OLED_Display_Style_Control_{}'.format(index + NUM_PARAM_CONTROLS)) for index in range(NUM_PARAM_CONTROLS)]],
          name='OLED_Display_Style_Controls_Bank_2')
        self.track_name_or_volume_value_displays = ButtonMatrixElement(rows=[
         [self._create_text_display_element((18, index + 16), 'Track_Name_Or_Volume_Value_Display_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]],
          name='Track_Name_Or_Volume_Value_Displays')
        self.device_parameter_name_or_value_displays = ButtonMatrixElement(rows=[
         [self._create_text_display_element((18, index + 24), 'Device_Parameter_Name_Or_Value_Display_{}'.format(index)) for index in range(NUM_PARAM_CONTROLS)]],
          name='Device_Parameter_Name_Or_Value_Displays')
        self.crossfade_assign_controls = ButtonMatrixElement(rows=[
         [self._make_note_button((index + 1), 4, name=('Crossfade_Assign_Controk_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]],
          name='Crossfade_Assign_Controls')
        self.crossfader = SliderElement(MIDI_CC_TYPE, 13, 16, name='Crossfader')
        self.physical_clip_launch_buttons_raw = [[self._make_note_button(12, col_index + self.physical_clip_launch_button_id_offset + row_index * NUM_TRACK_CONTROLS, 'Physical_Clip_Launch_Button_{}_{}'.format(col_index, row_index)) for col_index in range(NUM_TRACK_CONTROLS)] for row_index in range(NUM_SCENE_CONTROLS)]
        self.clip_launch_buttons_raw = [[MultiElement((self._make_note_button(0, col_index + 24 + row_index * NUM_TRACK_CONTROLS, 'TUI_Clip_Launch_Button_{}_{}'.format(col_index, row_index))), name=('Clip_Launch_Button_{}_{}'.format(col_index, row_index))) for col_index in range(NUM_TRACK_CONTROLS)] for row_index in range(NUM_SCENE_CONTROLS)]
        self.clip_launch_buttons = ButtonMatrixElement(rows=(self.clip_launch_buttons_raw),
          name='Clip_Launch_Buttons')
        self.scene_launch_buttons = ButtonMatrixElement(rows=[
         [self._make_note_button(0, (index + 88), name=('TUI_Scene_Launch_Button_{}'.format(index))) for index in range(NUM_SCENE_CONTROLS)]],
          name='TUI_Scene_Launch_Buttons')
        self.clip_name_displays = ButtonMatrixElement(rows=[[self._create_text_display_element((0, row_index + 16 + col_index * NUM_SCENE_CONTROLS), 'Clip_Name_Display_{}_{}'.format(col_index, row_index)) for col_index in range(NUM_TRACK_CONTROLS)] for row_index in range(NUM_SCENE_CONTROLS)])
        self.scene_name_displays = ButtonMatrixElement(rows=[
         [self._create_text_display_element((0, index + 80), 'Scene_Name_Display_{}'.format(index)) for index in range(NUM_SCENE_CONTROLS)]],
          name='Scene_Name_Displays')
        self.tui_scene_color_controls = ButtonMatrixElement(rows=[
         [ButtonElement(True, MIDI_CC_TYPE, 0, (index + 88), skin=skin, name=('TUI_Scene_Color_Control_{}'.format(index))) for index in range(NUM_SCENE_CONTROLS)]],
          name='TUI_Scene_Color_Controls')
        self.physical_clip_color_controls_raw = [[ButtonElement(True, MIDI_CC_TYPE, 12, (row_index + self.pad_identifier_offset + col_index * NUM_SCENE_CONTROLS), skin=skin, name=('Physical_Clip_Color_Control_{}_{}'.format(col_index, row_index))) for col_index in range(NUM_TRACK_CONTROLS)] for row_index in range(NUM_SCENE_CONTROLS)]
        self.clip_color_controls_raw = [[MultiElement(ButtonElement(True, MIDI_CC_TYPE, 0, (row_index + 24 + col_index * NUM_SCENE_CONTROLS), skin=skin, name=('TUI_Clip_Color_Control_{}_{}'.format(col_index, row_index))), name=('Clip_Color_Control_{}_{}'.format(col_index, row_index))) for col_index in range(NUM_TRACK_CONTROLS)] for row_index in range(NUM_SCENE_CONTROLS)]
        self.clip_color_controls = ButtonMatrixElement(rows=(self.clip_color_controls_raw),
          name='Clip_Color_Controls')
        self.playing_position_controls = ButtonMatrixElement(rows=[
         [SliderElement(MIDI_CC_TYPE, 0, index, send_should_depend_on_forwarding=False, name=('Playing_Position_Control_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]],
          name='Playing_Position_Controls')
        self.shift_button = self._make_note_button(12,
          (self.shift_button_id), 'Shift_Button', resource_type=PrioritizedResource)
        self.up_button = self._make_note_button(12, self.up_button_id, 'Up_Button')
        self.down_button = self._make_note_button(12, self.down_button_id, 'Down_Button')
        self.left_button = self._make_note_button(12, self.left_button_id, 'Left_Button')
        self.right_button = self._make_note_button(12, self.right_button_id, 'Right_Button')
        self.up_button_with_shift = ComboElement((self.up_button),
          modifier=[self.shift_button], name='Up_Button_With_Shift')
        self.down_button_with_shift = ComboElement((self.down_button),
          modifier=[self.shift_button], name='Down_Button_With_Shift')
        self.left_button_with_shift = ComboElement((self.left_button),
          modifier=[self.shift_button], name='Left_Button_With_Shift')
        self.right_button_with_shift = ComboElement((self.right_button),
          modifier=[
         self.shift_button],
          name='Right_Button_With_Shift')
        self.scene_selection_controls = ButtonMatrixElement(rows=[
         [self._make_note_button(0, index + 96, 'Scene_Selection_Control_{}'.format(index)) for index in range(NUM_SCENE_CONTROLS)]],
          name='Scene_Selection_Controls')
        self.duplicate_button = self._make_note_button(12, self.duplicate_button_id, 'Duplicate_Button')
        self.undo_button = self._make_note_button(12, self.undo_button_id, 'Undo_Button')
        self.redo_button = ComboElement((self.undo_button),
          modifier=[self.shift_button], name='Redo_Button')
        self.tui_device_parameter_name_displays = ButtonMatrixElement(rows=[
         [self._create_text_display_element((2, index + 16), 'TUI_Device_Parameter_Name_Display_{}'.format(index)) for index in range(NUM_PARAM_CONTROLS)]],
          name='TUI_Device_Parameter_Name_Displays')
        self.tui_device_parameter_value_displays = ButtonMatrixElement(rows=[
         [self._create_text_display_element((2, index + 32), 'TUI_Device_Parameter_Value_Display_{}'.format(index)) for index in range(NUM_PARAM_CONTROLS)]],
          name='TUI_Device_Parameter_Value_Displays')
        self.tui_arrangement_position_display = self._create_text_display_element((3,
                                                                                   16), 'TUI_Arrangement_Position_Display')
        self.tui_loop_start_display = self._create_text_display_element((3, 17), 'TUI_Loop_Start_Display')
        self.tui_loop_length_display = self._create_text_display_element((3, 18), 'TUI_Loop_Length_Display')
        self.tui_arrangement_position_control = EncoderElement(MIDI_CC_TYPE,
          10,
          0,
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='TUI_Arrangement_Position_Control')
        self.tui_loop_start_control = EncoderElement(MIDI_CC_TYPE,
          10,
          1,
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='TUI_Loop_Start_Control')
        self.tui_loop_length_control = EncoderElement(MIDI_CC_TYPE,
          10,
          2,
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='TUI_Loop_Length_Control')
        tempo_control_identifier = (3, 0)
        self.tempo_display = self._create_text_display_element(tempo_control_identifier, 'Tempo_Display')
        self.tempo_control = SysexElement(sysex_identifier=(sysex.SYSEX_MSG_HEADER + (self._product_id, sysex.TEXT_MSG_TYPE) + tempo_control_identifier),
          name='Tempo_Control')
        self.play_button = self._make_note_button(12, self.play_button_id, 'Play_Button')
        self.stop_button = self._make_note_button(12, self.stop_button_id, 'Stop_Button')
        self.session_record_button = self._make_note_button(12, self.session_record_button_id, 'Session_Record_Button')
        self.tap_tempo_button = self._make_note_button(12, self.tap_tempo_button_id, 'Tap_Tempo_Button')
        self._tui_prev_device_button = self._make_note_button(9, 1, 'TUI_Prev_Device_Button')
        self._tui_next_device_button = self._make_note_button(9, 2, 'TUI_Next_Device_Button')
        self.device_lock_button = self._make_note_button(10,
          10, 'Device_Lock_Button', is_momentary=False)
        self.num_devices_control = ButtonElement(True,
          MIDI_CC_TYPE, 9, 16, name='Num_Devices_Control')
        self.device_index_control = ButtonElement(True,
          MIDI_CC_TYPE, 9, 17, name='Device_Index_Control')
        self.device_name_display = self._create_text_display_element((2, 1), 'Device_Name_Display')
        self.device_enable_button = self._make_note_button(9,
          0, 'Device_Enable_Button', is_momentary=False)
        self._tui_prev_bank_button = self._make_note_button(9, 3, 'TUI_Prev_Bank_Button')
        self._tui_next_bank_button = self._make_note_button(9, 4, 'TUI_Next_Bank_Button')
        self.device_bank_name_display = self._create_text_display_element((2, 0), 'Device_Bank_Name_Display')
        self._tui_phase_nudge_down_button = self._make_note_button(10, 12, 'TUI_Phase_Nudge_Down_Button')
        self._tui_phase_nudge_up_button = self._make_note_button(10, 13, 'TUI_Phase_Nudge_Up_Button')
        self.tui_metronome_button = self._make_note_button(10,
          0, 'TUI_Metronome_Button', is_momentary=False)
        self.tui_automation_arm_button = self._make_note_button(10,
          4, 'TUI_Automation_Arm_Button', is_momentary=False)
        self.loop_button = self._make_note_button(10,
          5, 'Loop_Button', is_momentary=False)
        self.arrangement_overdub_button = self._make_note_button(10,
          3, 'Arrangement_Overdub_Button', is_momentary=False)
        self.follow_song_button = self._make_note_button(10,
          8, 'Follow_Song_Button', is_momentary=False)
        self.quantization_value_control = self._make_note_button(10, 15, 'Quantization_Value_Control')
        self._tui_quantize_button = self._make_note_button(10, 16, 'TUI_Quantize_Button')
        self.clip_trigger_quantization_control = self._make_note_button(10, 6, 'Clip_Trigger_Quantization_Control')
        self.delete_button = MultiElement((self._make_note_button(10, 14, 'TUI_Delete_Button')),
          (self._make_note_button(12, self.delete_button_id, 'Physical_Delete_Button')),
          name='Delete_Button')
        self.volume_value_displays = ButtonMatrixElement(rows=[
         [self._create_text_display_element((1, index), 'Volume_Value_Display_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]],
          name='Volume_Value_Displays')
        self.pan_value_displays = ButtonMatrixElement(rows=[
         [self._create_text_display_element((1, 16 + index), 'Pan_Value_Display_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]],
          name='Pan_Value_Displays')
        self.tui_arrangement_record_button = self._make_note_button(10, 22, 'TUI_Arrangement_Record_Button', False)
        self.insert_scene_button = self._make_note_button(10, 21, 'Insert_Scene_Button')
        self.launch_mode_switch = self._make_note_button(10, 23, 'Launch_Mode_Switch')

    def _make_note_button(self, channel, identifier, name, is_momentary=True, **k):
        return ButtonElement(
 is_momentary,
 MIDI_NOTE_TYPE,
 channel,
 identifier, skin=self._skin, 
         name=name, **k)

    def _sysex_message_generator(self, msg_type, id_bytes, v):
        return sysex.SYSEX_MSG_HEADER + (self._product_id, msg_type) + id_bytes + v + (sysex.SYSEX_END_BYTE,)

    def _create_text_display_element(self, item_id, name):
        display = PhysicalDisplayElement(width_in_chars=64, name=name)
        display.set_message_parts(sysex.SYSEX_MSG_HEADER + (self._product_id, sysex.TEXT_MSG_TYPE) + item_id, (
         sysex.SYSEX_END_BYTE,))
        return display


class ForceElements(Elements):
    physical_clip_launch_button_id_offset = 16
    duplicate_button_id = 96
    undo_button_id = 107
    shift_button_id = 114
    up_button_id = 115
    down_button_id = 116
    left_button_id = 117
    right_button_id = 118
    play_button_id = 104
    stop_button_id = 105
    session_record_button_id = 106
    tap_tempo_button_id = 99
    delete_button_id = 97
    pad_identifier_offset = 40

    def __init__(self, *a, **k):
        (super(ForceElements, self).__init__)(*a, **k)
        self.clip_select_button = self._make_note_button(12, 94, 'Clip_Select_Button')
        self.master_button = self._make_note_button(12, 88, 'Master_Button')
        self.track_assign_buttons_raw = [self._make_note_button(12, index + 8, 'Track_Assign_Button_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]
        self.track_assign_buttons = ButtonMatrixElement(rows=[
         self.track_assign_buttons_raw],
          name='Track_Assign_Buttons')
        self.track_assign_color_controls_raw = [ButtonElement(True, MIDI_CC_TYPE, 12, (index + 32), skin=(self._skin), name=('Track_Assign_Color_Control_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]
        self.track_assign_color_controls = ButtonMatrixElement(rows=[
         self.track_assign_color_controls_raw],
          name='Track_Assign_Color_Controls')
        physical_track_select_buttons_raw = [self._make_note_button(12, index, 'Physical_Track_Select_Button_{}'.format(index)) for index in range(NUM_TRACK_CONTROLS)]
        self.track_select_buttons = ButtonMatrixElement(rows=[
         [MultiElement((self._tui_track_select_buttons_raw[index]), (physical_track_select_buttons_raw[index]), name=('Track_Select_Button_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]],
          name='Track_Select_Buttons')
        self.physical_track_select_buttons_with_shift = ButtonMatrixElement(rows=[
         [ComboElement((physical_track_select_buttons_raw[index]), modifier=[self.shift_button], name='Physical_Track_Select_Button_With_Shift') for index in range(NUM_TRACK_CONTROLS)]],
          name='Physical_Track_Select_Buttons_With_Shift')
        self.physical_track_color_controls = ButtonMatrixElement(rows=[
         [ButtonElement(True, MIDI_CC_TYPE, 12, (index + 24), skin=(self._skin), name=('Physical_Track_Color_Control_{}'.format(index))) for index in range(NUM_TRACK_CONTROLS)]],
          name='Physical_Track_Color_Controls')
        self.force_physical_scene_launch_buttons = ButtonMatrixElement(rows=[
         [self._make_note_button(12, (index + 80), name=('Force_Physical_Scene_Launch_Button_{}'.format(index))) for index in range(NUM_SCENE_CONTROLS)]],
          name='Force_Physical_Scene_Launch_Buttons')
        self.continue_button = ComboElement((self.play_button),
          modifier=[self.shift_button], name='Continue_Button')
        self.physical_metronome_button = ComboElement((self.track_assign_buttons_raw[4]),
          modifier=[
         self.shift_button],
          name='Physical_Metronome_Button')
        self.prev_device_button = self._tui_prev_device_button
        self.next_device_button = self._tui_next_device_button
        self.prev_bank_button = self._tui_prev_bank_button
        self.next_bank_button = self._tui_next_bank_button
        self.assign_a_button = self._make_note_button(12, 119, 'Assign_A_Button')
        self.assign_b_button = self._make_note_button(12, 120, 'Assign_B_Button')
        self.phase_nudge_up_button = self._tui_phase_nudge_up_button
        self.phase_nudge_down_button = self._tui_phase_nudge_down_button
        self.quantize_button = MultiElement((self._tui_quantize_button),
          ComboElement((self.track_assign_buttons_raw[0]),
          modifier=[
         self.shift_button],
          name='Physical_Quantize_Button'),
          name='Quantize_Button')
        self.launch_button = self._make_note_button(12, 91, 'Launch_Button')


class MPCElementsBase(Elements):
    physical_clip_launch_button_id_offset = 0
    duplicate_button_id = 75
    undo_button_id = 74
    shift_button_id = 72
    up_button_id = 106
    down_button_id = 107
    left_button_id = 108
    right_button_id = 109
    play_button_id = 81
    stop_button_id = 79
    session_record_button_id = 78
    tap_tempo_button_id = 76
    delete_button_id = 71
    pad_identifier_offset = 0

    def __init__(self, *a, **k):
        (super(MPCElementsBase, self).__init__)(*a, **k)
        self.track_select_buttons = ButtonMatrixElement(rows=[
         self._tui_track_select_buttons_raw],
          name='Track_Select_Buttons')
        self.continue_button = self._make_note_button(12, 80, 'Continue_Button')
        self.physical_metronome_button = ComboElement((self.tap_tempo_button),
          modifier=[
         self.shift_button],
          name='Physical_Metronome_Button')
        self.read_write_button = self._make_note_button(12, 103, 'Read_Write_Button')
        self.selected_track_arm_button = self._make_note_button(12, 102, 'Selected_Track_Arm_Button')
        self.selected_track_mute_button = self._make_note_button(12, 104, 'Selected_Track_Mute_Button')
        self.selected_track_solo_button = self._make_note_button(12, 105, 'Selected_Track_Solo_Button')
        self.prev_device_button = MultiElement((self._tui_prev_device_button),
          (self._make_note_button(12, 93, 'Physical_Prev_Device_Button')),
          name='Prev_Device_Button')
        self.next_device_button = MultiElement((self._tui_next_device_button),
          (self._make_note_button(12, 94, 'Physical_Next_Device_Button')),
          name='Next_Device_Button')
        self.prev_bank_button = MultiElement((self._tui_prev_bank_button),
          (self._make_note_button(12, 95, 'Physical_Prev_Bank_Button')),
          name='Prev_Bank_Button')
        self.next_bank_button = MultiElement((self._tui_next_bank_button),
          (self._make_note_button(12, 96, 'Physical_Next_Bank_Button')),
          name='Next_Bank_Button')
        self.phase_nudge_up_button = MultiElement((self._tui_phase_nudge_up_button),
          (self._make_note_button(12, 86, 'Physical_Phase_Nudge_Up_Button')),
          name='Phase_Nudge_Up_Button')
        self.phase_nudge_down_button = MultiElement((self._tui_phase_nudge_down_button),
          (self._make_note_button(12, 85, 'Physical_Phase_Nudge_Down_Button')),
          name='Phase_Nudge_Down_Button')
        self.arrangement_record_button = self._make_note_button(12, 77, 'Arrangement_Record_Button')
        self.jump_backward_button = self._make_note_button(12, 82, 'Jump_Backward_Button')
        self.jump_forward_button = self._make_note_button(12, 83, 'Jump_Forward_Button')
        self.quantize_button = self._tui_quantize_button
        self.mpc_scene_launch_buttons = ButtonMatrixElement(rows=[[button for button in row[:4]] for row in self.physical_clip_launch_buttons_raw[:4]],
          name='MPC_Scene_Launch_Buttons')
        self.mpc_scene_color_controls = ButtonMatrixElement(rows=[[col[row_index] for col in self.physical_clip_color_controls_raw[:4]] for row_index in range(4)],
          name='MPC_Scene_Color_Controls')


class MPCXElements(MPCElementsBase):

    def __init__(self, *a, **k):
        (super(MPCXElements, self).__init__)(*a, **k)
        self.xyfx_button = self._make_note_button(12, 100, 'XYFX_Button')


class MPCLiveElements(MPCElementsBase):

    def __init__(self, *a, **k):
        (super(MPCLiveElements, self).__init__)(*a, **k)
        self.sixteen_level_button = self._make_note_button(12, 70, '16_Level_Button')