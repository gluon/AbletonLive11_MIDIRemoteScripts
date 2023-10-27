# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\komplete_kontrol_base.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 14742 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from functools import partial
from ableton.v2.base import listens, nop, task
from ableton.v2.control_surface import Layer, SimpleControlSurface, midi
from ableton.v2.control_surface.components import AutoArmComponent, BackgroundComponent, SessionRecordingComponent, SimpleTrackAssigner, UndoRedoComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement, MultiElement, SysexElement
from ableton.v2.control_surface.mode import AddLayerMode, EnablingMode, ModesComponent
from . import sysex
from .channel_strip_component import ChannelStripComponent
from .clip_launch_component import ClipLaunchComponent
from .control_element_util import MIDI_CHANNEL, create_button, create_display_line, create_encoder, create_sysex_element
from .detail_clip_component import DetailClipComponent
from .focus_follow_component import FocusFollowComponent
from .mixer_component import MixerComponent
from .selection_linked_session_ring_component import SelectionLinkedSessionRingComponent
from .transport_component import TransportComponent
NUM_TRACKS = 8
GOODBYE_MESSAGE = (
 midi.CC_STATUS + MIDI_CHANNEL, 2, 0)

def tracks_to_use_from_song(song):
    return tuple(song.visible_tracks) + tuple(song.return_tracks) + (song.master_track,)


