# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/atom.py
# Compiled at: 2021-11-23 12:54:43
# Size of source mod 2**32: 14688 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, inject, listens, liveobj_valid
from ableton.v2.control_surface import ControlSurface, Layer, PercussionInstrumentFinder
from ableton.v2.control_surface.components import ArmedTargetTrackComponent, BackgroundComponent, SessionNavigationComponent, SessionOverviewComponent, SessionRecordingComponent, SessionRingComponent, SimpleTrackAssigner, TransportComponent, UndoRedoComponent
from ableton.v2.control_surface.mode import AddLayerMode, LayerMode, ModesComponent, MomentaryBehaviour
from . import midi
from .channel_strip import ChannelStripComponent
from .drum_group import DrumGroupComponent
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .keyboard import KeyboardComponent
from .lighting import LightingComponent
from .mixer import MixerComponent
from .session import SessionComponent
from .skin import skin
from .translating_background import TranslatingBackgroundComponent
from .view_toggle import ViewToggleComponent

class ATOM(ControlSurface):

    def __init__(self, *a, **k):
        (super(ATOM, self).__init__)(*a, **k)
        with self.component_guard():
            with inject(skin=(const(skin))).everywhere():
                self._elements = Elements()
        with self.component_guard():
            with inject(element_container=(const(self._elements))).everywhere():
                self._create_lighting()
                self._create_transport()
                self._create_record_modes()
                self._create_undo()
                self._create_view_toggle()
                self._create_background()
                self._create_session()
                self._create_mixer()
                self._create_encoder_modes()
                self._create_session_navigation_modes()
                self._create_keyboard()
                self._create_drum_group()
                self._create_note_modes()
                self._create_pad_modes()
                self._create_user_assignments_mode()
                self._target_track = ArmedTargetTrackComponent(name='Target_Track')
                self._ATOM__on_target_track_changed.subject = self._target_track
                self._ATOM__on_native_mode_reply.subject = self._elements.native_mode_reply_element
        self._drum_group_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=(self._target_track.target_track)))
        self._ATOM__on_drum_group_changed.subject = self._drum_group_finder
        self._ATOM__on_drum_group_changed()
        self._ATOM__on_main_view_changed.subject = self.application.view

    def disconnect(self):
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)
        super(ATOM, self).disconnect()

    def port_settings_changed(self):
        self._session_ring.set_enabled(False)
        self._send_midi(midi.NATIVE_MODE_ON_MESSAGE)
        super(ATOM, self).port_settings_changed()

    def _create_lighting(self):
        self._lighting = LightingComponent(name='Lighting',
          is_enabled=False,
          layer=Layer(shift_button='shift_button', zoom_button='zoom_button'))
        self._lighting.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(play_button='play_button',
          loop_button='play_button_with_shift',
          stop_button='stop_button',
          metronome_button='click_button'))
        self._transport.set_enabled(True)

    def _create_record_modes(self):
        self._session_record = SessionRecordingComponent(name='Session_Record',
          is_enabled=False,
          layer=Layer(record_button='record_button'))
        self._record_modes = ModesComponent(name='Record_Modes')
        self._record_modes.add_mode('session', self._session_record)
        self._record_modes.add_mode('arrange', AddLayerMode((self._transport), layer=Layer(record_button='record_button')))
        self._ATOM__on_main_view_changed()

    def _create_undo(self):
        self._undo = UndoRedoComponent(name='Undo',
          is_enabled=False,
          layer=Layer(undo_button='stop_button_with_shift'))
        self._undo.set_enabled(True)

    def _create_view_toggle(self):
        self._view_toggle = ViewToggleComponent(name='View_Toggle',
          is_enabled=False,
          layer=Layer(detail_view_toggle_button='show_hide_button',
          main_view_toggle_button='preset_button'))
        self._view_toggle.set_enabled(True)

    def _create_background(self):
        self._background = BackgroundComponent(name='Background',
          is_enabled=False,
          add_nop_listeners=True,
          layer=Layer(set_loop_button='set_loop_button',
          nudge_button='nudge_button',
          bank_button='bank_button'))
        self._background.set_enabled(True)

    def _create_session(self):
        self._session_ring = SessionRingComponent(name='Session_Ring',
          is_enabled=False,
          num_tracks=SESSION_WIDTH,
          num_scenes=SESSION_HEIGHT)
        self._session = SessionComponent(name='Session', session_ring=(self._session_ring))
        self._session_navigation = SessionNavigationComponent(name='Session_Navigation',
          is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(left_button='left_button', right_button='right_button'))
        self._session_navigation.set_enabled(True)
        self._session_overview = SessionOverviewComponent(name='Session_Overview',
          is_enabled=False,
          session_ring=(self._session_ring),
          enable_skinning=True,
          layer=Layer(button_matrix='pads_with_zoom'))

    def _create_mixer(self):
        self._mixer = MixerComponent(name='Mixer',
          auto_name=True,
          tracks_provider=(self._session_ring),
          track_assigner=(SimpleTrackAssigner()),
          invert_mute_feedback=True,
          channel_strip_component_type=ChannelStripComponent)

    def _create_encoder_modes(self):
        self._encoder_modes = ModesComponent(name='Encoder_Modes', enable_skinning=True)
        self._encoder_modes.add_mode('volume', AddLayerMode(self._mixer, Layer(volume_controls='encoders')))
        self._encoder_modes.add_mode('pan', AddLayerMode(self._mixer, Layer(pan_controls='encoders')))
        self._encoder_modes.add_mode('send_a', AddLayerMode(self._mixer, Layer(send_a_controls='encoders')))
        self._encoder_modes.add_mode('send_b', AddLayerMode(self._mixer, Layer(send_b_controls='encoders')))
        self._encoder_modes.selected_mode = 'volume'

    def _create_session_navigation_modes(self):
        self._session_navigation_modes = ModesComponent(name='Session_Navigation_Modes',
          is_enabled=False,
          layer=Layer(cycle_mode_button='bank_button'))
        self._session_navigation_modes.add_mode('default',
          AddLayerMode((self._session_navigation),
          layer=Layer(up_button='up_button', down_button='down_button')),
          cycle_mode_button_color='DefaultButton.Off')
        self._session_navigation_modes.add_mode('paged',
          AddLayerMode((self._session_navigation),
          layer=Layer(page_up_button='up_button',
          page_down_button='down_button',
          page_left_button='left_button',
          page_right_button='right_button')),
          cycle_mode_button_color='DefaultButton.On')
        self._session_navigation_modes.selected_mode = 'default'

    def _create_keyboard(self):
        self._keyboard = KeyboardComponent((midi.KEYBOARD_CHANNEL),
          name='Keyboard',
          is_enabled=False,
          layer=Layer(matrix='pads',
          scroll_up_button='up_button',
          scroll_down_button='down_button'))

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(name='Drum_Group',
          is_enabled=False,
          translation_channel=(midi.DRUM_CHANNEL),
          layer=Layer(matrix='pads',
          scroll_page_up_button='up_button',
          scroll_page_down_button='down_button'))

    def _create_note_modes(self):
        self._note_modes = ModesComponent(name='Note_Modes', is_enabled=False)
        self._note_modes.add_mode('keyboard', self._keyboard)
        self._note_modes.add_mode('drum', self._drum_group)
        self._note_modes.selected_mode = 'keyboard'

    def _create_pad_modes(self):
        self._pad_modes = ModesComponent(name='Pad_Modes',
          is_enabled=False,
          layer=Layer(session_button='full_level_button',
          note_button='note_repeat_button',
          channel_button='select_button',
          encoder_modes_button='setup_button'))
        self._pad_modes.add_mode('session', (
         AddLayerMode(self._background, Layer(unused_pads='pads_with_shift')),
         AddLayerMode(self._session, Layer(clip_launch_buttons='pads',
           scene_launch_buttons=(self._elements.pads_with_shift.submatrix[
          3:, :]))),
         self._session_overview,
         self._session_navigation_modes))
        self._pad_modes.add_mode('note', self._note_modes)
        self._pad_modes.add_mode('channel', (
         self._elements.pads.reset,
         AddLayerMode(self._mixer, Layer(arm_buttons=(self._elements.pads.submatrix[:, :1]),
           solo_buttons=(self._elements.pads.submatrix[:, 1:2]),
           track_select_buttons=(self._elements.pads.submatrix[:, 2:3]))),
         AddLayerMode(self._session, Layer(stop_track_clip_buttons=(self._elements.pads.submatrix[:, 3:]))),
         self._session_navigation_modes))
        self._pad_modes.add_mode('encoder_modes',
          (
         LayerMode(self._encoder_modes, Layer(volume_button=(self._elements.pads_raw[0][0]),
           pan_button=(self._elements.pads_raw[0][1]),
           send_a_button=(self._elements.pads_raw[0][2]),
           send_b_button=(self._elements.pads_raw[0][3]))),
         AddLayerMode(self._background, Layer(unused_pads=(self._elements.pads.submatrix[:, 1:])))),
          behaviour=(MomentaryBehaviour()))
        self._pad_modes.selected_mode = 'session'
        self._pad_modes.set_enabled(True)

    def _create_user_assignments_mode(self):
        self._translating_background = TranslatingBackgroundComponent((midi.USER_CHANNEL),
          name='Translating_Background',
          is_enabled=False,
          add_nop_listeners=True,
          layer=Layer(note_repeat_button='note_repeat_button',
          full_level_button='full_level_button',
          bank_button='bank_button',
          preset_button='preset_button',
          show_hide_button='show_hide_button',
          nudge_button='nudge_button',
          set_loop_button='set_loop_button',
          setup_button='setup_button',
          up_button='up_button',
          down_button='down_button',
          left_button='left_button',
          right_button='right_button',
          select_button='select_button',
          click_button='click_button',
          record_button='record_button',
          play_button='play_button',
          stop_button='stop_button',
          pads='pads',
          encoders='encoders'))
        self._top_level_modes = ModesComponent(name='Top_Level_Modes',
          is_enabled=False,
          support_momentary_mode_cycling=False,
          layer=Layer(cycle_mode_button='editor_button'))
        self._top_level_modes.add_mode('default',
          (self.refresh_state), cycle_mode_button_color='DefaultButton.Off')
        self._top_level_modes.add_mode('user',
          (self._translating_background),
          cycle_mode_button_color='DefaultButton.On')
        self._top_level_modes.selected_mode = 'default'
        self._top_level_modes.set_enabled(True)

    @listens('is_view_visible', 'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible('Session'):
            self._record_modes.selected_mode = 'session'
        else:
            self._record_modes.selected_mode = 'arrange'

    @listens('target_track')
    def __on_target_track_changed(self):
        self._drum_group_finder.device_parent = self._target_track.target_track

    @listens('instrument')
    def __on_drum_group_changed(self):
        drum_group = self._drum_group_finder.drum_group
        self._drum_group.set_drum_group_device(drum_group)
        self._note_modes.selected_mode = 'drum' if liveobj_valid(drum_group) else 'keyboard'

    @listens('value')
    def __on_native_mode_reply(self, _):
        self._session_ring.set_enabled(True)