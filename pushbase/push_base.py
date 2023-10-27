# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\push_base.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 78483 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from past.utils import old_div
from contextlib import contextmanager
from functools import partial
from ableton.v2.base import NamedTuple, clamp, const, inject, listens, listens_group, liveobj_valid, nop
from ableton.v2.control_surface import BackgroundLayer, BankingInfo, ClipCreator, ControlSurface, DeviceBankRegistry, Layer, PercussionInstrumentFinder, midi
from ableton.v2.control_surface.components import BackgroundComponent, ModifierBackgroundComponent, SessionNavigationComponent, SessionOverviewComponent, SessionRingComponent, ViewControlComponent
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ChoosingElement, ComboElement, DoublePressContext, MultiElement, OptionalElement, to_midi_value
from ableton.v2.control_surface.mode import AddLayerMode, LayerMode, LazyEnablingMode, ModesComponent, ReenterBehaviour
from . import consts, sysex
from .actions import CaptureAndInsertSceneComponent, DeleteAndReturnToDefaultComponent, DeleteComponent, DeleteSelectedClipComponent, DeleteSelectedSceneComponent, DuplicateDetailClipComponent, DuplicateLoopComponent, UndoRedoComponent
from .auto_arm_component import RestoringAutoArmComponent
from .clip_control_component import ClipControlComponent
from .device_parameter_component import DeviceParameterComponent
from .fixed_length import DEFAULT_LENGTH_OPTION_INDEX, FixedLengthComponent, FixedLengthSetting
from .grid_resolution import GridResolution
from .instrument_component import NoteLayout, SelectedNotesInstrumentComponent
from .loop_selector_component import LoopSelectorComponent
from .matrix_maps import FEEDBACK_CHANNELS
from .melodic_component import MelodicComponent
from .message_box_component import DialogComponent, InfoComponent
from .messenger_mode_component import MessengerModesComponent
from .note_editor_component import DEFAULT_VELOCITY_RANGE_THRESHOLDS, get_all_notes, remove_all_notes
from .note_layout_switcher import NoteLayoutSwitcher
from .note_repeat_component import NoteRepeatEnabler
from .note_settings_component import NoteEditorSettingsComponent
from .select_playing_clip_component import SelectPlayingClipComponent
from .selection import PushSelection
from .session_recording_component import FixedLengthRecording, FixedLengthSessionRecordingComponent
from .skin_default import make_default_skin
from .step_seq_component import DrumStepSeqComponent, StepSeqComponent
from .touch_strip_controller import TouchStripControllerComponent, TouchStripEncoderConnection, TouchStripPitchModComponent
from .track_frozen_mode import TrackFrozenModesComponent
from .transport_component import TransportComponent
from .value_component import ParameterValueComponent, ValueComponent
from .velocity_levels_component import VelocityLevelsComponent
NUM_TRACKS = 8
NUM_SCENES = 8
TEMPO_SWING_TOUCH_DELAY = 0.4

def tracks_to_use_from_song(song):
    return tuple(song.visible_tracks) + tuple(song.return_tracks)


