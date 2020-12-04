#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/consts.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
import sys
import Live
from ableton.v2.control_surface import DEFAULT_PRIORITY
DISPLAY_LENGTH = 72
SIDE_BUTTON_COLORS = dict(color=u'DefaultButton.On', disabled_color=u'DefaultButton.Disabled')
PROTO_FAST_DEVICE_NAVIGATION = False
PROTO_AUDIO_NOTE_MODE = False
PROTO_SONG_IS_ROOT = False
PROTO_TOUCH_ENCODER_TO_STRIP = False
SHARED_PRIORITY = DEFAULT_PRIORITY
M4L_PRIORITY = DEFAULT_PRIORITY + 7
USER_BUTTON_PRIORITY = DEFAULT_PRIORITY + 6
MESSAGE_BOX_PRIORITY = DEFAULT_PRIORITY + 5
MOMENTARY_DIALOG_PRIORITY = DEFAULT_PRIORITY + 4
SETUP_DIALOG_PRIORITY = DEFAULT_PRIORITY + 3
DIALOG_PRIORITY = DEFAULT_PRIORITY + 2
NOTIFICATION_PRIORITY = DEFAULT_PRIORITY + 1
BACKGROUND_PRIORITY = DEFAULT_PRIORITY - 3
GLOBAL_MAP_MODE = Live.MidiMap.MapMode.relative_smooth_two_compliment
CHAR_ARROW_UP = u'\x00'
CHAR_ARROW_DOWN = u'\x01'
CHAR_ARROW_RIGHT = u'\x1e'
CHAR_ARROW_LEFT = u'\x1f'
CHAR_RACK = u'\x02'
CHAR_BAR_LEFT = u'\x03'
CHAR_BAR_RIGHT = u'\x04'
CHAR_SPLIT_BLOCK = u'\x05'
CHAR_SPLIT_DASH = u'\x06'
CHAR_FOLDER = u'\x07'
CHAR_ELLIPSIS = u'\x1c'
CHAR_FLAT_SIGN = u'\x1b'
CHAR_ELLIPSIS = u'\x1c'
CHAR_FULL_BLOCK = u'\x1d'
CHAR_SELECT = u'\x7f'
GRAPH_VOL = (u'\x03\x06\x06\x06\x06\x06\x06\x06', u'\x05\x06\x06\x06\x06\x06\x06\x06', u'\x05\x03\x06\x06\x06\x06\x06\x06', u'\x05\x05\x06\x06\x06\x06\x06\x06', u'\x05\x05\x03\x06\x06\x06\x06\x06', u'\x05\x05\x05\x06\x06\x06\x06\x06', u'\x05\x05\x05\x03\x06\x06\x06\x06', u'\x05\x05\x05\x05\x06\x06\x06\x06', u'\x05\x05\x05\x05\x03\x06\x06\x06', u'\x05\x05\x05\x05\x05\x06\x06\x06', u'\x05\x05\x05\x05\x05\x03\x06\x06', u'\x05\x05\x05\x05\x05\x05\x06\x06', u'\x05\x05\x05\x05\x05\x05\x03\x06', u'\x05\x05\x05\x05\x05\x05\x05\x06', u'\x05\x05\x05\x05\x05\x05\x05\x03', u'\x05\x05\x05\x05\x05\x05\x05\x05')
GRAPH_PAN = (u'\x05\x05\x05\x05\x06\x06\x06\x06', u'\x04\x05\x05\x05\x06\x06\x06\x06', u'\x06\x05\x05\x05\x06\x06\x06\x06', u'\x06\x04\x05\x05\x06\x06\x06\x06', u'\x06\x06\x05\x05\x06\x06\x06\x06', u'\x06\x06\x04\x05\x06\x06\x06\x06', u'\x06\x06\x06\x05\x06\x06\x06\x06', u'\x06\x06\x06\x04\x06\x06\x06\x06', u'\x06\x06\x06\x04\x03\x06\x06\x06', u'\x06\x06\x06\x06\x03\x06\x06\x06', u'\x06\x06\x06\x06\x05\x06\x06\x06', u'\x06\x06\x06\x06\x05\x03\x06\x06', u'\x06\x06\x06\x06\x05\x05\x06\x06', u'\x06\x06\x06\x06\x05\x05\x03\x06', u'\x06\x06\x06\x06\x05\x05\x05\x06', u'\x06\x06\x06\x06\x05\x05\x05\x03', u'\x06\x06\x06\x06\x05\x05\x05\x05')
GRAPH_SIN = (u'\x03\x06\x06\x06\x06\x06\x06\x06', u'\x04\x06\x06\x06\x06\x06\x06\x06', u'\x06\x03\x06\x06\x06\x06\x06\x06', u'\x06\x04\x06\x06\x06\x06\x06\x06', u'\x06\x06\x03\x06\x06\x06\x06\x06', u'\x06\x06\x04\x06\x06\x06\x06\x06', u'\x06\x06\x06\x03\x06\x06\x06\x06', u'\x06\x06\x06\x04\x06\x06\x06\x06', u'\x06\x06\x06\x06\x03\x06\x06\x06', u'\x06\x06\x06\x06\x04\x06\x06\x06', u'\x06\x06\x06\x06\x06\x03\x06\x06', u'\x06\x06\x06\x06\x06\x04\x06\x06', u'\x06\x06\x06\x06\x06\x06\x03\x06', u'\x06\x06\x06\x06\x06\x06\x04\x06', u'\x06\x06\x06\x06\x06\x06\x06\x03', u'\x06\x06\x06\x06\x06\x06\x06\x04')
DISTANT_FUTURE = 999999