class KompleteKontrolBase(SimpleControlSurface):
    mixer_component_class = MixerComponent
    channel_strip_component_class = ChannelStripComponent
    is_s_mk2 = False

    def __init__(self, *a, **k):
        (super(KompleteKontrolBase, self).__init__)(*a, **k)
        with self.component_guard():
            self._create_controls()
            self._create_components()
            self._KompleteKontrolBase__on_main_view_changed.subject = self.application.view
        self._handshake_response_pending = False
        self._handshake_task = self._tasks.add(task.run(self._send_handshake))
        self._handshake_task.kill()

    def disconnect(self):
        self._auto_arm.set_enabled(False)
        self._send_midi(GOODBYE_MESSAGE)
        super(KompleteKontrolBase, self).disconnect()

    def port_settings_changed(self):
        self.set_components_enabled(False)
        self._handshake_task.restart()

    def _send_handshake(self):
        self._handshake_response_pending = True
        self._handshake_control.send_value(0, force=True)

    @listens('value')
    def _on_handshake_response(self, _):
        self._handshake_task.kill()
        if self._handshake_response_pending:
            self._handshake_response_pending = False
            self.set_components_enabled(True)
            self.refresh_state()

    def set_components_enabled(self, enabled):
        with self.component_guard():
            for c in self._components:
                c.set_enabled(enabled)

    def _create_controls(self):
        self._play_button = MultiElement(create_button(16, 'Play_Button'), create_button(17, 'Play_Button_With_Shift'))
        self._record_button = create_button(18, 'Record_Button')
        self._count_in_button = create_button(19, 'Count_In_Button')
        self._stop_button = create_button(20, 'Stop_Button')
        self._clear_button = create_button(21, 'Clear_Button')
        self._loop_button = create_button(22, 'Loop_Button')
        self._metronome_button = create_button(23, 'Metronome_Button')
        self._tap_tempo_button = create_button(24, 'Tap_Tempo_Button')
        self._undo_button = create_button(32, 'Undo_Button')
        self._redo_button = create_button(33, 'Redo_Button')
        self._quantize_button = create_button(34, 'Quantize_Button')
        self._automation_button = create_button(35, 'Automation_Button')
        self._clip_launch_button = create_button(96, 'Clip_Launch_Button')
        self._track_stop_button = create_button(97, 'Track_Stop_Button')
        self._jump_encoder = create_encoder(52, 'Jump_Encoder')
        self._loop_encoder = create_encoder(53, 'Loop_Encoder')
        self._volume_encoders = ButtonMatrixElement(rows=[
         [create_encoder((index + 80), ('Volume_Encoder_{}'.format(index)), is_s_mk2=(self.is_s_mk2)) for index in range(NUM_TRACKS)]],
          name='Volume_Encoders')
        self._pan_encoders = ButtonMatrixElement(rows=[
         [create_encoder((index + 88), ('Pan_Encoder_{}'.format(index)), is_s_mk2=(self.is_s_mk2)) for index in range(NUM_TRACKS)]],
          name='Pan_Encoders')
        self._track_name_displays = ButtonMatrixElement(rows=[
         [create_display_line((sysex.TRACK_NAME_DISPLAY_HEADER), index, ('Track_Name_Display_{}'.format(index)), width=(33 if self.is_s_mk2 else 11)) for index in range(NUM_TRACKS)]],
          name='Track_Name_Displays')
        self._track_volume_displays = ButtonMatrixElement(rows=[
         [create_display_line((sysex.TRACK_VOLUME_DISPLAY_HEADER), index, ('Track_Volume_Display_{}'.format(index)), width=12) for index in range(NUM_TRACKS)]],
          name='Track_Volume_Displays')
        self._track_panning_displays = ButtonMatrixElement(rows=[
         [create_display_line((sysex.TRACK_PANNING_DISPLAY_HEADER), index, ('Track_Panning_Display_{}'.format(index)), width=12) for index in range(NUM_TRACKS)]],
          name='Track_Panning_Displays')
        self._track_type_displays = ButtonMatrixElement(rows=[
         [create_sysex_element(sysex.TRACK_TYPE_DISPLAY_HEADER, index, 'Track_Type_Display_{}'.format(index)) for index in range(NUM_TRACKS)]],
          name='Track_Type_Displays')
        self._track_mute_displays = ButtonMatrixElement(rows=[
         [create_sysex_element(sysex.TRACK_MUTE_DISPLAY_HEADER, index, 'Track_Mute_Display_{}'.format(index)) for index in range(NUM_TRACKS)]],
          name='Track_Mute_Displays')
        self._track_solo_displays = ButtonMatrixElement(rows=[
         [create_sysex_element(sysex.TRACK_SOLO_DISPLAY_HEADER, index, 'Track_Solo_Display_{}'.format(index)) for index in range(NUM_TRACKS)]],
          name='Track_Solo_Displays')
        self._track_muted_via_solo_displays = ButtonMatrixElement(rows=[
         [create_sysex_element(sysex.TRACK_MUTED_VIA_SOLO_DISPLAY_HEADER, index, 'Track_Muted_via_Solo_Display_{}'.format(index)) for index in range(NUM_TRACKS)]],
          name='Track_Muted_via_Solo_Displays')
        self._track_selection_displays = ButtonMatrixElement(rows=[
         [create_sysex_element(sysex.TRACK_SELECT_DISPLAY_HEADER, index, 'Track_Selection_Display_{}'.format(index)) for index in range(NUM_TRACKS)]],
          name='Track_Selection_Displays')
        self._focus_follow_control = SysexElement((lambda value: sysex.TRACK_CHANGED_DISPLAY_HEADER + value + (midi.SYSEX_END,)
),
          name='Focus_Follow_Control')
        self._handshake_control = create_button(1, 'Handshake_Control')
        self._handshake_control.reset = nop
        self._on_handshake_response.subject = self._handshake_control

    def _create_components(self):
        self._create_mixer()
        self._create_transport()
        self._create_session_recording()
        self._create_undo_redo()
        self._create_clip_launch()
        self._create_clip_launch_background()
        self._create_detail_clip()
        self._create_focus_follow()
        self._create_auto_arm()
        self._create_view_based_modes()

    def _create_mixer(self):
        self._session_ring = SelectionLinkedSessionRingComponent(name='Session_Ring',
          num_tracks=NUM_TRACKS,
          tracks_to_use=(partial(tracks_to_use_from_song, self.song)),
          always_snap_track_offset=True)
        self._mixer = self.mixer_component_class(name='Mixer',
          tracks_provider=(self._session_ring),
          track_assigner=(SimpleTrackAssigner()),
          channel_strip_component_type=(self.channel_strip_component_class),
          is_enabled=False,
          layer=(self._create_mixer_component_layer()))

    def _create_mixer_component_layer(self):
        return Layer(volume_controls=(self._volume_encoders),
          pan_controls=(self._pan_encoders),
          track_name_displays=(self._track_name_displays),
          track_volume_displays=(self._track_volume_displays),
          track_panning_displays=(self._track_panning_displays),
          track_type_displays=(self._track_type_displays),
          track_selection_displays=(self._track_selection_displays),
          track_mute_displays=(self._track_mute_displays),
          track_solo_displays=(self._track_solo_displays),
          track_muted_via_solo_displays=(self._track_muted_via_solo_displays))

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(play_button=(self._play_button),
          stop_button=(self._stop_button),
          loop_button=(self._loop_button),
          metronome_button=(self._metronome_button),
          tap_tempo_button=(self._tap_tempo_button),
          jump_encoder=(self._jump_encoder),
          loop_start_encoder=(self._loop_encoder)))

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(name='Session_Recording',
          is_enabled=False,
          layer=Layer(automation_button=(self._automation_button)))

    def _create_undo_redo(self):
        self._undo_redo = UndoRedoComponent(name='Undo_Redo',
          is_enabled=False,
          layer=Layer(undo_button=(self._undo_button), redo_button=(self._redo_button)))

    def _create_clip_launch(self):
        self._clip_launch = ClipLaunchComponent(name='Clip_Launch',
          is_enabled=False,
          layer=Layer(clip_launch_button=(self._clip_launch_button),
          track_stop_button=(self._track_stop_button)))

    def _create_clip_launch_background(self):
        self._clip_launch_background = BackgroundComponent(name='Background',
          is_enabled=False,
          add_nop_listeners=True,
          layer=Layer(clip_launch_button=(self._clip_launch_button),
          track_stop_button=(self._track_stop_button),
          priority=(-1)))

    def _create_detail_clip(self):
        self._detail_clip = DetailClipComponent(name='Detail_Clip',
          is_enabled=False,
          layer=Layer(quantize_notes_button=(self._quantize_button),
          delete_notes_button=(self._clear_button)))

    def _create_focus_follow(self):
        self._focus_follow = FocusFollowComponent(name='Focus_Follow',
          is_enabled=False,
          layer=Layer(focus_follow_control=(self._focus_follow_control)))

    def _create_auto_arm(self):
        self._auto_arm = AutoArmComponent(name='Auto_Arm', is_enabled=False)

    def _create_view_based_modes(self):
        self._view_based_modes = ModesComponent(is_enabled=False)
        self._view_based_modes.add_mode('session', (
         EnablingMode(self._clip_launch),
         AddLayerMode(self._transport, Layer(session_record_button=(self._record_button),
           record_button=(self._count_in_button)))))
        self._view_based_modes.add_mode('arrange', AddLayerMode(self._transport, Layer(record_button=(self._record_button),
          session_record_button=(self._count_in_button))))
        self._KompleteKontrolBase__on_main_view_changed()

    @listens('is_view_visible', 'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible('Session'):
            self._view_based_modes.selected_mode = 'session'
        else:
            self._view_based_modes.selected_mode = 'arrange'