class PushBase(ControlSurface):
    preferences_key = 'Push'
    drum_group_note_editor_skin = 'NoteEditor'
    slicing_note_editor_skin = 'NoteEditor'
    drum_group_velocity_levels_skin = 'VelocityLevels'
    slicing_velocity_levels_skin = 'VelocityLevels'
    note_layout_button = 'note_mode_button'
    note_editor_velocity_range_thresholds = DEFAULT_VELOCITY_RANGE_THRESHOLDS
    device_component_class = None
    selected_track_parameter_provider_class = None
    bank_definitions = None
    note_editor_class = None
    sliced_simpler_class = None

    def __init__(self, *a, **k):
        (super(PushBase, self).__init__)(*a, **k)
        self.register_slot(self.song.view, self._on_selected_track_changed, 'selected_track')
        self._device_decorator_factory = self._create_device_decorator_factory()
        self.register_disconnectable(self._device_decorator_factory)
        self._percussion_instrument_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=(self.song.view.selected_track)))
        self._double_press_context = DoublePressContext()
        injecting = self._create_injector()
        self._push_injector = injecting.everywhere()
        self._element_injector = inject(element_container=(const(None))).everywhere()
        with self.component_guard():
            self._suppress_sysex = False
            self._skin = self._create_skin()
            self._clip_creator = ClipCreator()
            self._note_editor_settings = []
            self._notification = None
            self._user = None
            with inject(skin=(const(self._skin))).everywhere():
                self._create_controls()
        self._element_injector = inject(element_container=(const(self.elements))).everywhere()
        self._save_note_modes = False

    def initialize(self):
        self._setup_accidental_touch_prevention()
        self._create_components()
        self._init_main_modes()
        self._on_selected_track_changed()
        self._PushBase__on_session_record_changed.subject = self.song
        self._PushBase__on_session_record_changed()
        self._PushBase__on_selected_track_is_frozen_changed.subject = self.song.view
        self.set_feedback_channels(FEEDBACK_CHANNELS)
        self._save_note_modes = True

    def disconnect(self):
        if self._user is not None:
            with self.component_guard():
                self._user.mode = sysex.USER_MODE
        super(PushBase, self).disconnect()

    @contextmanager
    def _component_guard(self):
        with super(PushBase, self)._component_guard():
            with self._push_injector:
                with self._element_injector:
                    song_view = self.song.view
                    old_selected_track = song_view.selected_track
                    yield
                    if song_view.selected_track != old_selected_track:
                        self._track_selection_changed_by_action()

    def _create_device_decorator_factory(self):
        raise NotImplementedError

    def _create_components(self):
        self._init_settings()
        self._init_notification()
        self._init_message_box()
        self._init_background()
        self._init_user()
        self._init_touch_strip_controller()
        self._init_track_frozen()
        self._init_undo_redo_actions()
        self._init_duplicate_actions()
        self._init_delete_actions()
        self._init_quantize_actions()
        self._init_session_ring()
        self._init_fixed_length()
        self._init_transport_and_recording()
        self._init_stop_clips_action()
        self._init_value_components()
        self._init_track_list()
        self._init_mixer()
        self._init_track_mixer()
        self._init_session()
        self._init_grid_resolution()
        self._init_drum_component()
        self._init_slicing_component()
        self._init_note_editor_settings_component()
        self._init_drum_step_sequencer()
        self._init_slicing_step_sequencer()
        self._init_instrument()
        self._init_split_melodic_sequencer()
        self._init_scales()
        self._init_note_repeat()
        self._init_matrix_modes()
        self._init_device()

    def _create_injector(self):
        return inject(double_press_context=(const(self._double_press_context)),
          expect_dialog=(const(self.expect_dialog)),
          show_notification=(const(self.show_notification)),
          selection=(lambda: PushSelection(application=(self.application),
          device_component=(self._device_component),
          navigation_component=(self._device_navigation))
))

    def _create_skin(self):
        return make_default_skin()

    def _needs_to_deactivate_session_recording(self):
        return self._matrix_modes.selected_mode == 'note' and self.song.exclusive_arm

    def _track_selection_changed_by_action(self):
        if self._needs_to_deactivate_session_recording():
            self._session_recording.deactivate_recording()
        if self._auto_arm.needs_restore_auto_arm:
            self._auto_arm.restore_auto_arm()

    def port_settings_changed(self):
        self._switch_to_live_mode()

    def _switch_to_live_mode(self):
        self._user.mode = sysex.LIVE_MODE
        self._user.force_send_mode()

    def _init_settings(self):
        self._settings = self._create_settings()

    def _create_settings(self):
        raise RuntimeError

    def update(self):
        self._PushBase__on_session_record_changed()
        self.recall_or_save_note_layout()
        self.reset_controlled_track()
        self.set_feedback_channels(FEEDBACK_CHANNELS)
        super(PushBase, self).update()

    def _create_controls(self):
        raise NotImplementedError

    def _with_shift(self, button):
        return ComboElement(button, modifier='shift_button')

    def _with_firmware_version(self, major_version, minor_version, control_element):
        raise NotImplementedError

    def _init_background(self):
        self._background = BackgroundComponent()
        self._background.layer = self._create_background_layer()
        self._matrix_background = BackgroundComponent()
        self._matrix_background.set_enabled(False)
        self._matrix_background.layer = Layer(matrix='matrix')
        self._mod_background = ModifierBackgroundComponent()
        self._mod_background.layer = Layer(shift_button='shift_button',
          select_button='select_button',
          delete_button='delete_button',
          duplicate_button='duplicate_button',
          quantize_button='quantize_button')
        self._param_control_background = BackgroundComponent(is_enabled=False,
          add_nop_listeners=True,
          layer=Layer(global_param_controls='global_param_controls',
          priority=(consts.BACKGROUND_PRIORITY)))
        self._param_control_background.set_enabled(True)

    def _create_background_layer(self):
        return Layer(top_buttons='select_buttons',
          bottom_buttons='track_state_buttons',
          scales_button='scale_presets_button',
          octave_up='octave_up_button',
          octave_down='octave_down_button',
          side_buttons='side_buttons',
          repeat_button='repeat_button',
          accent_button='accent_button',
          double_button='double_button',
          param_touch='global_param_touch_buttons',
          touch_strip='touch_strip_control',
          nav_up_button='nav_up_button',
          nav_down_button='nav_down_button',
          nav_left_button='nav_left_button',
          nav_right_button='nav_right_button',
          new_button='new_button',
          aftertouch='aftertouch_control',
          _notification=(self._notification.use_single_line(2)),
          priority=(consts.BACKGROUND_PRIORITY))

    def _init_track_list(self):
        pass

    def _can_auto_arm_track(self, track):
        routing = track.input_routing_type.display_name
        return routing == 'Ext: All Ins' or routing == 'All Ins' or routing.startswith(self.input_target_name_for_auto_arm)

    def _init_touch_strip_controller(self):
        strip_controller = TouchStripControllerComponent()
        strip_controller.set_enabled(False)
        strip_controller.layer = Layer(touch_strip='touch_strip_control')
        strip_controller.layer.priority = consts.DIALOG_PRIORITY
        self._strip_connection = TouchStripEncoderConnection(strip_controller, self.elements.touch_strip_tap)
        self.elements.tempo_control.set_observer(self._strip_connection)
        self.elements.swing_control.set_observer(self._strip_connection)
        self.elements.master_volume_control.set_observer(self._strip_connection)
        for encoder in self.elements.global_param_controls.nested_control_elements():
            encoder.set_observer(self._strip_connection)

        self._pitch_mod_touch_strip = TouchStripPitchModComponent()
        self._pitch_mod_touch_strip_layer = Layer(touch_strip='touch_strip_control',
          touch_strip_indication=(self._with_firmware_version(1, 16, ComboElement('touch_strip_control', modifier='select_button'))),
          touch_strip_toggle=(self._with_firmware_version(1, 16, ComboElement('touch_strip_tap', modifier='select_button'))))

    def _create_session_mode(self):
        raise NotImplementedError

    def _create_alternating_layout_modes_for_levels_and_loop(self, mode='drum', add_touch_strip=False, default_mode=None, alternative_mode=None):
        base_component = getattr(self, '_%s_component' % mode)
        base_layer = Layer(matrix=(self.elements.matrix.submatrix[:4, 4:8]), page_strip='touch_strip_control', scroll_strip=(self._with_shift('touch_strip_control')), accent_button='accent_button', full_velocity='full_velocity_element') if add_touch_strip else Layer(matrix=(self.elements.matrix.submatrix[:4, 4:8]))
        sequencer = getattr(self, '_%s_step_sequencer' % mode)
        velocity_levels = getattr(self, '_%s_velocity_levels' % mode)
        alternating_layouts = MessengerModesComponent(muted=True, is_enabled=False)
        alternating_layouts.add_mode('sequencer_loop',
          [
         sequencer,
         self._note_editor_settings_component,
         AddLayerMode(sequencer, Layer(loop_selector_matrix=(self.elements.double_press_matrix.submatrix[
          4:8, 4:8]),
           short_loop_selector_matrix=(self.elements.double_press_event_matrix.submatrix[
          4:8, 4:8]))),
         AddLayerMode(base_component, base_layer)],
          message=(consts.MessageBoxText.ALTERNATE_LOOP_SELECTOR),
          default_mode=default_mode,
          alternative_mode=alternative_mode)
        alternating_layouts.add_mode('sequencer_velocity_levels',
          [
         sequencer,
         self._note_editor_settings_component,
         velocity_levels,
         AddLayerMode(base_component, base_layer),
         AddLayerMode(velocity_levels, Layer(matrix=(self.elements.matrix.submatrix[4:8, 4:8])))],
          message=(consts.MessageBoxText.ALTERNATE_16_VELOCITIES),
          default_mode=default_mode,
          alternative_mode=alternative_mode)
        return alternating_layouts

    def _create_alternating_layout_modes_for_64pads(self, mode='drum', add_touch_strip=False, default_mode=None, alternative_mode=None):
        base_component = getattr(self, '_%s_component' % mode)
        touch_strip_modes = [LayerMode(self._pitch_mod_touch_strip, self._pitch_mod_touch_strip_layer)] if add_touch_strip else []
        loop_selector = LoopSelectorComponent(follow_detail_clip=True,
          clip_creator=(self._clip_creator),
          name=(mode.title() + '_Pad_Loop_Selector'),
          is_enabled=False,
          layer=Layer(loop_selector_matrix=(self.elements.double_press_matrix.submatrix[:, 0]),
          short_loop_selector_matrix=(self.elements.double_press_event_matrix.submatrix[:,
         0])),
          default_size=8)
        alternating_layouts = MessengerModesComponent(muted=True, is_enabled=False)
        alternating_layouts.add_mode('64pads',
          ([
         AddLayerMode(base_component, Layer(matrix='matrix'))] + touch_strip_modes),
          default_mode=default_mode,
          alternative_mode=alternative_mode)
        alternating_layouts.add_mode('56pads_loop',
          ([
         loop_selector,
         AddLayerMode(base_component, Layer(matrix=(self.elements.matrix.submatrix[:, 1:])))] + touch_strip_modes),
          message=(consts.MessageBoxText.ALTERNATE_56_PADS),
          default_mode=default_mode,
          alternative_mode=alternative_mode)
        alternating_layouts.selected_mode = '64pads'
        return alternating_layouts

    def _create_slicing_modes(self):
        layout_args = dict(mode='slicing', add_touch_strip=True)
        create_layouts_for_levels_and_loop = partial(
         (self._create_alternating_layout_modes_for_levels_and_loop), **layout_args)
        self._slicing_loop_modes = create_layouts_for_levels_and_loop(default_mode='sequencer_loop',
          alternative_mode='sequencer_velocity_levels')
        self._slicing_loop_modes.selected_mode = 'sequencer_loop'
        self._slicing_velocity_levels_modes = create_layouts_for_levels_and_loop(default_mode='sequencer_velocity_levels',
          alternative_mode='sequencer_loop')
        self._slicing_velocity_levels_modes.selected_mode = 'sequencer_velocity_levels'
        self._slicing_64pads_modes = (self._create_alternating_layout_modes_for_64pads)(default_mode='64pads', 
         alternative_mode='56pads_loop', **layout_args)
        slicing_modes = MessengerModesComponent(name='Slicing_Modes', is_enabled=False)
        slicing_modes.add_mode('64pads',
          (self._slicing_64pads_modes),
          message=(consts.MessageBoxText.LAYOUT_SLICING_64_PADS))
        self._register_matrix_mode('64pads',
          modes_component=(self._slicing_64pads_modes),
          parent_path=[
         'matrix_modes', 'note', 'slicing'])
        slicing_modes.add_mode('sequencer_loop',
          (self._slicing_loop_modes),
          message=(consts.MessageBoxText.LAYOUT_SLICING_LOOP))
        self._register_matrix_mode('sequencer_loop',
          modes_component=(self._slicing_64pads_modes),
          parent_path=[
         'matrix_modes', 'note', 'slicing'])
        slicing_modes.add_mode('sequencer_velocity_levels',
          (self._slicing_velocity_levels_modes),
          message=(consts.MessageBoxText.LAYOUT_SLICING_LEVELS))
        self._register_matrix_mode('sequencer_velocity_levels',
          modes_component=(self._slicing_64pads_modes),
          parent_path=[
         'matrix_modes', 'note', 'slicing'])
        slicing_modes.selected_mode = '64pads'
        return slicing_modes

    def _create_drum_modes(self):
        layout_args = dict(mode='drum', add_touch_strip=False)
        create_layouts_for_levels_and_loop = partial(
         (self._create_alternating_layout_modes_for_levels_and_loop), **layout_args)
        self._drum_loop_modes = create_layouts_for_levels_and_loop(default_mode='sequencer_loop',
          alternative_mode='sequencer_velocity_levels')
        self._drum_loop_modes.selected_mode = 'sequencer_loop'
        self._drum_velocity_levels_modes = create_layouts_for_levels_and_loop(default_mode='sequencer_velocity_levels',
          alternative_mode='sequencer_loop')
        self._drum_velocity_levels_modes.selected_mode = 'sequencer_velocity_levels'
        self._drum_64pads_modes = (self._create_alternating_layout_modes_for_64pads)(default_mode='64pads', 
         alternative_mode='56pads_loop', **layout_args)
        drum_modes = MessengerModesComponent(name='Drum_Modes', is_enabled=False)
        drum_modes.add_mode('sequencer_loop',
          (self._drum_loop_modes),
          message=(consts.MessageBoxText.LAYOUT_DRUMS_LOOP))
        self._register_matrix_mode('sequencer_loop',
          modes_component=(self._drum_loop_modes),
          parent_path=[
         'matrix_modes', 'note', 'drums'])
        drum_modes.add_mode('sequencer_velocity_levels',
          (self._drum_velocity_levels_modes),
          message=(consts.MessageBoxText.LAYOUT_DRUMS_LEVELS))
        self._register_matrix_mode('sequencer_velocity_levels',
          modes_component=(self._drum_loop_modes),
          parent_path=[
         'matrix_modes', 'note', 'drums'])
        drum_modes.add_mode('64pads',
          (self._drum_64pads_modes),
          message=(consts.MessageBoxText.LAYOUT_DRUMS_64_PADS))
        self._register_matrix_mode('64pads',
          modes_component=(self._drum_loop_modes),
          parent_path=[
         'matrix_modes', 'note', 'drums'])
        drum_modes.selected_mode = 'sequencer_loop'
        return drum_modes

    def _init_matrix_modes(self):
        self._auto_arm = RestoringAutoArmComponent(name='Auto_Arm')
        self._auto_arm.can_auto_arm_track = self._can_auto_arm_track
        self._auto_arm.layer = Layer(_notification=(self._notification.use_single_line(2)))
        self._select_playing_clip = SelectPlayingClipComponent(name='Select_Playing_Clip',
          playing_clip_above_layer=Layer(action_button='nav_up_button'),
          playing_clip_below_layer=Layer(action_button='nav_down_button'))
        self._select_playing_clip.layer = Layer(_notification=(self._notification.use_single_line(2)))
        self._drum_modes = self._create_drum_modes()
        self._slicing_modes = self._create_slicing_modes()
        self._note_modes = ModesComponent(name='Note_Modes')
        self._note_modes.add_mode('drums', [self._drum_component, self._note_repeat_enabler, self._drum_modes])
        self._register_matrix_mode('drums',
          modes_component=(self._drum_modes),
          parent_path=[
         'matrix_modes', 'note'])
        self._note_modes.add_mode('slicing', [
         self._slicing_component, self._note_repeat_enabler, self._slicing_modes])
        self._register_matrix_mode('slicing',
          modes_component=(self._slicing_modes),
          parent_path=[
         'matrix_modes', 'note'])
        self._note_modes.add_mode('looper', self._audio_loop if consts.PROTO_AUDIO_NOTE_MODE else self._matrix_background)
        self._note_modes.add_mode('instrument', [
         self._note_repeat_enabler, self._instrument, self._scales_enabler])
        self._register_matrix_mode('instrument',
          modes_component=(self._instrument),
          parent_path=[
         'matrix_modes', 'note'])
        self._note_modes.add_mode('disabled', self._matrix_background)
        self._register_matrix_mode('disabled', parent_path=['matrix_modes', 'note'])
        self._note_modes.selected_mode = 'disabled'
        self._note_modes.set_enabled(False)
        self._matrix_modes = ModesComponent(name='Matrix_Modes')
        self._register_matrix_mode('matrix_modes', self._matrix_modes)
        self._matrix_modes.add_mode('session', self._create_session_mode())
        self._register_matrix_mode('session', parent_path=['matrix_modes'])
        self._matrix_modes.add_mode('note',
          (self._create_note_mode()),
          behaviour=(self._auto_arm.auto_arm_restore_behaviour()))
        self._register_matrix_mode('note',
          modes_component=(self._note_modes), parent_path=['matrix_modes'])
        self._matrix_modes.selected_mode = 'note'
        self._matrix_modes.layer = Layer(session_button='session_mode_button',
          note_button='note_mode_button')
        self._PushBase__on_matrix_mode_changed.subject = self._matrix_modes
        self._matrix_modes.selected_mode = 'note'
        self._PushBase__on_percussion_instrument_changed.subject = self._percussion_instrument_finder
        self._PushBase__on_drums_note_layout_changed.subject = self._drum_modes
        self._PushBase__on_slicing_note_layout_changed.subject = self._slicing_modes

    def _register_matrix_mode(self, name, modes_component=None, parent_path=None):
        pass

    def _switch_note_mode_layout(self):
        cyclable_mode = {'instrument':self._instrument, 
         'drums':self._drum_modes, 
         'slicing':self._slicing_modes}.get(self._note_modes.selected_mode, None)
        getattr(cyclable_mode, 'cycle_mode', nop)()
        self._load_alternative_note_layout()

    def _get_current_alternative_layout_mode(self):
        note_mode = self._note_modes.selected_mode
        if note_mode == 'instrument':
            mode = {'play':self._instrument.play_modes,  'sequence':self._instrument.sequence_modes, 
             'split_melodic_sequencer':self._split_sequencer_mode}.get(self._instrument.selected_mode, None)
        else:
            if note_mode == 'drums':
                mode = {'64pads':self._drum_64pads_modes,  'sequencer_loop':self._drum_loop_modes, 
                 'sequencer_velocity_levels':self._drum_velocity_levels_modes}.get(self._drum_modes.selected_mode, None)
            else:
                if note_mode == 'slicing':
                    mode = {'64pads':self._slicing_64pads_modes,  'sequencer_loop':self._slicing_loop_modes, 
                     'sequencer_velocity_levels':self._slicing_velocity_levels_modes}.get(self._slicing_modes.selected_mode, None)
                else:
                    mode = None
        return mode

    def _create_note_mode(self):
        self._note_layout_switcher = NoteLayoutSwitcher(switch_note_mode_layout=(self._switch_note_mode_layout),
          get_current_alternative_layout_mode=(self._get_current_alternative_layout_mode),
          is_enabled=False,
          layer=Layer(cycle_button=(self.note_layout_button),
          lock_button=(self._with_shift(self.note_layout_button))))
        return [
         self._view_control,
         self._note_modes,
         self._delete_clip,
         self._select_playing_clip,
         self._note_layout_switcher]

    def _create_user_component(self):
        raise NotImplementedError

    def _init_user(self):
        self._user = self._create_user_component()
        self._PushBase__on_hardware_mode_changed.subject = self._user
        self._PushBase__on_before_hardware_mode_sent.subject = self._user
        self._PushBase__on_after_hardware_mode_sent.subject = self._user

    def _create_session_layer(self):
        return Layer(clip_launch_buttons='matrix',
          scene_launch_buttons='side_buttons',
          duplicate_button='duplicate_button',
          touch_strip='touch_strip_control')

    def _set_session_skin(self, session):
        pass

    def _create_fixed_length_recording(self):
        return self.register_disconnectable(FixedLengthRecording((self.song),
          (self._clip_creator),
          fixed_length_setting=(self._fixed_length_setting)))

    def _instantiate_session(self):
        raise NotImplementedError

    def _create_session(self):
        session = self._instantiate_session()
        self._set_session_skin(session)
        for scene_index in range(8):
            scene = session.scene(scene_index)
            scene.layer = Layer(select_button='select_button',
              delete_button='delete_button')
            scene._do_select_scene = self.on_select_scene
            for track_index in range(8):
                clip_slot = scene.clip_slot(track_index)
                clip_slot._do_select_clip = self.on_select_clip_slot
                clip_slot.layer = Layer(delete_button='delete_button',
                  select_button='select_button',
                  duplicate_button='duplicate_button')

        session.duplicate_layer = Layer(scene_buttons='side_buttons')
        return session

    def on_select_clip_slot(self, clip_slot):
        pass

    def on_select_scene(self, scene):
        pass

    def on_select_track(self, track):
        pass

    def _create_session_overview(self):
        return SessionOverviewComponent(session_ring=(self._session_ring),
          name='Session_Overview',
          enable_skinning=True,
          is_enabled=False,
          layer=(self._create_session_overview_layer()))

    def _create_session_overview_layer(self):
        raise NotImplementedError

    def _init_session_ring(self):
        self._session_ring = SessionRingComponent(num_tracks=NUM_TRACKS,
          num_scenes=NUM_SCENES,
          tracks_to_use=(partial(tracks_to_use_from_song, self.song)),
          is_enabled=True)

    def _init_session(self):
        self._session_mode = LazyEnablingMode(self._create_session)
        self._session_overview_mode = LazyEnablingMode(self._create_session_overview)
        self._session_navigation = SessionNavigationComponent(session_ring=(self._session_ring),
          is_enabled=False,
          layer=(self._create_session_navigation_layer()))

    def _create_session_navigation_layer(self):
        return Layer(left_button='nav_left_button',
          right_button='nav_right_button',
          up_button='nav_up_button',
          down_button='nav_down_button',
          page_left_button=(self._with_shift('nav_left_button')),
          page_right_button=(self._with_shift('nav_right_button')),
          page_up_button=(MultiElement('octave_up_button', self._with_shift('nav_up_button'))),
          page_down_button=(MultiElement('octave_down_button', self._with_shift('nav_down_button'))))

    def _create_track_modes_layer(self):
        return Layer(stop_button='global_track_stop_button',
          mute_button='global_mute_button',
          solo_button='global_solo_button')

    def _when_track_is_not_frozen(self, *modes):
        return TrackFrozenModesComponent(default_mode=[
         modes],
          frozen_mode=(self._track_frozen_info),
          is_enabled=False)

    def _create_device_mode(self):
        raise NotImplementedError

    def _create_main_mixer_modes(self):
        raise NotImplementedError

    def _create_clip_mode(self):
        return [
         self._when_track_is_not_frozen(partial(self._view_control.show_view, 'Detail/Clip'), LazyEnablingMode(self._create_clip_control))]

    def _init_main_modes(self):

        def configure_note_editor_settings(parameter_provider, mode):
            for note_editor_setting in self._note_editor_settings:
                note_editor_setting.component.parameter_provider = parameter_provider
                note_editor_setting.component.automation_layer = getattr(note_editor_setting, mode + '_automation_layer')

        self._track_note_editor_mode = partial(configure_note_editor_settings, self._track_parameter_provider, 'track')
        self._device_note_editor_mode = partial(configure_note_editor_settings, self._device_component, 'device')
        self._enable_stop_mute_solo_as_modifiers = AddLayerMode(self._mod_background, Layer(stop='global_track_stop_button',
          mute='global_mute_button',
          solo='global_solo_button'))
        self._main_modes = ModesComponent()
        self._create_main_mixer_modes()
        self._main_modes.add_mode('clip', self._create_clip_mode())
        self._main_modes.add_mode('device',
          (self._create_device_mode()),
          behaviour=(ReenterBehaviour(self._device_navigation.back_to_top)))
        self._init_browse_mode()
        self._main_modes.selected_mode = 'device'
        self._main_modes.layer = self._create_main_modes_layer()
        self._PushBase__on_main_modes_changed.subject = self._main_modes
        self._PushBase__on_main_modes_changed(self._main_modes.selected_mode)

    def _init_browse_mode(self):
        raise NotImplementedError

    def _create_main_modes_layer(self):
        return Layer(volumes_button='vol_mix_mode_button',
          pan_sends_button='pan_send_mix_mode_button',
          track_button='single_track_mix_mode_button',
          clip_button='clip_mode_button',
          device_button='device_mode_button',
          browse_button='browse_mode_button',
          add_effect_right_button='create_device_button',
          add_effect_left_button=(self._with_shift('create_device_button')),
          add_instrument_track_button='create_track_button')

    def _init_track_frozen(self):
        self._track_frozen_info = InfoComponent(info_text=(consts.MessageBoxText.TRACK_FROZEN_INFO),
          is_enabled=False,
          layer=(self._create_track_frozen_layer()))

    def _create_track_frozen_layer(self):
        return Layer()

    def _init_mixer(self):
        pass

    def _init_track_mixer(self):
        self._track_parameter_provider = self.register_disconnectable(self.selected_track_parameter_provider_class())
        self._track_mixer = DeviceParameterComponent(parameter_provider=(self._track_parameter_provider),
          is_enabled=False,
          layer=(self._create_track_mixer_layer()))

    def _create_track_mixer_layer(self):
        return Layer(parameter_controls='fine_grain_param_controls')

    def _create_device_component(self):
        return self.device_component_class(device_decorator_factory=(self._device_decorator_factory),
          device_bank_registry=(self._device_bank_registry),
          banking_info=(self._banking_info),
          name='DeviceComponent',
          is_enabled=True)

    def _create_device_parameter_component(self):
        return DeviceParameterComponent(parameter_provider=(self._device_component),
          is_enabled=False,
          layer=(self._create_device_parameter_layer()))

    def _create_device_parameter_layer(self):
        return Layer(parameter_controls='fine_grain_param_controls')

    def _create_device_navigation(self):
        raise NotImplementedError

    def _init_device(self):
        self._device_bank_registry = DeviceBankRegistry()
        self._banking_info = BankingInfo(self.bank_definitions)
        self._device_component = self._create_device_component()
        self._device_parameter_component = self._create_device_parameter_component()
        self._device_navigation = self._create_device_navigation()

    def _create_view_control_component(self):
        return ViewControlComponent(name='View_Control')

    def _init_fixed_length(self):
        self._fixed_length_setting = FixedLengthSetting()
        self._fixed_length_setting.enabled = self.preferences.setdefault('fixed_length_enabled', False)
        self._fixed_length_setting.selected_index = self.preferences.setdefault('fixed_length_option', DEFAULT_LENGTH_OPTION_INDEX)
        self._fixed_length_setting.legato_launch = self.preferences.setdefault('fixed_length_legato_launch', False)
        self._PushBase__on_fixed_length_enabled_changed.subject = self._fixed_length_setting
        self._PushBase__on_fixed_length_selected_index_changed.subject = self._fixed_length_setting
        self._PushBase__on_fixed_length_legato_launch_changed.subject = self._fixed_length_setting
        self._fixed_length = FixedLengthComponent(fixed_length_setting=(self._fixed_length_setting))
        self._fixed_length.layer = Layer(fixed_length_toggle_button='fixed_length_button')
        length, _ = self._fixed_length_setting.get_selected_length(self.song)
        self._clip_creator.fixed_length = length

    def _create_session_recording(self):
        return FixedLengthSessionRecordingComponent(fixed_length_setting=(self._fixed_length_setting),
          clip_creator=(self._clip_creator),
          view_controller=(self._view_control),
          name='Session_Recording')

    @listens('focused_document_view')
    def __on_session_visible_changed(self):
        is_showing_session = self.application.view.focused_document_view == 'Session'
        self._session_recording.layer = self._session_recording_session_layer if is_showing_session else self._session_recording_arrangement_layer
        self._view_control.layer = self._view_control_session_layer if is_showing_session else self._view_control_arrangement_layer
        self._session_recording.footswitch_toggles_arrangement_recording = not is_showing_session

    def _init_transport_and_recording(self):
        self._view_control = self._create_view_control_component()
        self._view_control.set_enabled(False)
        self._view_control_arrangement_layer = Layer(prev_track_button='nav_left_button',
          next_track_button='nav_right_button')
        self._view_control_session_layer = Layer(prev_scene_button=(OptionalElement('nav_up_button', self._settings['workflow'], False)),
          next_scene_button=(OptionalElement('nav_down_button', self._settings['workflow'], False)),
          prev_scene_list_button=(OptionalElement('nav_up_button', self._settings['workflow'], True)),
          next_scene_list_button=(OptionalElement('nav_down_button', self._settings['workflow'], True))) + self._view_control_arrangement_layer
        self._session_recording = self._create_session_recording()
        new_button = MultiElement(self.elements.new_button, self.elements.foot_pedal_button.double_press)
        session_recording_base_layer = Layer(automation_button='automation_button',
          new_scene_button=(self._with_shift('new_button')),
          re_enable_automation_button=(self._with_shift('automation_button')),
          delete_automation_button=(ComboElement('automation_button', 'delete_button')),
          foot_switch_button=(self.elements.foot_pedal_button.single_press),
          capture_midi_button=ComboElement('new_button', modifier='record_button'),
          _uses_foot_pedal='foot_pedal_button')
        self._session_recording_arrangement_layer = Layer(record_button=(self._with_shift('record_button')),
          arrangement_record_button='record_button') + session_recording_base_layer
        self._session_recording_session_layer = Layer(record_button='record_button',
          arrangement_record_button=(self._with_shift('record_button')),
          new_button=(OptionalElement(new_button, self._settings['workflow'], False)),
          scene_list_new_button=(OptionalElement(new_button, self._settings['workflow'], True))) + session_recording_base_layer
        self._PushBase__on_session_visible_changed.subject = self.application.view
        self._PushBase__on_session_visible_changed()
        self._transport = TransportComponent(name='Transport')
        self._transport.layer = Layer(play_button='play_button',
          stop_button=(self._with_shift('play_button')),
          tap_tempo_button='tap_tempo_button',
          metronome_button='metronome_button')

    def _create_clip_control(self):
        return ClipControlComponent(loop_layer=(self._create_clip_loop_layer()),
          audio_layer=(self._create_clip_audio_layer()),
          clip_name_layer=(self._create_clip_name_layer()),
          name='Clip_Control',
          is_enabled=False)

    def _create_clip_loop_layer(self):
        return Layer(encoders=(self.elements.global_param_controls.submatrix[:4, :]),
          shift_button='shift_button')

    def _create_clip_audio_layer(self):
        return Layer(warp_mode_encoder='parameter_controls_raw[4]',
          transpose_encoder='parameter_controls_raw[5]',
          detune_encoder='parameter_controls_raw[6]',
          gain_encoder='parameter_controls_raw[7]',
          shift_button='shift_button')

    def _create_clip_name_layer(self):
        return Layer()

    def _init_grid_resolution(self):
        self._grid_resolution = self.register_disconnectable(GridResolution())

    def _init_note_editor_settings_component(self):
        self._note_editor_settings_component = NoteEditorSettingsComponent(note_settings_component_class=(self.note_settings_component_class),
          automation_component_class=(self.automation_component_class),
          grid_resolution=(self._grid_resolution),
          initial_encoder_layer=Layer(initial_encoders='global_param_controls',
          priority=(consts.MOMENTARY_DIALOG_PRIORITY)),
          encoder_layer=Layer(encoders='global_param_controls',
          priority=(consts.MOMENTARY_DIALOG_PRIORITY)))
        self._note_editor_settings_component.settings.layer = self._create_note_settings_component_layer()
        self._note_editor_settings_component.mode_selector_layer = self._create_note_editor_mode_selector_layer()
        self._note_editor_settings.append(NamedTuple(component=(self._note_editor_settings_component),
          track_automation_layer=(self._create_note_editor_track_automation_layer()),
          device_automation_layer=(self._create_note_editor_track_automation_layer())))

    def _automateable_main_modes(self):
        return ('device', 'volumes', 'pan_sends', 'track')

    @listens('selected_mode')
    def __on_main_modes_changed(self, mode):
        editor_setting = None
        if mode == 'clip':
            editor_setting = 'note_settings'
        else:
            if mode in self._automateable_main_modes():
                editor_setting = 'automation'
        self._note_editor_settings_component.selected_setting = editor_setting
        self._note_editor_settings_component.update_view_state_based_on_selected_setting(editor_setting)

    def _create_note_editor_mode_selector_layer(self):
        return Layer(select_buttons='select_buttons',
          state_buttons='track_state_buttons',
          priority=(consts.MOMENTARY_DIALOG_PRIORITY))

    def _create_note_settings_component_layer(self):
        raise NotImplementedError

    def _create_note_editor_track_automation_layer(self):
        return Layer(priority=(consts.MOMENTARY_DIALOG_PRIORITY))

    def _create_note_editor_device_automation_layer(self):
        return Layer(priority=(consts.MOMENTARY_DIALOG_PRIORITY))

    def _create_sequence_instrument_layer(self):
        return Layer(accent_button='accent_button',
          full_velocity='full_velocity_element',
          playhead='playhead_element',
          mute_button='global_mute_button',
          quantization_buttons='side_buttons',
          note_editor_matrices=(ButtonMatrixElement([
         [self.elements.matrix.submatrix[:, 7 - row] for row in range(8)]])),
          duplicate_button='duplicate_button',
          delete_button='delete_button')

    def _create_sequence_instrument_layer_with_loop(self):
        return Layer(playhead='playhead_element',
          mute_button='global_mute_button',
          quantization_buttons='side_buttons',
          loop_selector_matrix=(self.elements.double_press_matrix.submatrix[:, 0]),
          short_loop_selector_matrix=(self.elements.double_press_event_matrix.submatrix[:,
         0]),
          note_editor_matrices=(ButtonMatrixElement([
         [self.elements.matrix.submatrix[:, 7 - row] for row in range(7)]])),
          duplicate_button='duplicate_button',
          delete_button='delete_button')

    def _create_play_instrument_with_loop_layer(self):
        return Layer(playhead='playhead_element',
          mute_button='global_mute_button',
          quantization_buttons='side_buttons',
          loop_selector_matrix=(self.elements.double_press_matrix.submatrix[:, 0]),
          short_loop_selector_matrix=(self.elements.double_press_event_matrix.submatrix[:,
         0]),
          duplicate_button='duplicate_button',
          delete_button='delete_button')

    def _init_instrument(self):
        self._note_layout = self.register_disconnectable(NoteLayout(song=(self.song), preferences=(self.preferences)))
        instrument_basic_layer = Layer(accent_button='accent_button',
          full_velocity='full_velocity_element',
          octave_strip=(self._with_shift('touch_strip_control')),
          octave_up_button='octave_up_button',
          octave_down_button='octave_down_button',
          scale_up_button=(self._with_shift('octave_up_button')),
          scale_down_button=(self._with_shift('octave_down_button')))
        self._instrument = MelodicComponent(skin=(self._skin),
          is_enabled=False,
          clip_creator=(self._clip_creator),
          name='Melodic_Component',
          grid_resolution=(self._grid_resolution),
          note_layout=(self._note_layout),
          note_editor_settings=(self._note_editor_settings_component),
          note_editor_class=(self.note_editor_class),
          velocity_range_thresholds=(self.note_editor_velocity_range_thresholds),
          layer=(self._create_sequence_instrument_layer()),
          sequence_layer_with_loop=(self._create_sequence_instrument_layer_with_loop()),
          instrument_play_layer=(instrument_basic_layer + Layer(matrix='matrix',
          aftertouch_control='aftertouch_control',
          delete_button='delete_button')),
          instrument_sequence_layer=(instrument_basic_layer + Layer(note_strip='touch_strip_control')),
          pitch_mod_touch_strip_mode=(LayerMode(self._pitch_mod_touch_strip, self._pitch_mod_touch_strip_layer)),
          play_loop_instrument_layer=(self._create_play_instrument_with_loop_layer()))
        self._register_matrix_mode('play',
          (self._instrument.play_modes),
          parent_path=[
         'matrix_modes', 'note', 'instrument'])
        self._register_matrix_mode('sequence',
          (self._instrument.sequence_modes),
          parent_path=[
         'matrix_modes', 'note', 'instrument'])
        self._PushBase__on_note_editor_layout_changed.subject = self._instrument

    def _create_scales_enabler(self):
        raise NotImplementedError

    def _init_scales(self):
        self._scales_enabler = self._create_scales_enabler()

    def _create_drum_step_sequencer_layer(self):
        return Layer(playhead='playhead_element',
          full_velocity='full_velocity_element',
          accent_button='accent_button',
          button_matrix=(self.elements.matrix.submatrix[:8, :4]),
          quantization_buttons='side_buttons',
          solo_button='global_solo_button',
          select_button='select_button',
          delete_button='delete_button',
          mute_button='global_mute_button',
          duplicate_button='duplicate_button')

    def _create_split_seq_layer(self):
        return Layer(playhead='playhead_element',
          full_velocity='full_velocity_element',
          accent_button='accent_button',
          button_matrix=(self.elements.matrix.submatrix[:8, :4]),
          quantization_buttons='side_buttons',
          delete_button='delete_button',
          mute_button='global_mute_button',
          duplicate_button='duplicate_button')

    def _init_split_melodic_sequencer(self):
        split_seq_note_editor = self.note_editor_class(clip_creator=(self._clip_creator),
          grid_resolution=(self._grid_resolution),
          velocity_range_thresholds=(self.note_editor_velocity_range_thresholds),
          get_notes_handler=get_all_notes,
          remove_notes_handler=remove_all_notes,
          duplicate_all_notes=True,
          is_enabled=False)
        self._selected_note_instrument = SelectedNotesInstrumentComponent(note_layout=(self._note_layout),
          note_editor_component=split_seq_note_editor,
          is_enabled=False,
          layer=Layer(octave_strip=(self._with_shift('touch_strip_control')),
          octave_up_button='octave_up_button',
          octave_down_button='octave_down_button',
          scale_up_button=(self._with_shift('octave_up_button')),
          scale_down_button=(self._with_shift('octave_down_button')),
          matrix=(self.elements.matrix.submatrix[:8, 4:8]),
          aftertouch_control='aftertouch_control',
          delete_button='delete_button',
          select_button='select_button'))
        self._note_editor_settings_component.add_editor(split_seq_note_editor)
        self._split_melodic_sequencer = StepSeqComponent((self._clip_creator),
          (self._skin),
          grid_resolution=(self._grid_resolution),
          note_editor_component=split_seq_note_editor,
          instrument_component=(self._selected_note_instrument),
          is_enabled=False,
          layer=(self._create_split_seq_layer()))
        self._split_sequencer_mode = MessengerModesComponent(muted=True, is_enabled=False)
        self._split_sequencer_mode.add_mode('default',
          (self._split_melodic_sequencer),
          default_mode='default',
          alternative_mode='alternative')
        self._split_sequencer_mode.add_mode('alternative',
          [
         self._split_melodic_sequencer,
         AddLayerMode(self._split_melodic_sequencer, Layer(loop_selector_matrix=(self.elements.double_press_matrix.submatrix[:,
          4]),
           short_loop_selector_matrix=(self.elements.double_press_event_matrix.submatrix[:,
          4])))],
          message=(consts.MessageBoxText.LAYOUT_MELODIC_32_PADS_LOOP_SELECTOR),
          default_mode='default',
          alternative_mode='alternative')
        self._split_sequencer_mode.selected_mode = 'default'
        self._instrument.add_mode('split_melodic_sequencer',
          [
         split_seq_note_editor,
         self._selected_note_instrument,
         self._split_sequencer_mode,
         self._note_editor_settings_component,
         LayerMode(self._pitch_mod_touch_strip, self._pitch_mod_touch_strip_layer)],
          message=(consts.MessageBoxText.LAYOUT_MELODIC_32_PADS))
        self._register_matrix_mode('split_melodic_sequencer',
          modes_component=(self._split_sequencer_mode),
          parent_path=[
         'matrix_modes', 'note', 'instrument'])

    def _init_drum_step_sequencer(self):
        self._drum_velocity_levels = VelocityLevelsComponent(target_note_provider=(self._drum_component),
          skin_base_key=(self.drum_group_velocity_levels_skin),
          is_enabled=False,
          layer=Layer(velocity_levels='velocity_levels_element',
          select_button='select_button'))
        drum_note_editor = self.note_editor_class(clip_creator=(self._clip_creator),
          grid_resolution=(self._grid_resolution),
          skin_base_key=(self.drum_group_note_editor_skin),
          velocity_provider=(self._drum_velocity_levels),
          velocity_range_thresholds=(self.note_editor_velocity_range_thresholds))
        self._note_editor_settings_component.add_editor(drum_note_editor)
        self._drum_step_sequencer = DrumStepSeqComponent((self._clip_creator),
          (self._skin),
          name='Drum_Step_Sequencer',
          grid_resolution=(self._grid_resolution),
          note_editor_component=drum_note_editor,
          instrument_component=(self._drum_component),
          is_enabled=False)
        self._drum_step_sequencer.layer = self._create_drum_step_sequencer_layer()
        self._audio_loop = LoopSelectorComponent(follow_detail_clip=True,
          name='Loop_Selector',
          default_size=8)
        self._audio_loop.set_enabled(False)
        self._audio_loop.layer = Layer(loop_selector_matrix='matrix')

    def _create_slicing_step_sequencer_layer(self):
        return Layer(playhead='playhead_element',
          full_velocity='full_velocity_element',
          accent_button='accent_button',
          button_matrix=(self.elements.matrix.submatrix[:8, :4]),
          quantization_buttons='side_buttons',
          select_button='select_button',
          duplicate_button='duplicate_button',
          delete_button='delete_button')

    def _init_slicing_step_sequencer(self):
        self._slicing_velocity_levels = VelocityLevelsComponent(target_note_provider=(self._slicing_component),
          skin_base_key=(self.slicing_velocity_levels_skin),
          is_enabled=False,
          layer=Layer(velocity_levels='velocity_levels_element',
          select_button='select_button'))
        slice_note_editor = self.note_editor_class(clip_creator=(self._clip_creator),
          grid_resolution=(self._grid_resolution),
          skin_base_key=(self.slicing_note_editor_skin),
          velocity_provider=(self._slicing_velocity_levels),
          velocity_range_thresholds=(self.note_editor_velocity_range_thresholds))
        self._note_editor_settings_component.add_editor(slice_note_editor)
        self._slicing_step_sequencer = StepSeqComponent((self._clip_creator),
          (self._skin),
          name='Slice_Step_Sequencer',
          grid_resolution=(self._grid_resolution),
          note_editor_component=slice_note_editor,
          instrument_component=(self._slicing_component),
          is_enabled=False)
        self._slicing_step_sequencer.layer = self._create_slicing_step_sequencer_layer()

    def _create_drum_component(self):
        raise NotImplementedError

    def _init_drum_component(self):
        self._drum_component = self._create_drum_component()
        self._drum_component.layer = Layer(page_strip='touch_strip_control',
          scroll_strip=(self._with_shift('touch_strip_control')),
          solo_button='global_solo_button',
          select_button='select_button',
          delete_button='delete_button',
          scroll_page_up_button='octave_up_button',
          scroll_page_down_button='octave_down_button',
          quantize_button='quantize_button',
          duplicate_button='duplicate_button',
          mute_button='global_mute_button',
          scroll_up_button=(self._with_shift('octave_up_button')),
          scroll_down_button=(self._with_shift('octave_down_button')),
          accent_button='accent_button',
          full_velocity='full_velocity_element')

    def _init_slicing_component(self):
        self._slicing_component = self.sliced_simpler_class(quantizer=(self._quantize),
          is_enabled=False)
        self._slicing_component.layer = Layer(scroll_page_up_button='octave_up_button',
          scroll_page_down_button='octave_down_button',
          scroll_up_button=(self._with_shift('octave_up_button')),
          scroll_down_button=(self._with_shift('octave_down_button')),
          delete_button='delete_button',
          select_button='select_button',
          quantize_button='quantize_button',
          accent_button='accent_button',
          full_velocity='full_velocity_element')

    def _init_note_repeat(self):
        self._note_repeat_enabler = NoteRepeatEnabler(note_repeat=(self._c_instance.note_repeat))
        self._note_repeat_enabler.set_enabled(False)
        self._note_repeat_enabler.layer = Layer(repeat_button='repeat_button')
        self._note_repeat_enabler.note_repeat_component.layer = self._create_note_repeat_layer()

    def _create_note_repeat_layer(self):
        return Layer(aftertouch_control='aftertouch_control',
          select_buttons='side_buttons',
          priority=(consts.DIALOG_PRIORITY))

    def _init_notification(self):
        self._notification = self._create_notification_component()

    def _create_notification_component(self):
        raise NotImplementedError

    def _create_message_box_background_layer(self):
        return BackgroundLayer('select_buttons',
          'track_state_buttons',
          'scale_presets_button',
          'octave_up_button',
          'octave_down_button',
          'side_buttons',
          'repeat_button',
          'accent_button',
          'global_param_controls',
          'global_param_touch_buttons',
          'touch_strip_control',
          'touch_strip_tap',
          'matrix',
          'nav_up_button',
          'nav_down_button',
          'nav_left_button',
          'nav_right_button',
          'shift_button',
          'select_button',
          'delete_button',
          'duplicate_button',
          'double_button',
          'quantize_button',
          'play_button',
          'new_button',
          'automation_button',
          'tap_tempo_button',
          'metronome_button',
          'fixed_length_button',
          'record_button',
          'undo_button',
          'tempo_control',
          'swing_control',
          'master_volume_control',
          'global_param_controls',
          'vol_mix_mode_button',
          'pan_send_mix_mode_button',
          'single_track_mix_mode_button',
          'clip_mode_button',
          'device_mode_button',
          'browse_mode_button',
          'user_button',
          'master_select_button',
          'create_device_button',
          'create_track_button',
          'global_track_stop_button',
          'global_mute_button',
          'global_solo_button',
          'note_mode_button',
          'session_mode_button',
          priority=(consts.MESSAGE_BOX_PRIORITY))

    def _create_message_box_layer(self):
        raise RuntimeError

    def _init_message_box(self):
        self._dialog = DialogComponent(is_enabled=True)
        self._dialog.message_box_layer = (
         self._create_message_box_background_layer(),
         self._create_message_box_layer())

    def _for_non_frozen_tracks(self, component, **k):
        TrackFrozenModesComponent(default_mode=component, 
         frozen_mode=self._track_frozen_info, **k)
        return component

    def _init_undo_redo_actions(self):
        self._undo_redo = UndoRedoComponent(name='Undo_Redo')
        self._undo_redo.layer = Layer(undo_button='undo_button',
          redo_button=(self._with_shift('undo_button')))

    def _init_stop_clips_action(self):
        pass

    def _create_capture_and_insert_scene_component(self):
        return CaptureAndInsertSceneComponent(name='Capture_And_Insert_Scene')

    def _init_duplicate_actions(self):
        capture_element = ChoosingElement(self._settings['workflow'], 'duplicate_button', self._with_shift('duplicate_button'))
        self._capture_and_insert_scene = self._create_capture_and_insert_scene_component()
        self._capture_and_insert_scene.set_enabled(True)
        self._capture_and_insert_scene.layer = Layer(action_button=capture_element)
        duplicate_element = OptionalElement('duplicate_button', self._settings['workflow'], False)
        self._duplicate_detail_clip = DuplicateDetailClipComponent(name='Duplicate_Detail_Clip')
        self._duplicate_detail_clip.set_enabled(True)
        self._duplicate_detail_clip.layer = Layer(action_button=duplicate_element)
        self._duplicate_loop = self._for_non_frozen_tracks(DuplicateLoopComponent(name='Duplicate_Loop',
          layer=Layer(action_button='double_button'),
          is_enabled=False))

    def _init_delete_actions(self):
        self._delete_component = DeleteComponent(name='Deleter')
        self._delete_component.layer = Layer(delete_button='delete_button')
        self._delete_default_component = DeleteAndReturnToDefaultComponent(name='DeleteAndDefault')
        self._delete_default_component.layer = Layer(delete_button='delete_button')
        self._delete_clip = DeleteSelectedClipComponent(name='Selected_Clip_Deleter')
        self._delete_clip.layer = Layer(action_button='delete_button')
        self._delete_scene = DeleteSelectedSceneComponent(name='Selected_Scene_Deleter')
        self._delete_scene.layer = Layer(action_button=(self._with_shift('delete_button')))

    def _init_quantize_actions(self):
        raise NotImplementedError

    def _init_value_components(self):
        self._swing_amount = ValueComponent('swing_amount',
          (self.song),
          display_label='Swing Amount:',
          display_format='%d%%',
          model_transform=(lambda x: clamp(old_div(x, 200.0), 0.0, 0.5)
),
          view_transform=(lambda x: x * 200.0
),
          encoder_factor=100.0,
          encoder_touch_delay=TEMPO_SWING_TOUCH_DELAY)
        self._swing_amount.layer = Layer(encoder='swing_control')
        tempo_param = self.song.master_track.mixer_device.song_tempo
        self._tempo = ValueComponent('tempo',
          (self.song),
          display_label='Tempo:',
          display_format='%0.2f BPM',
          encoder_factor=128.0,
          encoder_touch_delay=TEMPO_SWING_TOUCH_DELAY,
          model_transform=(lambda x: clamp(x, tempo_param.min, tempo_param.max)
))
        self._tempo.layer = Layer(encoder='tempo_control', shift_button='shift_button')
        self._master_vol = ParameterValueComponent((self.song.master_track.mixer_device.volume),
          display_label='Master Volume:',
          display_seg_start=3,
          name='Master_Volume_Display')
        self._master_vol.layer = Layer(encoder='master_volume_control')
        self._master_cue_vol = ParameterValueComponent((self.song.master_track.mixer_device.cue_volume),
          display_label='Cue Volume:',
          display_seg_start=3,
          name='Cue_Volume_Display')
        self._master_cue_vol.layer = Layer(encoder=(self._with_shift('master_volume_control')))

    def mxd_grab_control_priority(self):
        return consts.M4L_PRIORITY

    @listens('selected_mode')
    def __on_note_editor_layout_changed(self, mode):
        self.reset_controlled_track(mode)
        if mode:
            if self._save_note_modes:
                self.song.view.selected_track.set_data('push-selected-note-mode', mode)

    @listens('selected_mode')
    def __on_drums_note_layout_changed(self, mode):
        if mode:
            if self._save_note_modes:
                self.song.view.selected_track.set_data('push-selected-note-mode', mode)

    @listens('selected_mode')
    def __on_slicing_note_layout_changed(self, mode):
        if mode:
            if self._save_note_modes:
                self.song.view.selected_track.set_data('push-selected-note-mode', mode)

    def _save_default_note_layout(self, track):
        if self._note_modes.selected_mode == 'drums':
            track.set_data('push-selected-note-mode', 'sequencer_loop')
        else:
            if self._note_modes.selected_mode == 'slicing':
                track.set_data('push-selected-note-mode', '64pads')
            else:
                if self._note_modes.selected_mode == 'instrument':
                    track.set_data('push-selected-note-mode', 'play')

    def _load_alternative_note_layout(self):
        current_alternative_mode = self._get_current_alternative_layout_mode()
        if current_alternative_mode:
            default_mode, alternative_mode = current_alternative_mode.get_default_mode_and_alternative_mode()
            if self.song.view.selected_track.get_data('alternative_mode_locked', False) and alternative_mode:
                current_alternative_mode.selected_mode = alternative_mode
                self._note_layout_switcher.cycle_button.color = 'DefaultButton.Alert'
            else:
                if default_mode:
                    current_alternative_mode.selected_mode = default_mode
                    self._note_layout_switcher.cycle_button.color = 'DefaultButton.On'
        else:
            self._note_layout_switcher.cycle_button.color = 'DefaultButton.On'

    def _load_saved_note_layout(self, track, saved_mode):
        drum_device, sliced_simpler = self._percussion_instruments_for_track(track)
        self._drum_component.set_drum_group_device(drum_device)
        self._slicing_component.set_simpler(sliced_simpler)
        if liveobj_valid(drum_device) and saved_mode in self._drum_modes.modes:
            self._drum_modes.selected_mode = saved_mode
        else:
            if liveobj_valid(sliced_simpler) and saved_mode in self._slicing_modes.modes:
                self._slicing_modes.selected_mode = saved_mode
            else:
                if saved_mode in self._instrument.modes:
                    self._instrument.selected_mode = saved_mode
        self._load_alternative_note_layout()

    def recall_or_save_note_layout(self, mode=None):
        track = self.song.view.selected_track
        saved_mode = track.get_data('push-selected-note-mode', None)
        if mode == None:
            if saved_mode:
                self._load_saved_note_layout(track, saved_mode)
            else:
                self._save_default_note_layout(track)

    def reset_controlled_track(self, mode=None):
        if self._instrument.is_enabled() and mode == 'sequence':
            self.release_controlled_track()
        else:
            self.set_controlled_track(self.song.view.selected_track)

    @listens('selected_track.is_frozen')
    def __on_selected_track_is_frozen_changed(self):
        self._select_note_mode()

    def _on_selected_track_changed(self):
        self._note_layout_switcher.release_alternative_layout()
        self._select_note_mode()

    def _send_midi(self, midi_event_bytes, optimized=True):
        if not (self._suppress_sysex and midi.is_sysex(midi_event_bytes)):
            return super(PushBase, self)._send_midi(midi_event_bytes, optimized)

    def _update_playhead_color(self, color):
        self._instrument.playhead_color = color
        self._drum_step_sequencer.playhead_color = color
        self._split_melodic_sequencer.playhead_color = color
        self._slicing_step_sequencer.playhead_color = color

    @listens('session_record')
    def __on_session_record_changed(self):
        status = self.song.session_record
        self._update_playhead_color('PlayheadRecord' if status else 'Playhead')
        feedback_color = int(to_midi_value(self._skin['Instrument.FeedbackRecord']) if status else to_midi_value(self._skin['Instrument.Feedback']))
        self._c_instance.set_feedback_velocity(feedback_color)

    @listens('enabled')
    def __on_fixed_length_enabled_changed(self, enabled):
        self.preferences['fixed_length_enabled'] = enabled

    @listens('selected_index')
    def __on_fixed_length_selected_index_changed(self, index):
        self.preferences['fixed_length_option'] = index

    @listens('legato_launch')
    def __on_fixed_length_legato_launch_changed(self, value):
        self.preferences['fixed_length_legato_launch'] = value

    @listens('before_mode_sent')
    def __on_before_hardware_mode_sent(self, mode):
        self._suppress_sysex = False

    @listens('after_mode_sent')
    def __on_after_hardware_mode_sent(self, mode):
        if mode == sysex.USER_MODE:
            self._suppress_sysex = True

    @listens('mode')
    def __on_hardware_mode_changed(self, mode):
        if mode == sysex.USER_MODE:
            self._suppress_sysex = True
            self.request_rebuild_midi_map()
            for control in self.controls:
                control.clear_send_cache()

        self._update_auto_arm()

    @listens('selected_mode')
    def __on_matrix_mode_changed(self, mode):
        self._update_auto_arm(selected_mode=mode)

    def _update_auto_arm(self, selected_mode=None):
        self._auto_arm.set_enabled(self._user.mode == sysex.LIVE_MODE and (selected_mode or self._matrix_modes.selected_mode) == 'note')

    @listens('instrument')
    def __on_percussion_instrument_changed(self):
        self._select_note_mode()

    def _select_note_mode(self):
        track = self.song.view.selected_track
        drum_device, sliced_simpler = self._percussion_instruments_for_track(track)
        self._drum_component.set_drum_group_device(drum_device)
        self._slicing_component.set_simpler(sliced_simpler)
        if track == None or track.is_foldable or track in self.song.return_tracks or track == self.song.master_track or track.is_frozen:
            self._note_modes.selected_mode = 'disabled'
        else:
            if track and track.has_audio_input:
                self._note_modes.selected_mode = 'looper'
            else:
                if drum_device:
                    self._note_modes.selected_mode = 'drums'
                else:
                    if sliced_simpler:
                        self._note_modes.selected_mode = 'slicing'
                    else:
                        self._note_modes.selected_mode = 'instrument'
        self.recall_or_save_note_layout()
        self.reset_controlled_track()

    def _percussion_instruments_for_track(self, track):
        self._percussion_instrument_finder.device_parent = track
        drum_device = self._percussion_instrument_finder.drum_group
        sliced_simpler = self._percussion_instrument_finder.sliced_simpler
        return (
         drum_device, sliced_simpler)

    def _setup_accidental_touch_prevention(self):
        self._accidental_touch_prevention_layer = BackgroundLayer('tempo_control_tap',
          'swing_control_tap',
          'master_volume_control_tap',
          priority=(consts.MOMENTARY_DIALOG_PRIORITY))
        self._PushBase__on_param_encoder_touched.replace_subjects(self.elements.global_param_touch_buttons_raw)

    @listens_group('value')
    def __on_param_encoder_touched(self, value, encoder):
        if any(map(lambda e: e.is_pressed()
, self.elements.global_param_touch_buttons_raw)):
            self._accidental_touch_prevention_layer.grab(self)
        else:
            self._accidental_touch_prevention_layer.release(self)

    def get_matrix_button(self, column, row):
        return self.elements.matrix_rows_raw[7 - row][column]

    def expect_dialog(self, message):
        self.schedule_message(1, partial(self._dialog.expect_dialog, message))

    def show_notification(self, message, blink_text=None, notification_time=None):
        return self._notification.show_notification(message, blink_text, notification_time)

    def process_midi_bytes(self, midi_bytes, midi_processor):
        if not midi.is_sysex(midi_bytes):
            recipient = self.get_recipient_for_nonsysex_midi_message(midi_bytes)
            if isinstance(recipient, ButtonElement):
                if midi.extract_value(midi_bytes) != 0:
                    if self._notification is not None:
                        self._notification.hide_notification()
        super(PushBase, self).process_midi_bytes(midi_bytes, midi_processor)