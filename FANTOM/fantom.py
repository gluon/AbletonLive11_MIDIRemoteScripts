# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/fantom.py
# Compiled at: 2021-08-06 01:27:35
# Size of source mod 2**32: 9707 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, inject, listens
from ableton.v2.control_surface import IdentifiableControlSurface, Layer, PercussionInstrumentFinder, midi
from ableton.v2.control_surface.components import SessionNavigationComponent, SessionRecordingComponent, SessionRingComponent, UndoRedoComponent
from novation.simple_device import SimpleDeviceParameterComponent
from . import sysex
from .colors import Rgb
from .drum_group import DrumGroupComponent
from .elements import NUM_SCENES, NUM_TRACKS, Elements
from .mixer import MixerComponent
from .session import SessionComponent
from .skin import skin
from .transport import TransportComponent
DRUM_FEEDBACK_CHANNEL = 15

def is_song_recording(song):
    return song.session_record or song.record_mode


def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


class FANTOM(IdentifiableControlSurface):
    identity_request = sysex.INITIATE_CONNECTION

    def __init__(self, *a, **k):
        (super(FANTOM, self).__init__)(a, product_id_bytes=(0, 91), **k)
        with self.component_guard():
            with inject(skin=(const(skin))).everywhere():
                self._elements = Elements()
        with self.component_guard():
            with inject(element_container=(const(self._elements))).everywhere():
                self._create_transport()
                self._create_session_recording()
                self._create_undo()
                self._create_device_parameters()
                self._create_session_ring()
                self._create_session_navigation()
                self._create_session()
                self._create_mixer()
                self._create_drum_group()
                self._create_drum_group_finder_and_listeners()

    def disconnect(self):
        self._send_midi(sysex.TERMINATE_CONNECTION)
        super(FANTOM, self).disconnect()

    def on_identified(self, response_bytes):
        self._session_ring.set_enabled(True)
        self.set_feedback_channels([DRUM_FEEDBACK_CHANNEL])
        self._set_feedback_velocity()
        super(FANTOM, self).on_identified(response_bytes)

    def port_settings_changed(self):
        self._session_ring.set_enabled(False)
        super(FANTOM, self).port_settings_changed()

    def process_midi_bytes(self, midi_bytes, midi_processor):
        if midi.is_sysex(midi_bytes):
            if self._is_identity_response(midi_bytes):
                if self._identity_response_pending:
                    self._send_midi(self.identity_request)
        super(FANTOM, self).process_midi_bytes(midi_bytes, midi_processor)

    def _is_identity_response(self, midi_bytes):
        return len(midi_bytes) > sysex.REFRESH_REQUEST_LENGTH and midi_bytes[:sysex.REFRESH_REQUEST_LENGTH] == sysex.REFRESH_REQUEST

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(play_button='play_button',
          stop_button='stop_button',
          record_button='record_button',
          metronome_button='metro_button',
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
          re_enable_automation_button='automation_re_enable_button',
          automation_button='automation_arm_button'))
        self._session_recording.set_enabled(True)

    def _create_undo(self):
        self._undo = UndoRedoComponent(name='Undo',
          is_enabled=False,
          layer=Layer(undo_button='undo_button'))
        self._undo.undo_button.color = 'DefaultButton.Off'
        self._undo.set_enabled(True)

    def _create_device_parameters(self):
        self._device_parameters = SimpleDeviceParameterComponent(name='Device_Parameters',
          is_enabled=False,
          layer=Layer(parameter_controls='device_controls'))
        self._device_parameters.set_enabled(True)

    def _create_session_ring(self):
        self._session_ring = SessionRingComponent(name='Session_Ring',
          is_enabled=False,
          num_tracks=NUM_TRACKS,
          num_scenes=NUM_SCENES,
          tracks_to_use=(lambda : tuple(self.song.visible_tracks) + tuple(self.song.return_tracks)))

    def _create_session_navigation(self):
        self._session_navigation = SessionNavigationComponent(name='Session_Navigation',
          is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(up_button='up_button',
          down_button='down_button',
          left_button='left_button',
          right_button='right_button'))
        self._session_navigation.set_enabled(True)

    def _create_session(self):
        self._session = SessionComponent(name='Session',
          is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(clip_launch_buttons='clip_launch_buttons',
          scene_launch_buttons='scene_launch_buttons',
          stop_track_clip_buttons='stop_track_buttons',
          stop_all_clips_button='stop_all_clips_button',
          track_select_control='track_select_control',
          scene_name_display='scene_name_display'))
        self._session.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(name='Mixer',
          is_enabled=False,
          tracks_provider=(self._session_ring),
          layer=Layer(volume_controls='volume_controls',
          pan_controls='pan_controls',
          send_controls='send_controls',
          track_select_control='track_select_control',
          arm_buttons='arm_buttons',
          solo_buttons='solo_buttons',
          mute_buttons='mute_buttons',
          track_info_display='track_info_display'))
        self._mixer.master_strip().layer = Layer(volume_control='master_volume_control',
          pan_control='master_pan_control')
        self._mixer.set_enabled(True)

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(name='Drum_Group',
          is_enabled=False,
          translation_channel=DRUM_FEEDBACK_CHANNEL,
          layer=Layer(matrix='drum_pads'))
        self._drum_group.set_enabled(True)

    def _create_drum_group_finder_and_listeners(self):
        self._drum_group_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=(self.song.view.selected_track)))
        self._FANTOM__on_selected_track_changed.subject = self.song.view
        self._FANTOM__on_drum_group_changed.subject = self._drum_group_finder
        self._FANTOM__on_session_record_changed.subject = self.song
        self._FANTOM__on_record_mode_changed.subject = self.song
        self._FANTOM__on_selected_track_changed()
        self._FANTOM__on_drum_group_changed()

    def _set_feedback_velocity(self):
        track = self.song.view.selected_track
        if is_song_recording(self.song) and track_can_record(track):
            feedback_velocity = Rgb.RED.midi_value
        else:
            feedback_velocity = Rgb.GREEN.midi_value
        self._c_instance.set_feedback_velocity(int(feedback_velocity))

    @listens('selected_track')
    def __on_selected_track_changed(self):
        track = self.song.view.selected_track
        self._drum_group_finder.device_parent = track
        self._FANTOM__on_selected_track_arm_changed.subject = track
        self._FANTOM__on_selected_track_implicit_arm_changed.subject = track
        self.set_controlled_track(self.song.view.selected_track)

    @listens('instrument')
    def __on_drum_group_changed(self):
        self._drum_group.set_drum_group_device(self._drum_group_finder.drum_group)

    @listens('session_record')
    def __on_session_record_changed(self):
        self._set_feedback_velocity()

    @listens('record_mode')
    def __on_record_mode_changed(self):
        self._set_feedback_velocity()

    @listens('arm')
    def __on_selected_track_arm_changed(self):
        self._set_feedback_velocity()

    @listens('implicit_arm')
    def __on_selected_track_implicit_arm_changed(self):
        self._set_feedback_velocity()