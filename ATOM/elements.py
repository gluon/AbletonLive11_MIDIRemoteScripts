<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import MIDI_NOTE_TYPE, ElementsBase, MapMode, create_matrix_identifiers
SESSION_WIDTH = 4
SESSION_HEIGHT = 4

class Elements(ElementsBase):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self.add_modifier_button(32, 'Shift_Button')
        self.add_modifier_button(104, 'Zoom_Button')
        self.add_button(24, 'Note_Repeat_Button')
        self.add_button(25, 'Full_Level_Button')
        self.add_button(26, 'Bank_Button')
        self.add_button(27, 'Preset_Button')
        self.add_button(29, 'Show_Hide_Button')
        self.add_button(30, 'Nudge_Button')
        self.add_button(31, 'Editor_Button')
        self.add_button(85, 'Set_Loop_Button')
        self.add_button(86, 'Setup_Button')
        self.add_button(87, 'Up_Button')
        self.add_button(89, 'Down_Button')
        self.add_button(90, 'Left_Button')
        self.add_button(102, 'Right_Button')
        self.add_button(103, 'Select_Button')
        self.add_button(105, 'Click_Button')
        self.add_button(107, 'Record_Button')
        self.add_button(109, 'Play_Button')
        self.add_button(111, 'Stop_Button')
        self.add_button_matrix(create_matrix_identifiers(36, 52, width=4, flip_rows=True),
          'Pads',
          msg_type=MIDI_NOTE_TYPE,
          is_rgb=True)
        self.add_encoder_matrix([
         list(range(14, 18))],
          'Encoders', map_mode=(MapMode.LinearSignedBit))
        self.add_modified_control(control=(self.play_button), modifier=(self.shift_button))
        self.add_modified_control(control=(self.stop_button), modifier=(self.shift_button))
        self.add_modified_control(control=(self.pads), modifier=(self.zoom_button))
        self.add_modified_control(control=(self.pads), modifier=(self.shift_button))
        self.add_submatrix((self.pads), 'Pads_Row_0', rows=(0, 1))
        self.add_submatrix((self.pads), 'Pads_Row_1', rows=(1, 2))
        self.add_submatrix((self.pads), 'Pads_Row_2', rows=(2, 3))
        self.add_submatrix((self.pads), 'Pads_Row_3', rows=(3, 4))
        self.add_submatrix((self.pads_with_shift),
          'Pads_Column_3_With_Shift', columns=(3, 4))
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/elements.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4131 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
from functools import partial
import Live
from ableton.v2.base import depends, recursive_map
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, InputControlElement, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement
SESSION_WIDTH = 4
SESSION_HEIGHT = 4

@depends(skin=None)
def create_button(identifier, name, msg_type=MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, 0, identifier, name=name, **k)


def create_encoder(identifier, name, **k):
    return EncoderElement(
 MIDI_CC_TYPE,
 0,
 identifier,
 Live.MidiMap.MapMode.relative_smooth_signed_bit, name=name, **k)


class Elements(object):

    def __init__(self, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.shift_button = create_button(32,
          'Shift_Button', resource_type=PrioritizedResource)
        self.zoom_button = create_button(104,
          'Zoom_Button', resource_type=PrioritizedResource)
        self.note_repeat_button = create_button(24, 'Note_Repeat_Button')
        self.full_level_button = create_button(25, 'Full_Level_Button')
        self.bank_button = create_button(26, 'Bank_Button')
        self.preset_button = create_button(27, 'Preset_Button')
        self.show_hide_button = create_button(29, 'Show_Hide_Button')
        self.nudge_button = create_button(30, 'Nudge_Button')
        self.editor_button = create_button(31, 'Editor_Button')
        self.set_loop_button = create_button(85, 'Set_Loop_Button')
        self.setup_button = create_button(86, 'Setup_Button')
        self.up_button = create_button(87, 'Up_Button')
        self.down_button = create_button(89, 'Down_Button')
        self.left_button = create_button(90, 'Left_Button')
        self.right_button = create_button(102, 'Right_Button')
        self.select_button = create_button(103, 'Select_Button')
        self.click_button = create_button(105, 'Click_Button')
        self.record_button = create_button(107, 'Record_Button')
        self.play_button = create_button(109, 'Play_Button')
        self.stop_button = create_button(111, 'Stop_Button')
        self.pads_raw = [[create_button((offset + col_index), ('{}_Pad_{}'.format(col_index, row_index)), msg_type=MIDI_NOTE_TYPE) for col_index in range(SESSION_WIDTH)] for row_index, offset in enumerate(range(48, 32, -4))]
        self.pads = ButtonMatrixElement(rows=(self.pads_raw), name='Pads')

        def with_modifier(modifier_button, button):
            return ComboElement(control=button,
              modifier=modifier_button,
              name=('{}_With_{}'.format(button.name, modifier_button.name.split('_')[0])))

        self.play_button_with_shift = with_modifier(self.shift_button, self.play_button)
        self.stop_button_with_shift = with_modifier(self.shift_button, self.stop_button)
        self.pads_with_shift = ButtonMatrixElement(name='Pads_With_Shift',
          rows=(recursive_map(partial(with_modifier, self.shift_button), self.pads_raw)))
        self.pads_with_zoom = ButtonMatrixElement(name='Pads_With_Zoom',
          rows=(recursive_map(partial(with_modifier, self.zoom_button), self.pads_raw)))
        self.encoders = ButtonMatrixElement(rows=[
         [create_encoder(index + 14, 'Encoder_{}'.format(index)) for index in range(4)]],
          name='Encoders')
        self.native_mode_reply_element = InputControlElement(MIDI_CC_TYPE,
          15, 127, name='Native_Mode_Reply_Element')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
