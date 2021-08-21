# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/elements.py
# Compiled at: 2021-08-05 15:33:19
# Size of source mod 2**32: 8070 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement
from . import sysex
from .ringed_encoder import RingedEncoderElement
from .scene_name_display import SceneNameDisplayElement
from .simple_display import SimpleDisplayElement
from .track_info_display import TrackInfoDisplayElement
NUM_TRACKS = 6
NUM_SCENES = 8

@depends(skin=None)
def create_button(identifier, name, channel=0, msg_type=MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, channel, identifier, name=name, **k)


def create_encoder(identifier, name, channel=0, map_mode=Live.MidiMap.MapMode.absolute, element_class=EncoderElement, **k):
    encoder = element_class(MIDI_CC_TYPE, channel, identifier, map_mode, name=name, **k)
    encoder.set_needs_takeover(False)
    return encoder


class Elements(object):

    def __init__(self, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.up_button = create_button(1, 'Up_Button')
        self.down_button = create_button(2, 'Down_Button')
        self.left_button = create_button(3, 'Left_Button')
        self.right_button = create_button(4, 'Right_Button')
        self.stop_all_clips_button = create_button(64, 'Stop_All_Clips_Button')
        self.play_button = create_button(80, 'Play_Button')
        self.stop_button = create_button(81, 'Stop_Button')
        self.record_button = create_button(82, 'Record_Button')
        self.undo_button = create_button(83, 'Undo_Button')
        self.metro_button = create_button(84, 'Metronome_Button')
        self.session_record_button = create_button(85, 'Session_Record_Button')
        self.capture_midi_button = create_button(86, 'Capture_Midi_Button')
        self.automation_re_enable_button = create_button(87, 'Automation_Re-enable_Button')
        self.automation_arm_button = create_button(88, 'Automation_Arm_Button')
        self.arrangement_overdub_button = create_button(89, 'Arrangement_Overdub_Button')
        self.tap_tempo_button = create_button(91, 'Tap_Tempo_Button')
        for group_index, root_name in enumerate(('Arm', 'Solo', 'Mute')):
            setattr(self, '{}_buttons'.format(root_name.lower()), ButtonMatrixElement(name=('{}_Buttons'.format(root_name)),
              rows=[
             [create_button((group_index + 65), ('{}_Button_{}'.format(root_name, sub_index)), channel=(sub_index + 1)) for sub_index in range(NUM_TRACKS)]]))

        self.stop_track_buttons = ButtonMatrixElement(name='Stop_Track_Buttons',
          rows=[
         [create_button(64, ('Stop_Track_Button_{}'.format(row_index)), channel=(row_index + 1)) for row_index in range(NUM_SCENES)]])
        self.scene_launch_buttons = ButtonMatrixElement(name='Scene_Launch_Buttons',
          rows=[
         [create_button(row_index, ('Scene_Launch_Button_{}'.format(row_index)), msg_type=MIDI_NOTE_TYPE) for row_index in range(NUM_SCENES)]])
        self.clip_launch_buttons = ButtonMatrixElement(name='Clip_Launch_Buttons',
          rows=[[create_button((col_index + NUM_SCENES + row_index * NUM_TRACKS), ('{}_Clip_Launch_Button_{}'.format(col_index, row_index)), msg_type=MIDI_NOTE_TYPE) for col_index in range(NUM_TRACKS)] for row_index in range(NUM_SCENES)])
        self.drum_pads = ButtonMatrixElement(name='Drum_Pads',
          rows=[[create_button((col_index + 60 + row_index * 4), ('{}_Drum_Pad_{}'.format(col_index, row_index)), msg_type=MIDI_NOTE_TYPE, channel=9) for col_index in range(4)] for row_index in range(4)])
        self.tempo_coarse_control = create_encoder(34,
          'Tempo_Coarse_Control',
          map_mode=(Live.MidiMap.MapMode.relative_smooth_binary_offset))
        self.tempo_fine_control = create_encoder(35,
          'Tempo_Fine_Control',
          map_mode=(Live.MidiMap.MapMode.relative_smooth_binary_offset))
        self.master_pan_control = create_encoder(72, 'Master_Pan_Control')
        self.master_volume_control = create_encoder(73, 'Master_Volume_Control')
        self.track_select_control = create_encoder(96,
          'Track_Select_Control', resource_type=PrioritizedResource)
        self.device_controls = ButtonMatrixElement(name='Device_Controls',
          rows=[
         [create_encoder((index + 16), ('Device_Control_{}'.format(index)), element_class=RingedEncoderElement) for index in range(8)]])
        self.pan_controls = ButtonMatrixElement(name='Pan_Controls',
          rows=[
         [create_encoder(72, ('Pan_Control_{}'.format(index)), channel=(index + 1)) for index in range(NUM_TRACKS)]])
        self.volume_controls = ButtonMatrixElement(name='Volume_Controls',
          rows=[
         [create_encoder(73, ('Volume_Control_{}'.format(index)), channel=(index + 1)) for index in range(NUM_TRACKS)]])
        self.send_controls = ButtonMatrixElement(name='Send_Controls',
          rows=[
         [create_encoder(74, ('Send_A_Control_{}'.format(index)), channel=(index + 1)) for index in range(NUM_TRACKS)],
         [create_encoder(75, ('Send_B_Control_{}'.format(index)), channel=(index + 1)) for index in range(NUM_TRACKS)]])
        self.beat_time_display = SimpleDisplayElement((sysex.BEAT_TIME_DISPLAY_HEADER),
          (
         0, sysex.SYSEX_END_BYTE),
          name='Beat Time Display')
        self.tempo_display = SimpleDisplayElement((sysex.TEMPO_DISPLAY_HEADER),
          (0, sysex.SYSEX_END_BYTE), name='Tempo Display')
        self.track_info_display = TrackInfoDisplayElement((sysex.TRACK_INFO_DISPLAY_HEADER),
          (
         sysex.SYSEX_END_BYTE,),
          name='Track_Info_Display')
        self.scene_name_display = SceneNameDisplayElement((sysex.SCENE_NAME_DISPLAY_HEADER),
          (
         sysex.SYSEX_END_BYTE,),
          name='Scene_Name_Display')