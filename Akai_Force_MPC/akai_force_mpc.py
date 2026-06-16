# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\akai_force_mpc.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 23550 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import zip
from contextlib import contextmanager
from functools import partial
from itertools import chain
from ableton.v2.base import const, inject, task
from ableton.v2.control_surface import BankingInfo, ControlSurface, DeviceDecoratorFactory, Layer, Skin
from ableton.v2.control_surface.components import BackgroundComponent, RightAlignTracksTrackAssigner, SessionRingComponent, UndoRedoComponent
from ableton.v2.control_surface.default_bank_definitions import BANK_DEFINITIONS as DEFAULT_BANK_DEFINITIONS
from ableton.v2.control_surface.elements import MultiElement, SysexElement
from ableton.v2.control_surface.mode import AddLayerMode, LayerMode, ModesComponent, MomentaryBehaviour
from .background import LightingBackgroundComponent
from .channel_strip import ChannelStripComponent
from .clip_actions import ClipActionsComponent
from .device import DeviceComponent
from .device_navigation import ScrollingDeviceNavigationComponent
from .device_parameters import DeviceParameterComponent
from .elements import NUM_SCENE_CONTROLS, NUM_TRACK_CONTROLS, ForceElements, MPCLiveElements, MPCXElements
from .mixer import MixerComponent
from .mode import ExtendComboElementMode
from .ping_pong import PingPongComponent
from .scene_list import SceneListComponent
from .session import SessionComponent
from .session_navigation import SessionNavigationComponent
from .session_recording import SessionRecordingComponent
from .skin import ForceColors, MPCColors
from .sysex import BROADCAST_ID, FORCE_PRODUCT_ID, MPC_LIVE_PRODUCT_ID, MPC_X_PRODUCT_ID, PING_MSG_TYPE, PONG_MSG_TYPE, SUPPORTED_PRODUCT_IDS, SYSEX_END_BYTE, SYSEX_MSG_HEADER
from .sysex_element import IdentifyingSysexElement
from .transport import ForceTransportComponent, MPCTransportComponent

