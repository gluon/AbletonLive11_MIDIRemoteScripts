#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/elements.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import object
from functools import partial
import Live
from ableton.v2.base import depends, recursive_map
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement
SESSION_WIDTH = 4
SESSION_HEIGHT = 4

@depends(skin=None)
def create_button(identifier, name, msg_type = MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, 0, identifier, name=name, **k)


def create_encoder(identifier, name, **k):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.relative_smooth_signed_bit, name=name, **k)


class Elements(object):

    def __init__(self, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.shift_button = create_button(32, u'Shift_Button', resource_type=PrioritizedResource)
        self.zoom_button = create_button(104, u'Zoom_Button', resource_type=PrioritizedResource)
        self.note_repeat_button = create_button(24, u'Note_Repeat_Button')
        self.full_level_button = create_button(25, u'Full_Level_Button')
        self.bank_button = create_button(26, u'Bank_Button')
        self.preset_button = create_button(27, u'Preset_Button')
        self.show_hide_button = create_button(29, u'Show_Hide_Button')
        self.nudge_button = create_button(30, u'Nudge_Button')
        self.editor_button = create_button(31, u'Editor_Button')
        self.set_loop_button = create_button(85, u'Set_Loop_Button')
        self.setup_button = create_button(86, u'Setup_Button')
        self.up_button = create_button(87, u'Up_Button')
        self.down_button = create_button(89, u'Down_Button')
        self.left_button = create_button(90, u'Left_Button')
        self.right_button = create_button(102, u'Right_Button')
        self.select_button = create_button(103, u'Select_Button')
        self.click_button = create_button(105, u'Click_Button')
        self.record_button = create_button(107, u'Record_Button')
        self.play_button = create_button(109, u'Play_Button')
        self.stop_button = create_button(111, u'Stop_Button')
        self.pads_raw = [ [ create_button(offset + col_index, u'{}_Pad_{}'.format(col_index, row_index), msg_type=MIDI_NOTE_TYPE) for col_index in range(SESSION_WIDTH) ] for row_index, offset in enumerate(range(48, 32, -4)) ]
        self.pads = ButtonMatrixElement(rows=self.pads_raw, name=u'Pads')

        def with_modifier(modifier_button, button):
            return ComboElement(control=button, modifier=modifier_button, name=u'{}_With_{}'.format(button.name, modifier_button.name.split(u'_')[0]))

        self.play_button_with_shift = with_modifier(self.shift_button, self.play_button)
        self.stop_button_with_shift = with_modifier(self.shift_button, self.stop_button)
        self.pads_with_shift = ButtonMatrixElement(name=u'Pads_With_Shift', rows=recursive_map(partial(with_modifier, self.shift_button), self.pads_raw))
        self.pads_with_zoom = ButtonMatrixElement(name=u'Pads_With_Zoom', rows=recursive_map(partial(with_modifier, self.zoom_button), self.pads_raw))
        self.encoders = ButtonMatrixElement(rows=[[ create_encoder(index + 14, u'Encoder_{}'.format(index)) for index in range(4) ]], name=u'Encoders')