class MessageBoxText(object):
    LIVE_DIALOG = u'\n                    Live is showing a dialog' + u'\n                    that needs your attention.'
    CLIP_DUPLICATION_FAILED = u'\n                     The clip could not be duplicated' + u'\n                      because it is recording'
    SCENE_LIMIT_REACHED = u'\n                  No more scene can be inserted' + u'\n                   for this version of Live'
    SCENE_DUPLICATION_FAILED = u'\n                  This scene cannot be duplicated' + u'\n                      because it is recording'
    TRACK_LIMIT_REACHED = u'\n                  No more track can be inserted' + u'\n                   for this version of Live'
    MAX_RETURN_TRACKS_REACHED = u'\n                  Maximum number of return tracks' + u'\n                  reached'
    TRACK_DUPLICATION_FAILED = u'\n                  This track cannot be duplicated' + u'\n                      because it is recording'
    TRACK_DELETE_FAILED = u'\n                  This track cannot be deleted' + u'\n                      because it is recording'
    DELETE_TRACK = u'                  Track deleted:    %s'
    DUPLICATE_TRACK = u'                  Track duplicated: %s'
    DELETE_CLIP = u'                  Clip deleted:     %s'
    DUPLICATE_CLIP = u'                  Clip duplicated:  %s'
    QUANTIZE_CLIP = u'                  Quantized to:     %(to)s, %(amount)s'
    QUANTIZE_CLIP_PITCH = u'                Quantized %(source)s to:   %(to)s, %(amount)s'
    DELETE_NOTES = u'                  Notes deleted:    %s'
    CAPTURE_AND_INSERT_SCENE = u'                      Duplicated to scene %s'
    DUPLICATE_LOOP = u'                   New loop length: %(length)s'
    DELETE_SCENE = u'                  Scene deleted:    %s'
    DUPLICATE_SCENE = u'                  Scene duplicated: %s'
    DELETE_ENVELOPE = u'                  Delete automation %(automation)s'
    DEFAULT_PARAMETER_VALUE = u'                  Reset to default: %(automation)s'
    DELETE_DRUM_RACK_PAD = u'                  Drum Pad deleted: %s'
    DELETE_SLICE = u'       Slice %s   deleted'
    FIXED_LENGTH = u'                      Fixed Length: %s'
    EMPTY_DEVICE_CHAIN = u'\n\n               No Devices.    Press [Browse] to add a device.'
    STUCK_PAD_WARNING = u'         Warning: Low threshold may cause stuck pads'
    UNDO = u'            Undo:     Reverted last action'
    REDO = u'            Redo: Re-performed last undone action'
    TRACK_FROZEN_INFO = u'                    ' + u'Cannot modify a frozen track'
    SELECTED_CLIP_BLINK = u' Press            to edit playing   clip'
    PLAYING_CLIP_ABOVE_SELECTED_CLIP = u' Press Up Arrow   to edit playing   clip'
    PLAYING_CLIP_BELOW_SELECTED_CLIP = u' Press Down Arrow to edit playing   clip'
    TOUCHSTRIP_PITCHBEND_MODE = u'                  Touchstrip Mode:  Pitchbend'
    TOUCHSTRIP_MODWHEEL_MODE = u'                  Touchstrip Mode:  Modwheel'
    COPIED_DRUM_PAD = u'     Pad %len=8,s copied.           Press destination pad to paste'
    PASTED_DRUM_PAD = u'     Pad %len=8,s duplicated to     %len=8,s'
    CANNOT_COPY_EMPTY_DRUM_PAD = u'                  Cannot copy empty drum pad'
    CANNOT_PASTE_TO_SOURCE_DRUM_PAD = u'                    Cannot paste to source drum pad'
    COPIED_STEP = u'     Note(s) copied.           Press destination step to paste'
    PASTED_STEP = u'     Note(s) duplicated.'
    COPIED_PAGE = u'     Page copied.           Press destination page to paste'
    PASTED_PAGE = u'     Page duplicated.'
    CANNOT_COPY_EMPTY_PAGE = u'                  Cannot copy empty page'
    CANNOT_PASTE_TO_SOURCE_PAGE = u'                    Cannot paste to source page'
    CANNOT_PASTE_FROM_STEP_TO_PAGE = u'                    Cannot paste from step to page'
    CANNOT_COPY_EMPTY_STEP = u'                  Cannot copy empty step'
    CANNOT_PASTE_TO_SOURCE_STEP = u'                    Cannot paste to source step'
    PAGE_CLEARED = u'                    Page cleared'
    CANNOT_CLEAR_EMPTY_PAGE = u'                    Cannot clear empty page'
    CANNOT_PASTE_FROM_PAGE_TO_STEP = u'                    Cannot paste from page to step'
    COPIED_CLIP = u'         %len=8,s copied.     Press destination clip  slot to paste'
    PASTED_CLIP = u'         %len=8,s duplicated to:    %len=17,s'
    CANNOT_COPY_EMPTY_CLIP = u' Cannot copy from empty clip slot'
    CANNOT_COPY_GROUP_SLOT = u'      Group clips cannot be copied'
    CANNOT_COPY_RECORDING_CLIP = u'      Cannot copy recording clip'
    CANNOT_COPY_AUDIO_CLIP_TO_MIDI_TRACK = u'     Please paste this audio clip       into an audio track'
    CANNOT_COPY_MIDI_CLIP_TO_AUDIO_TRACK = u'     Please paste this MIDI clip    into a MIDI track'
    CANNOT_PASTE_INTO_GROUP_SLOT = u'    A clip cannot be pasted into a  group track'
    LAYOUT_DRUMS_LOOP = u'          Drums:  Loop Selector'
    LAYOUT_DRUMS_LEVELS = u'          Drums:  16 Velocities'
    LAYOUT_DRUMS_64_PADS = u'          Drums:  64 Pads'
    LAYOUT_SLICING_LOOP = u'        Slicing:  Loop Selector'
    LAYOUT_SLICING_LEVELS = u'        Slicing:  16 Velocities'
    LAYOUT_SLICING_64_PADS = u'        Slicing:  64 Slices'
    ALTERNATE_LOOP_SELECTOR = u'          Loop Selector'
    ALTERNATE_16_VELOCITIES = u'          16 Velocities'
    ALTERNATE_56_PADS = u'          Loop Selector'
    ALTERNATE_PLAY_LOOP = u'          Loop Selector'
    ALTERNATE_SEQUENCE_LOOP = u'          Loop Selector'
    LAYOUT_MELODIC_PLAYING = u'        Melodic:  64 Notes'
    LAYOUT_MELODIC_SEQUENCER = u'        Melodic:  Sequencer'
    LAYOUT_MELODIC_32_PADS = u'        Melodic:  Sequencer  +  32  Notes'
    LAYOUT_MELODIC_32_PADS_LOOP_SELECTOR = u'        Loop Selector'
    LAYOUT_SESSION_VIEW = u' Session View'
    LAYOUT_SESSION_OVERVIEW = u' Session Overview'


_test_mode = __builtins__.get(u'TEST_MODE', False)
if not _test_mode:
    try:
        _this_module = sys.modules[__name__]
        _proto_list = [ a for a in dir(_this_module) if a.startswith(u'PROTO_') ]
        for attr in _proto_list:
            try:
                _local_consts = __import__(u'local_consts', globals(), locals(), [attr])
                setattr(_this_module, attr, getattr(_local_consts, attr))
            except AttributeError:
                pass

    except ImportError:
        pass