class Akai_Force_MPC(ControlSurface):

    def __init__(self, *a, **k):
        (super(Akai_Force_MPC, self).__init__)(*a, **k)
        self._product_id = None
        self._element_injector = inject(element_container=(const(None))).everywhere()
        self._is_initialized = False
        self._initialize_task = self._tasks.add(task.run(self._initialize))
        self._initialize_task.kill()
        self._components_enabled = False
        with self.component_guard():
            self._ping_element = SysexElement(send_message_generator=(const(SYSEX_MSG_HEADER + (BROADCAST_ID, PING_MSG_TYPE, SYSEX_END_BYTE))),
              name='Ping_Element')
            self._pong_element = MultiElement(*[IdentifyingSysexElement(sysex_identifier=(SYSEX_MSG_HEADER + (identifier, PONG_MSG_TYPE)), name=('Pong_Element_{}'.format(index))) for index, identifier in enumerate(SUPPORTED_PRODUCT_IDS)], **{'name': 'Pong_Multi_Element'})
            self._ping_pong = PingPongComponent(on_pong_callback=(self._identify),
              on_ping_timeout=(partial(self._enable_components, False)),
              name='Ping_Pong')
            self._ping_pong.layer = Layer(ping=(self._ping_element),
              pong=(self._pong_element))

    @contextmanager
    def _component_guard(self):
        with super(Akai_Force_MPC, self)._component_guard():
            with self._element_injector:
                yield

    @property
    def is_force(self):
        return self._product_id == FORCE_PRODUCT_ID

    def _identify(self, id_byte):
        if id_byte in SUPPORTED_PRODUCT_IDS:
            if not self._is_initialized:
                self._product_id = id_byte
                self._create_elements()
                self._initialize_task.restart()
            else:
                if self._product_id == id_byte:
                    self._enable_components(True)

    def _initialize(self):
        self._create_components()
        self._is_initialized = True
        self._enable_components(True)

    def _create_elements(self):
        with self.component_guard():
            skin = Skin(ForceColors if self.is_force else MPCColors)
            with inject(skin=(const(skin))).everywhere():
                elements_class = None
                if self.is_force:
                    elements_class = ForceElements
                else:
                    if self._product_id == MPC_X_PRODUCT_ID:
                        elements_class = MPCXElements
                    else:
                        if self._product_id == MPC_LIVE_PRODUCT_ID:
                            elements_class = MPCLiveElements
                self._elements = elements_class(self._product_id)
        self._element_injector = inject(element_container=(const(self._elements))).everywhere()

    def _create_components(self):
        with self.component_guard():
            self._create_mixer()
            self._create_session()
            self._create_session_navigation()
            self._create_transport()
            self._create_actions()
            if self.is_force:
                self._create_track_assign_button_modes()
                self._create_background()
            self._create_launch_modes()
            self._create_device()
            self._create_session_recording()

    def _enable_components(self, enable):
        if self._components_enabled != enable:
            if enable:
                self._clear_send_cache()
            with self.component_guard():
                self._components_enabled = enable
                for component in [c for c in self.root_components if c is not self._ping_pong]:
                    component.set_enabled(enable)

    def _clear_send_cache(self):
        for control in self.controls:
            control.clear_send_cache()

    def _create_mixer(self):
        self._session_ring = SessionRingComponent(is_enabled=False,
          num_tracks=NUM_TRACK_CONTROLS,
          num_scenes=NUM_SCENE_CONTROLS,
          tracks_to_use=(lambda: tuple(self.song.visible_tracks) + tuple(self.song.return_tracks) + (self.song.master_track,)
),
          name='Session_Ring')
        self._mixer = MixerComponent(is_enabled=False,
          tracks_provider=(self._session_ring),
          track_assigner=RightAlignTracksTrackAssigner(song=(self.song),
          include_master_track=True),
          channel_strip_component_type=ChannelStripComponent,
          name='Mixer',
          layer=Layer(volume_controls='volume_sliders',
          pan_controls='pan_sliders',
          solo_buttons='solo_buttons',
          mute_buttons='mute_buttons',
          arm_buttons='arm_buttons',
          send_controls='send_encoders',
          track_type_controls='track_type_controls',
          output_meter_left_controls='meter_controls_left',
          output_meter_right_controls='meter_controls_right',
          track_select_buttons='track_select_buttons',
          track_name_displays='track_name_displays',
          num_sends_control='num_sends_control',
          track_color_controls='tui_track_color_controls',
          oled_display_style_controls='oled_display_style_controls_bank_1',
          track_name_or_volume_value_displays='track_name_or_volume_value_displays',
          crossfade_assign_controls='crossfade_assign_controls',
          crossfader_control='crossfader',
          solo_mute_buttons='solo_mute_buttons',
          volume_value_displays='volume_value_displays',
          pan_value_displays='pan_value_displays',
          send_value_displays='send_value_displays'))
        if not self.is_force:
            self._mixer.layer += Layer(selected_track_arm_button='selected_track_arm_button',
              selected_track_mute_button='selected_track_mute_button',
              selected_track_solo_button='selected_track_solo_button')
        else:
            self._mixer.layer += Layer(master_button='master_button',
              physical_track_color_controls='physical_track_color_controls')

    def _create_session(self):
        self._session = SessionComponent(is_enabled=False,
          session_ring=(self._session_ring),
          name='Session',
          layer=Layer(stop_track_clip_buttons='clip_stop_buttons',
          clip_launch_buttons='clip_launch_buttons',
          scene_launch_buttons='scene_launch_buttons',
          clip_name_displays='clip_name_displays',
          scene_name_displays='scene_name_displays',
          scene_color_controls='tui_scene_color_controls',
          clip_color_controls='clip_color_controls',
          playing_position_controls='playing_position_controls',
          select_button=('clip_select_button' if self.is_force else 'shift_button'),
          scene_selection_controls='scene_selection_controls',
          stop_all_clips_button='stop_all_clips_button',
          insert_scene_button='insert_scene_button'))
        if self.is_force:
            self._session.layer += Layer(force_scene_launch_buttons='force_physical_scene_launch_buttons')

    def _create_session_navigation(self):
        self._session_navigation = SessionNavigationComponent(is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(page_up_button='up_button_with_shift',
          page_down_button='down_button_with_shift',
          page_left_button='left_button_with_shift',
          page_right_button='right_button_with_shift',
          up_button='up_button',
          down_button='down_button',
          left_button='left_button',
          right_button='right_button'),
          name='Session_Navigation')

    def _create_track_assign_button_modes(self):
        self._background = BackgroundComponent(name='Background')
        self._modes = ModesComponent(name='Track_Assign_Button_Modes', is_enabled=False)
        self._modes.add_mode('mute', [
         ExtendComboElementMode(combo_pairs=(list(zip(self._elements.mute_buttons_raw, self._elements.track_assign_buttons_raw)))),
         AddLayerMode(self._mixer, Layer(mute_color_controls='track_assign_color_controls'))])
        self._modes.add_mode('solo', [
         ExtendComboElementMode(combo_pairs=(list(zip(self._elements.solo_buttons_raw, self._elements.track_assign_buttons_raw)))),
         AddLayerMode(self._mixer, Layer(solo_color_controls='track_assign_color_controls'))])
        self._modes.add_mode('rec_arm', [
         ExtendComboElementMode(combo_pairs=(list(zip(self._elements.arm_buttons_raw, self._elements.track_assign_buttons_raw)))),
         AddLayerMode(self._mixer, Layer(arm_color_controls='track_assign_color_controls'))])
        self._modes.add_mode('clip_stop', [
         ExtendComboElementMode(combo_pairs=(list(zip(self._elements.clip_stop_buttons_raw, self._elements.track_assign_buttons_raw)))),
         AddLayerMode(self._session, Layer(stop_clip_color_controls='track_assign_color_controls'))])
        self._modes.add_mode('shift',
          [
         AddLayerMode(self._transport, Layer(metronome_color_control='track_assign_color_controls_raw[4]',
           clip_trigger_quantization_color_controls='physical_track_color_controls')),
         AddLayerMode(self._clip_actions, Layer(quantize_color_control='track_assign_color_controls_raw[0]')),
         LayerMode(self._background, Layer(button1='track_assign_color_controls_raw[1]',
           button2='track_assign_color_controls_raw[2]',
           button3='track_assign_color_controls_raw[3]',
           button5='track_assign_color_controls_raw[5]',
           button6='track_assign_color_controls_raw[6]',
           button7='track_assign_color_controls_raw[7]'))],
          behaviour=(MomentaryBehaviour()))
        self._modes.add_mode('assign_a',
          [
         AddLayerMode(self._mixer, Layer(assign_a_buttons='track_assign_buttons',
           assign_a_color_controls='track_assign_color_controls'))],
          behaviour=(MomentaryBehaviour()))
        self._modes.add_mode('assign_b',
          [
         AddLayerMode(self._mixer, Layer(assign_b_buttons='track_assign_buttons',
           assign_b_color_controls='track_assign_color_controls'))],
          behaviour=(MomentaryBehaviour()))
        self._modes.layer = Layer(mute_button='mute_button',
          solo_button='solo_button',
          rec_arm_button='rec_arm_button',
          clip_stop_button='clip_stop_button',
          shift_button='shift_button',
          assign_a_button='assign_a_button',
          assign_b_button='assign_b_button')
        self._modes.selected_mode = 'clip_stop'

    def _create_background(self):
        self.background = LightingBackgroundComponent(name='Background')
        self.background.layer = Layer(launch_button='launch_button')

    def _create_launch_modes(self):
        self._scene_list = SceneListComponent(name='Expanded_Scene_Launch',
          session_ring=(self._session_ring),
          num_scenes=16)
        self._launch_modes = ModesComponent(name='Launch_Modes')
        self._launch_modes.add_mode('clip_launch',
          [
         partial(self._elements.launch_mode_switch.send_value, 0),
         ExtendComboElementMode(combo_pairs=(list(zip(chain(*self._elements.clip_launch_buttons_raw), chain(*self._elements.physical_clip_launch_buttons_raw))))),
         ExtendComboElementMode(combo_pairs=(list(zip(chain(*self._elements.clip_color_controls_raw), chain(*self._elements.physical_clip_color_controls_raw)))))],
          cycle_mode_button_color='Mode.Off')
        if not self.is_force:
            self._launch_modes.add_mode('scene_launch',
              [
             partial(self._elements.launch_mode_switch.send_value, 1),
             LayerMode(self._scene_list, Layer(scene_launch_buttons='mpc_scene_launch_buttons',
               scene_color_controls='mpc_scene_color_controls'))],
              cycle_mode_button_color='Mode.On')
            self._launch_modes.layer = Layer(cycle_mode_button=('xyfx_button' if self._product_id == MPC_X_PRODUCT_ID else 'sixteen_level_button'))
        self._launch_modes.selected_mode = 'clip_launch'

    def _create_actions(self):
        self._clip_actions = ClipActionsComponent(name='Clip_Actions',
          is_enabled=False,
          layer=Layer(duplicate_button='duplicate_button',
          quantization_value_control='quantization_value_control',
          quantize_button='quantize_button',
          delete_button='delete_button'))
        self._undo_redo = UndoRedoComponent(name='Undo_Redo',
          is_enabled=False,
          layer=Layer(undo_button='undo_button', redo_button='redo_button'))
        self._undo_redo.undo_button.color = 'Action.On'
        self._undo_redo.redo_button.color = 'Action.On'

    def _create_device(self):
        self._device = DeviceComponent(is_enabled=False,
          device_decorator_factory=(DeviceDecoratorFactory()),
          device_bank_registry=(self._device_bank_registry),
          banking_info=(BankingInfo(DEFAULT_BANK_DEFINITIONS)),
          toggle_lock=(self.toggle_lock),
          name='Device',
          layer=Layer(prev_bank_button='prev_bank_button',
          next_bank_button='next_bank_button',
          bank_name_display='device_bank_name_display',
          device_lock_button='device_lock_button'))
        self._device_parameters = DeviceParameterComponent(is_enabled=False,
          parameter_provider=(self._device),
          name='Device_Parameters',
          layer=Layer(parameter_controls='physical_device_controls',
          absolute_parameter_controls='tui_device_controls',
          parameter_enable_controls='device_parameter_enable_controls',
          display_style_controls='oled_display_style_controls_bank_2',
          touch_controls='physical_device_control_touch_elements',
          parameter_name_or_value_displays='device_parameter_name_or_value_displays',
          parameter_name_displays='tui_device_parameter_name_displays',
          parameter_value_displays='tui_device_parameter_value_displays',
          device_enable_button='device_enable_button'))
        self._device_navigation = ScrollingDeviceNavigationComponent(is_enabled=False,
          name='Device_Navigation',
          device_component=(self._device),
          layer=Layer(prev_device_button='prev_device_button',
          next_device_button='next_device_button',
          num_devices_control='num_devices_control',
          device_index_control='device_index_control',
          device_name_display='device_name_display'))

    def _create_transport(self):
        transport_component_class = ForceTransportComponent if self.is_force else MPCTransportComponent
        self._transport = transport_component_class(is_enabled=False,
          name='Transport',
          layer=Layer(tempo_display='tempo_display',
          tempo_control='tempo_control',
          play_button='play_button',
          continue_playing_button='continue_button',
          stop_button='stop_button',
          tap_tempo_button='tap_tempo_button',
          shift_button='shift_button',
          nudge_down_button='phase_nudge_down_button',
          nudge_up_button='phase_nudge_up_button',
          tui_metronome_button='tui_metronome_button',
          metronome_button='physical_metronome_button',
          loop_button='loop_button',
          arrangement_overdub_button='arrangement_overdub_button',
          follow_song_button='follow_song_button',
          clip_trigger_quantization_control='clip_trigger_quantization_control',
          loop_start_display='tui_loop_start_display',
          loop_length_display='tui_loop_length_display',
          arrangement_position_display='tui_arrangement_position_display',
          loop_start_control='tui_loop_start_control',
          loop_length_control='tui_loop_length_control',
          arrangement_position_control='tui_arrangement_position_control',
          tui_arrangement_record_button='tui_arrangement_record_button'))
        self._transport.tap_tempo_button.color = 'Transport.TapTempo'
        if self.is_force:
            self._transport.layer += Layer(clip_trigger_quantization_button_row='physical_track_select_buttons_with_shift')
        else:
            self._transport.layer += Layer(record_button='arrangement_record_button',
              jump_backward_button='jump_backward_button',
              jump_forward_button='jump_forward_button')

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(is_enabled=False,
          name='Session_Recording',
          layer=Layer(record_button='session_record_button',
          automation_button='tui_automation_arm_button'))
        if not self.is_force:
            self._session_recording.layer += Layer(mpc_automation_toggle='read_write_button')