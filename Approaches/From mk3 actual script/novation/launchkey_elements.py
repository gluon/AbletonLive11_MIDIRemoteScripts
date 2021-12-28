#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/launchkey_elements.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement
SESSION_WIDTH = 8
SESSION_HEIGHT = 2
DRUM_CHANNEL = 9

@depends(skin=None)
def create_button(identifier, name, msg_type = MIDI_CC_TYPE, channel = 15, **k):
    return ButtonElement(True, msg_type, channel, identifier, name=name, **k)


def create_encoder(identifier, name, **k):
    return EncoderElement(MIDI_CC_TYPE, 15, identifier, Live.MidiMap.MapMode.absolute, name=name, **k)


class LaunchkeyElements(object):

    def __init__(self, *a, **k):
        super(LaunchkeyElements, self).__init__(*a, **k)
        self.right_button = create_button(102, u'Right_Button')
        self.left_button = create_button(103, u'Left_Button')
        self.shift_button = create_button(108, u'Shift_Button', resource_type=PrioritizedResource, channel=0)
        self.play_button = create_button(115, u'Play_Button')
        self.record_button = create_button(117, u'Record_Button')
        self.scene_launch_buttons_raw = [create_button(104, u'Scene_Launch_Button', channel=0), create_button(105, u'Stop_Solo_Mute_Button', channel=0)]
        self.scene_launch_buttons = ButtonMatrixElement(rows=[self.scene_launch_buttons_raw], name=u'Scene_Launch_Buttons')
        self.clip_launch_matrix = ButtonMatrixElement(rows=[ [ create_button(offset + col_index, u'{}_Clip_Launch_Button_{}'.format(col_index, row_index), msg_type=MIDI_NOTE_TYPE, channel=0) for col_index in range(SESSION_WIDTH) ] for row_index, offset in enumerate(range(96, 119, 16)) ], name=u'Clip_Launch_Matrix')
        drum_pad_rows = ((48, 49, 50, 51),
         (44, 45, 46, 47),
         (40, 41, 42, 43),
         (36, 37, 38, 39))
        self.drum_pads = ButtonMatrixElement(rows=[ [ create_button(row_identifiers[col_index], u'Drum_Pad_{}_{}'.format(col_index, row_index), msg_type=MIDI_NOTE_TYPE, channel=DRUM_CHANNEL) for col_index in range(4) ] for row_index, row_identifiers in enumerate(drum_pad_rows) ], name=u'Drum_Pads')
        self.pots = ButtonMatrixElement(rows=[[ create_encoder(index + 21, u'Pot_{}'.format(index)) for index in range(SESSION_WIDTH) ]], name=u'Pots')
        self.incontrol_mode_switch = create_button(12, u'InControl_Mode_Switch', msg_type=MIDI_NOTE_TYPE)
        self.pad_layout_switch = create_button(3, u'Pad_Layout_Switch')
        self.pot_layout_switch = create_button(9, u'Pot_Layout_Switch')
