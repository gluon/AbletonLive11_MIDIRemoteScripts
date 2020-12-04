#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/elements.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import object
import Live
from ableton.v2.base import depends, mixin
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement, SliderElement, SysexElement
from . import sysex
from .caching_control_element import CachingControlElement
from .color_sysex_element import ColorSysexElement
from .message import NUM_MESSAGE_SEGMENTS
from .physical_display import ConfigurablePhysicalDisplayElement, SpecialPhysicalDisplayElement
SESSION_WIDTH = 8
SESSION_HEIGHT = 2
DEFAULT_CHANNEL = 15
IGNORED_FEEDBACK_CHANNEL = 14
DISPLAY_LINE_WIDTH = 72
NUM_DISPLAY_LINE_SEGMENTS = 8

@depends(skin=None)
def create_display_color_element(h_position, v_position, name, **k):
    sysex_identifier = sysex.SET_PROPERTY_MSG_HEADER + (h_position, sysex.COLOR_PROPERTY_BYTE, v_position)
    return mixin(CachingControlElement, ColorSysexElement)(sysex_identifier=sysex_identifier, send_message_generator=(lambda v: sysex_identifier + (v, sysex.SYSEX_END_BYTE)), default_value=0, name=name, **k)


def create_display_color_element_line(v_position, **k):
    raw_line = [ create_display_color_element(index, v_position, u'Color_Field_{}_{}'.format(index, v_position), **k) for index in range(SESSION_WIDTH) ]
    return (raw_line, ButtonMatrixElement(rows=[raw_line], name=u'Color_Field_Line_{}'.format(v_position)))


def create_selection_field(h_position, v_position):
    sysex_identifier = sysex.SET_PROPERTY_MSG_HEADER + (h_position, sysex.VALUE_PROPERTY_BYTE, v_position)
    return mixin(CachingControlElement, SysexElement)(sysex_identifier=sysex_identifier, send_message_generator=lambda v: sysex_identifier + (v, sysex.SYSEX_END_BYTE), default_value=0, name=u'Selection_Field_{}_{}'.format(h_position, v_position))


def create_selection_field_line(v_position):
    lines_raw = [ create_selection_field(index, v_position) for index in range(SESSION_WIDTH) ]
    return (lines_raw, ButtonMatrixElement(rows=[lines_raw], name=u'Selection_Field_Line_{}'.format(v_position)))


@depends(skin=None)
def create_rgb_led(identifier, name, **k):
    return ColorSysexElement(send_message_generator=(lambda v: sysex.SET_LED_MSG_HEADER + (identifier, sysex.SOLID_COLOR_LED_BYTE) + v + (sysex.SYSEX_END_BYTE,)), default_value=(0, 0, 0), name=name, **k)


@depends(skin=None)
def create_button(identifier, name, channel = DEFAULT_CHANNEL, msg_type = MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, channel, identifier, name=name, **k)


def create_text_display_line(v_position):
    display = mixin(CachingControlElement, ConfigurablePhysicalDisplayElement)(v_position=v_position, width_in_chars=DISPLAY_LINE_WIDTH, num_segments=NUM_DISPLAY_LINE_SEGMENTS, name=u'Text_Display_{}'.format(v_position))
    display.set_message_parts(sysex.SET_PROPERTY_MSG_HEADER, (sysex.SYSEX_END_BYTE,))
    for index in range(NUM_DISPLAY_LINE_SEGMENTS):
        display.segment(index).set_position_identifier((index,))

    return display


class SpecialFeedbackChannelSliderElement(SliderElement):
    feedback_channel = IGNORED_FEEDBACK_CHANNEL


