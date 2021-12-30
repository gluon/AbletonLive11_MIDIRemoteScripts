#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/launchpad_elements.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import object
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, SliderElement, SysexElement
from . import sysex
SESSION_WIDTH = 8
SESSION_HEIGHT = 8
BUTTON_FADER_MAIN_CHANNEL = 4
BUTTON_FADER_COLOR_CHANNEL = 5

@depends(skin=None)
def create_button(identifier, name, msg_type = MIDI_CC_TYPE, channel = 0, **k):
    return ButtonElement(True, msg_type, channel, identifier, name=name, **k)


def create_slider(identifier, name, **k):
    slider = SliderElement(MIDI_CC_TYPE, BUTTON_FADER_MAIN_CHANNEL, identifier, name=name, **k)
    slider.set_needs_takeover(False)
    return slider


class LaunchpadElements(object):
    model_id = 0
    default_layout = 0
    button_fader_cc_offset = 0

    def __init__(self, arrow_button_identifiers = (91, 92, 93, 94), session_mode_button_identifier = 95, *a, **k):
        super(LaunchpadElements, self).__init__(*a, **k)
        self.up_button = create_button(arrow_button_identifiers[0], u'Up_Button')
        self.down_button = create_button(arrow_button_identifiers[1], u'Down_Button')
        self.left_button = create_button(arrow_button_identifiers[2], u'Left_Button')
        self.right_button = create_button(arrow_button_identifiers[3], u'Right_Button')
        self.session_mode_button = create_button(session_mode_button_identifier, u'Session_Mode_Button')
        self.scene_launch_buttons_raw = [ create_button(identifier, u'Scene_Launch_Button_{}'.format(row_index)) for row_index, identifier in enumerate(range(89, 18, -10)) ]
        self.scene_launch_buttons = ButtonMatrixElement(rows=[self.scene_launch_buttons_raw], name=u'Scene_Launch_Buttons')
        self.clip_launch_matrix = ButtonMatrixElement(rows=[ [ create_button(offset + col_index, u'{}_Clip_Launch_Button_{}'.format(col_index, row_index), msg_type=MIDI_NOTE_TYPE) for col_index in range(SESSION_WIDTH) ] for row_index, offset in enumerate(range(81, 10, -10)) ], name=u'Clip_Launch_Matrix')
        self.firmware_mode_switch = SysexElement(name=u'Firmware_Mode_Switch', send_message_generator=lambda v: sysex.STD_MSG_HEADER + (self.model_id,
         sysex.FIRMWARE_MODE_COMMAND_BYTE,
         v,
         sysex.SYSEX_END_BYTE), default_value=sysex.STANDALONE_MODE_BYTE, optimized=True)
        layout_switch_identifier = sysex.STD_MSG_HEADER + (self.model_id, sysex.LAYOUT_COMMAND_BYTE)
        self.layout_switch = SysexElement(name=u'Layout_Switch', sysex_identifier=layout_switch_identifier, send_message_generator=lambda v: layout_switch_identifier + (v if type(v) is tuple else (v,)) + (sysex.SYSEX_END_BYTE,), default_value=self.default_layout, enquire_message=layout_switch_identifier + (sysex.SYSEX_END_BYTE,))

    def _create_scale_feedback_switch(self):
        self.scale_feedback_switch = SysexElement(name=u'Scale_Feedback_Switch', send_message_generator=lambda v: sysex.STD_MSG_HEADER + (self.model_id,
         sysex.SCALE_FEEDBACK_COMMAND_BYTE,
         v,
         sysex.SYSEX_END_BYTE))

    def _create_drum_pads(self):
        drum_pad_rows = ((64, 65, 66, 67, 96, 97, 98, 99),
         (60, 61, 62, 63, 92, 93, 94, 95),
         (56, 57, 58, 59, 88, 89, 90, 91),
         (52, 53, 54, 55, 84, 85, 86, 87),
         (48, 49, 50, 51, 80, 81, 82, 83),
         (44, 45, 46, 47, 76, 77, 78, 79),
         (40, 41, 42, 43, 72, 73, 74, 75),
         (36, 37, 38, 39, 68, 69, 70, 71))
        self.drum_pads = ButtonMatrixElement(rows=[ [ create_button(row_identifiers[col_index], u'Drum_Pad_{}_{}'.format(col_index, row_index), msg_type=MIDI_NOTE_TYPE, channel=8) for col_index in range(SESSION_WIDTH) ] for row_index, row_identifiers in enumerate(drum_pad_rows) ], name=u'Drum_Pads')

    def _create_scale_pads(self):
        self.scale_pads = ButtonMatrixElement(rows=[[ create_button(identifier, u'Scale_Pad_{}'.format(identifier), msg_type=MIDI_NOTE_TYPE, channel=15) for identifier in range(128) ]], name=u'Scale_Pads')

    def _fader_setup_message_generator(self, bank, orientation, polarity):
        return sysex.STD_MSG_HEADER + (self.model_id,
         sysex.FADER_COMMAND_BYTE,
         bank,
         orientation) + tuple((byte for index in range(SESSION_WIDTH) for byte in (index,
         polarity,
         index + bank * SESSION_WIDTH + self.button_fader_cc_offset,
         0))) + (sysex.SYSEX_END_BYTE,)
