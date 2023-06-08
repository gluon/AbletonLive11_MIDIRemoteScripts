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