class Elements(object):

    def __init__(self, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.display_up_button = create_button(81, u'Display_Up_Button')
        self.display_down_button = create_button(82, u'Display_Down_Button')
        self.up_button = create_button(85, u'Up_Button')
        self.down_button = create_button(86, u'Down_Button')
        self.mixer_up_button = create_button(87, u'Mixer_Up_Button')
        self.mixer_down_button = create_button(88, u'Mixer_Down_Button')
        self.grid_button = create_button(89, u'Grid_Button')
        self.options_button = create_button(90, u'Options_Button')
        self.shift_button = create_button(91, u'Shift_Button', resource_type=PrioritizedResource)
        self.duplicate_button = create_button(92, u'Duplicate_Button')
        self.clear_button = create_button(93, u'Clear_Button')
        self.track_left_button = create_button(102, u'Track_Left_Button')
        self.track_right_button = create_button(103, u'Track_Right_Button')
        self.rw_button = create_button(112, u'RW_Button')
        self.ff_button = create_button(113, u'FF_Button')
        self.stop_button = create_button(114, u'Stop_Button')
        self.play_button = create_button(115, u'Play_Button')
        self.loop_button = create_button(116, u'Loop_Button')
        self.record_button = create_button(117, u'Record_Button')

        def with_shift(button):
            return ComboElement(control=button, modifier=self.shift_button, name=u'{}_With_Shift'.format(button.name))

        self.up_button_with_shift = with_shift(self.up_button)
        self.down_button_with_shift = with_shift(self.down_button)
        self.record_button_with_shift = with_shift(self.record_button)
        self.play_button_with_shift = with_shift(self.play_button)
        self.track_left_button_with_shift = with_shift(self.track_left_button)
        self.track_right_button_with_shift = with_shift(self.track_right_button)
        self.duplicate_button_with_shift = with_shift(self.duplicate_button)
        pads_raw = [ [ create_button(offset + col_index, u'Pad_{}_{}'.format(col_index, row_index), msg_type=MIDI_NOTE_TYPE) for col_index in range(SESSION_WIDTH) ] for row_index, offset in enumerate((96, 112)) ]
        self.pads = ButtonMatrixElement(rows=pads_raw, name=u'Pads')
        self.pads_quadratic = ButtonMatrixElement(rows=[pads_raw[0][4:],
         pads_raw[1][4:],
         pads_raw[0][:4],
         pads_raw[1][:4]], name=u'Pads_Quadratic')
        self.pads_flattened = ButtonMatrixElement(rows=[pads_raw[0] + pads_raw[1]], name=u'Pads_Flattened')
        self.shifted_pad_row_1 = ButtonMatrixElement(rows=[[ with_shift(control) for control in pads_raw[1] ]], name=u'Pad_Row_1_With_Shift')
        scene_launch_buttons_raw = [ create_button(83 + row_index, name=u'Scene_Launch_Button_{}'.format(row_index)) for row_index in range(SESSION_HEIGHT) ]
        self.scene_launch_buttons = ButtonMatrixElement(rows=[scene_launch_buttons_raw], name=u'Scene_Launch_Buttons')
        self.shifted_scene_launch_button_1 = with_shift(scene_launch_buttons_raw[1])
        sliders = [ SpecialFeedbackChannelSliderElement(MIDI_CC_TYPE, DEFAULT_CHANNEL, 41 + index, name=u'Slider_{}'.format(index)) for index in range(SESSION_WIDTH) ]
        for slider in sliders:
            slider.set_feedback_delay(1)

        self.sliders = ButtonMatrixElement(rows=[sliders], name=u'Sliders')
        self.slider_leds = ButtonMatrixElement(rows=[[ create_rgb_led(index + 54, u'Slider_LED_{}'.format(index)) for index in range(8) ]], name=u'Slider_LEDs')
        self.mixer_soft_button_row_0 = ButtonMatrixElement(rows=[[ create_button(identifier, u'Mixer_Soft_Button_{}_0'.format(col_index)) for col_index, identifier in enumerate(range(59, 59 + SESSION_WIDTH)) ]], name=u'Mixer_Soft_Button_Row_0')
        self.mixer_soft_button_row_1 = ButtonMatrixElement(rows=[[ create_button(identifier, u'Mixer_Soft_Button_{}_1'.format(col_index)) for col_index, identifier in enumerate(range(59 + SESSION_WIDTH, 59 + SESSION_WIDTH * 2)) ]], name=u'Mixer_Soft_Button_Row_1')
        self.message_display = SpecialPhysicalDisplayElement(width_in_chars=38, num_segments=NUM_MESSAGE_SEGMENTS, name=u'Message_Display')
        self.message_display.set_message_parts(sysex.SHOW_MESSAGE_MSG_HEADER, (sysex.SYSEX_END_BYTE,))
        self.center_display_1 = mixin(CachingControlElement, ConfigurablePhysicalDisplayElement)(v_position=0, width_in_chars=9, name=u'Center_Display_1')
        self.center_display_2 = mixin(CachingControlElement, ConfigurablePhysicalDisplayElement)(v_position=1, width_in_chars=9, name=u'Center_Display_2')
        self.mixer_display_1 = mixin(CachingControlElement, ConfigurablePhysicalDisplayElement)(v_position=2, width_in_chars=9, name=u'Mixer_Button_Display_1')
        self.mixer_display_2 = mixin(CachingControlElement, ConfigurablePhysicalDisplayElement)(v_position=3, width_in_chars=9, name=u'Mixer_Button_Display_2')
        for display in (self.center_display_1,
         self.center_display_2,
         self.mixer_display_1,
         self.mixer_display_2):
            display.set_message_parts(sysex.SET_PROPERTY_MSG_HEADER, (sysex.SYSEX_END_BYTE,))
            display.segment(0).set_position_identifier((8,))

        self.center_color_field = create_display_color_element(8, 0, u'Center_Color_Field')
        self.mixer_color_field_1 = create_display_color_element(8, 1, u'Mixer_Color_Field_1')
        self.mixer_color_field_2 = create_display_color_element(8, 2, u'Mixer_Color_Field_2')
        self.select_buttons_raw = [ create_button(51 + index, u'Select_Button_{}'.format(index)) for index in range(8) ]
        self.select_buttons = ButtonMatrixElement(rows=[self.select_buttons_raw], name=u'Select_Buttons')
        self.select_buttons_with_shift_raw = [ with_shift(button) for button in self.select_buttons_raw ]
        self.display_layout_switch = SysexElement(name=u'Display_Layout_Switch', send_message_generator=lambda v: sysex.SET_SCREEN_LAYOUT_MESSAGE_HEADER + (v, sysex.SYSEX_END_BYTE), default_value=sysex.EMPTY_SCREEN_LAYOUT_BYTE, optimized=True)
        self.text_display_line_0 = create_text_display_line(0)
        self.text_display_line_1 = create_text_display_line(1)
        self.text_display_line_2 = create_text_display_line(2)
        self.text_display_line_3 = create_text_display_line(3)
        self.text_display_line_5 = create_text_display_line(5)
        self.text_display_line_3_with_shift = with_shift(self.text_display_line_3)
        self.text_display_line_5_with_shift = with_shift(self.text_display_line_5)
        self.text_display_lines = [self.text_display_line_0,
         self.text_display_line_1,
         self.text_display_line_2,
         self.text_display_line_3,
         self.text_display_line_5]
        color_field_line_0_raw, self.color_field_line_0 = create_display_color_element_line(0)
        color_field_line_1_raw, _ = create_display_color_element_line(1)
        self.color_field_line_2_raw, self.color_field_line_2 = create_display_color_element_line(2)
        self.color_field_lines_0_1_flattened = ButtonMatrixElement(rows=[color_field_line_0_raw + color_field_line_1_raw], name=u'Color_Field_Lines_0_1_Flattened')
        self.color_field_line_2_with_shift = ButtonMatrixElement(rows=[[ with_shift(color_field) for color_field in self.color_field_line_2_raw ]], name=u'Color_Field_Line_2_With_Shift')
        selection_field_line_0_raw, _ = create_selection_field_line(0)
        self.selection_field_line_1_raw, self.selection_field_line_1 = create_selection_field_line(1)
        self.selection_field_line_2_raw, self.selection_field_line_2 = create_selection_field_line(2)
        self.selection_field_lines_0_1_flattened = ButtonMatrixElement(rows=[selection_field_line_0_raw + self.selection_field_line_1_raw], name=u'Selection_Field_Lines_0_1_Flattened')
        self.selection_field_line_1_with_shift = ButtonMatrixElement(rows=[[ with_shift(field) for field in self.selection_field_line_1_raw ]], name=u'Selection_Field_Line_1_With_Shift')
        self.selection_field_line_2_with_shift = ButtonMatrixElement(rows=[[ with_shift(field) for field in self.selection_field_line_2_raw ]], name=u'Selection_Field_Line_2_With_Shift')
        encoders = [ EncoderElement(MIDI_CC_TYPE, DEFAULT_CHANNEL, 21 + index, map_mode=Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Encoder_{}'.format(index)) for index in range(8) ]
        for encoder in encoders:
            encoder.set_feedback_delay(1)

        self.encoders = ButtonMatrixElement(rows=[encoders], name=u'Encoders')
        self.encoder_color_fields = ButtonMatrixElement(rows=[[ create_display_color_element(index, 1, u'Encoder_Color_Field_{}'.format(index)) for index in range(8) ]], name=u'Encoder_Color_Fields')
