# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/fantom.py
# Compiled at: 2022-01-28 05:06:23
# Size of source mod 2**32: 5669 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, Layer
from ableton.v3.control_surface.components import DeviceComponent, DrumGroupComponent, SessionNavigationComponent, SessionRecordingComponent, UndoRedoComponent
from . import sysex
from .colors import Rgb
from .elements import NUM_SCENES, NUM_TRACKS, Elements
from .mixer import MixerComponent
from .session import SessionComponent
from .skin import skin
from .transport import TransportComponent
DRUM_FEEDBACK_CHANNEL = 15

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = skin
    num_tracks = NUM_TRACKS
    num_scenes = NUM_SCENES
    include_returns = True
    feedback_channels = [DRUM_FEEDBACK_CHANNEL]
    playing_feedback_velocity = Rgb.GREEN.midi_value
    recording_feedback_velocity = Rgb.RED.midi_value
    custom_identity_response = sysex.REFRESH_REQUEST
    identity_request = sysex.INITIATE_CONNECTION
    identity_request_delay = 10.0


class FANTOM(ControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(a, specification=Specification, **k)

    def _create_control_surface(self):
        self._create_transport()
        self._create_session_recording()
        self._create_undo()
        self._create_device_parameters()
        self._create_session_navigation()
        self._create_session()
        self._create_mixer()
        self._create_drum_group()
        self.set_is_observing_instruments(True)
        self.set_can_update_controlled_track(True)

    def disconnect(self):
        self._send_midi(sysex.TERMINATE_CONNECTION)
        super().disconnect()

    def _create_transport(self):
        self._transport = TransportComponent(is_enabled=False,
          layer=Layer(play_button='play_button',
          stop_button='stop_button',
          arrangement_record_button='record_button',
          metronome_button='metronome_button',
          arrangement_overdub_button='arrangement_overdub_button',
          tap_tempo_button='tap_tempo_button',
          capture_midi_button='capture_midi_button',
          tempo_coarse_control='tempo_coarse_control',
          tempo_fine_control='tempo_fine_control',
          beat_time_display='beat_time_display',
          tempo_display='tempo_display'))
        self._transport.set_enabled(True)

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(name='Session_Recording',
          is_enabled=False,
          layer=Layer(record_button='session_record_button',
          re_enable_automation_button='automation_re-enable_button',
          automation_button='automation_arm_button'))
        self._session_recording.set_enabled(True)

    def _create_undo(self):
        self._undo = UndoRedoComponent(is_enabled=False,
          layer=Layer(undo_button='undo_button'))
        self._undo.set_enabled(True)

    def _create_device_parameters(self):
        self._device_parameters = DeviceComponent(is_enabled=False,
          layer=Layer(parameter_controls='device_controls'))
        self._device_parameters.set_enabled(True)

    def _create_session_navigation(self):
        self._session_navigation = SessionNavigationComponent(is_enabled=False,
          layer=Layer(up_button='up_button',
          down_button='down_button',
          left_button='left_button',
          right_button='right_button'))
        self._session_navigation.set_enabled(True)

    def _create_session(self):
        self._session = SessionComponent(is_enabled=False,
          layer=Layer(clip_launch_buttons='clip_launch_buttons',
          scene_launch_buttons='scene_launch_buttons',
          stop_track_clip_buttons='stop_track_buttons',
          stop_all_clips_button='stop_all_clips_button',
          track_select_control='track_select_control',
          scene_name_display='scene_name_display'))
        self._session.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(is_enabled=False,
          layer=Layer(volume_controls='volume_controls',
          pan_controls='pan_controls',
          send_a_controls='send_a_controls',
          send_b_controls='send_b_controls',
          track_select_control='track_select_control',
          arm_buttons='arm_buttons',
          solo_buttons='solo_buttons',
          mute_buttons='mute_buttons',
          track_info_display='track_info_display',
          master_track_volume_control='master_volume_control',
          master_track_pan_control='master_pan_control'))
        self._mixer.set_enabled(True)

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(is_enabled=False,
          translation_channel=DRUM_FEEDBACK_CHANNEL,
          layer=Layer(matrix='drum_pads'),
          full_velocity=(self._c_instance.full_velocity))
        self._drum_group.set_enabled(True)

    def drum_group_changed(self, drum_group):
        self._drum_group.set_drum_group_device(drum_group)