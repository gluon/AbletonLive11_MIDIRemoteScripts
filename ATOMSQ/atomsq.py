#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/atomsq.py
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import const, inject, listens
from ableton.v2.control_surface import ControlSurface, Layer, SessionRingSelectionLinking
from ableton.v2.control_surface.components import BackgroundComponent, MixerComponent, SessionNavigationComponent, SessionRecordingComponent, SessionRingComponent, SimpleTrackAssigner, UndoRedoComponent
from ableton.v2.control_surface.mode import AddLayerMode, EnablingMode, ModesComponent
from novation.simple_device_navigation import SimpleDeviceNavigationComponent
from novation.view_control import NotifyingViewControlComponent
from . import midi
from .button_labels import ButtonLabelsComponent
from .channel_strip import ChannelStripComponent
from .elements import BANK_BUTTON_NAMES, Elements, SESSION_HEIGHT, SESSION_WIDTH
from .launch_and_stop import LaunchAndStopComponent
from .session import SessionComponent
from .simple_device import SimpleDeviceParameterComponent
from .translating_background import TranslatingBackgroundComponent
from .transport import TransportComponent
from .view_toggle import ViewToggleComponent

class ATOMSQ(ControlSurface):

    def __init__(self, *a, **k):
        super(ATOMSQ, self).__init__(*a, **k)
        with self.component_guard():
            self._elements = Elements()
            with inject(element_container=const(self._elements)).everywhere():
                self._create_background()
                self._create_transport()
                self._create_undo()
                self._create_view_toggle()
                self._create_device_parameters()
                self._create_translating_background()
                self._create_device_navigation()
                self._create_launch_and_stop()
                self._create_session()
                self._create_mixer()
                self._create_view_control()
                self._create_button_labels()
                self._create_record_modes()
                self._create_lower_pad_modes()
                self._create_main_modes()
        self.__on_main_view_changed.subject = self.application.view

    def disconnect(self):
        super(ATOMSQ, self).disconnect()
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)

    def port_settings_changed(self):
        self._send_midi(midi.NATIVE_MODE_ON_MESSAGE)
        if self._main_modes.selected_mode == u'instrument':
            self.schedule_message(1, self._elements.upper_firmware_toggle_switch.send_value, 1)
        if self._main_modes.selected_mode != u'song':
            self.schedule_message(1, self._elements.lower_firmware_toggle_switch.send_value, 1)
        super(ATOMSQ, self).port_settings_changed()

    def _create_background(self):
        self._background = BackgroundComponent(name=u'Background', is_enabled=False, add_nop_listeners=True, layer=Layer(**{name:name for name in BANK_BUTTON_NAMES}))
        self._background.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name=u'Transport', is_enabled=False, layer=Layer(scroll_encoder=u'display_encoder', play_button=u'play_button', loop_button=u'play_button_with_shift', stop_button=u'stop_button', metronome_button=u'click_button', capture_midi_button=u'record_button_with_shift', prev_cue_button=u'display_left_button', next_cue_button=u'display_right_button', shift_button=u'shift_button'))
        self._transport.set_enabled(True)

    def _create_undo(self):
        self._undo = UndoRedoComponent(name=u'Undo', is_enabled=False, layer=Layer(undo_button=u'stop_button_with_shift'))
        self._undo.set_enabled(True)

    def _create_view_toggle(self):
        self._view_toggle = ViewToggleComponent(name=u'View_Toggle', is_enabled=False, layer=Layer(main_view_toggle_button=u'bank_a_button', browser_view_toggle_button=u'bank_b_button', detail_view_toggle_button=u'bank_d_button', clip_view_toggle_button=u'bank_h_button'))

    def _create_device_parameters(self):
        self._device_parameters = SimpleDeviceParameterComponent(name=u'Device_Parameters', device_bank_registry=self._device_bank_registry, toggle_lock=self.toggle_lock, layer=Layer(device_name_display=u'device_name_display'), is_enabled=False)
        self._device_parameters.set_enabled(True)

    def _create_translating_background(self):
        self._translating_background = TranslatingBackgroundComponent(name=u'Translating_Background', is_enabled=False, add_nop_listeners=True, layer=Layer(encoders=u'encoders', channel_selection_buttons=u'display_buttons'))

    def _create_device_navigation(self):
        self._device_navigation = SimpleDeviceNavigationComponent(name=u'Device_Navigation', is_enabled=False, layer=Layer(prev_button=u'display_buttons_raw[1]', next_button=u'display_buttons_raw[2]'))

    def _create_launch_and_stop(self):
        self._launch_and_stop = LaunchAndStopComponent(name=u'Launch_And_Stop', is_enabled=False, layer=Layer(clip_launch_button=u'display_buttons_raw[3]', scene_launch_button=u'display_buttons_raw[4]', track_stop_button=u'display_buttons_raw[5]'))

    def _create_session(self):
        self._session_ring = SessionRingComponent(name=u'Session_Ring', num_tracks=SESSION_WIDTH, num_scenes=SESSION_HEIGHT)
        self._session = SessionComponent(name=u'Session', is_enabled=False, session_ring=self._session_ring, layer=Layer(clip_launch_buttons=u'upper_pads'))
        self._session_navigation = SessionNavigationComponent(name=u'Session_Navigation', is_enabled=False, session_ring=self._session_ring, layer=Layer(up_button=u'up_button_with_shift', down_button=u'down_button_with_shift'))
        self._session_navigation.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(name=u'Mixer', auto_name=True, tracks_provider=self._session_ring, track_assigner=SimpleTrackAssigner(), channel_strip_component_type=ChannelStripComponent)
        self._mixer.selected_strip().layer = Layer(track_name_display=u'track_name_display')
        self._mixer.set_enabled(True)

    def _create_view_control(self):
        self._view_control = NotifyingViewControlComponent(name=u'View_Control', is_enabled=False, track_provider=self._session_ring, enable_skinning=False, layer=Layer(next_track_button=u'right_button', prev_track_button=u'left_button', next_scene_button=u'down_button', prev_scene_button=u'up_button'))
        self._view_control.set_enabled(True)
        self._session_ring_selection_linking = self.register_disconnectable(SessionRingSelectionLinking(session_ring=self._session_ring, selection_changed_notifier=self._view_control))

    def _create_button_labels(self):
        self._button_labels = ButtonLabelsComponent(is_enabled=False, layer=Layer(display_lines=u'button_label_display_matrix'))
        self._button_labels.set_enabled(True)

    def _create_record_modes(self):
        self._session_record = SessionRecordingComponent(name=u'Session_Record', is_enabled=False, layer=Layer(record_button=u'record_button'))
        self._record_modes = ModesComponent(name=u'Record_Modes')
        self._record_modes.add_mode(u'session', EnablingMode(self._session_record))
        self._record_modes.add_mode(u'arrange', AddLayerMode(self._transport, layer=Layer(record_button=u'record_button')))
        self.__on_main_view_changed()

    def _create_lower_pad_modes(self):
        self._lower_pad_modes = ModesComponent(name=u'Lower_Pad_Modes', is_enabled=False, layer=Layer(cycle_mode_button=u'minus_button'))
        self._lower_pad_modes.add_mode(u'select', AddLayerMode(self._mixer, Layer(track_select_buttons=u'lower_pads')), cycle_mode_button_color=u'Session.StopClipDisabled')
        self._lower_pad_modes.add_mode(u'stop', AddLayerMode(self._session, Layer(stop_track_clip_buttons=u'lower_pads')), cycle_mode_button_color=u'Session.StopClip')
        self._lower_pad_modes.selected_mode = u'select'

    def _create_main_modes(self):
        self._main_modes = ModesComponent(name=u'Main_Modes', is_enabled=False, layer=Layer(song_button=u'song_mode_button', instrument_button=u'instrument_mode_button', editor_button=u'editor_mode_button', user_button=u'user_mode_button'))
        device_params_mode = AddLayerMode(self._device_parameters, Layer(parameter_controls=u'encoders'))
        enable_lower_fw_functions = partial(self._elements.lower_firmware_toggle_switch.send_value, 1)
        disable_upper_fw_functions = partial(self._elements.upper_firmware_toggle_switch.send_value, 0)
        self._main_modes.add_mode(u'song', (partial(self._elements.lower_firmware_toggle_switch.send_value, 0),
         disable_upper_fw_functions,
         self._elements.display_buttons.reset,
         self._view_toggle,
         self._launch_and_stop,
         self._session,
         self._lower_pad_modes,
         AddLayerMode(self._session.scene(0), Layer(launch_button=u'plus_button')),
         AddLayerMode(self._mixer.selected_strip(), Layer(volume_control=u'encoders_raw[0]', pan_control=u'encoders_raw[1]', send_controls=self._elements.encoders.submatrix[2:, :], solo_button=u'display_buttons_raw[0]', mute_button=u'display_buttons_raw[1]', arm_button=u'display_buttons_raw[2]')),
         AddLayerMode(self._mixer, Layer(crossfader_control=u'touch_strip'))))
        self._main_modes.add_mode(u'instrument', (enable_lower_fw_functions, partial(self._elements.upper_firmware_toggle_switch.send_value, 1), device_params_mode))
        self._main_modes.add_mode(u'editor', (enable_lower_fw_functions,
         disable_upper_fw_functions,
         device_params_mode,
         self._device_navigation,
         AddLayerMode(self._device_parameters, Layer(device_lock_button=u'display_buttons_raw[0]', device_on_off_button=u'display_buttons_raw[3]', prev_bank_button=u'display_buttons_raw[4]', next_bank_button=u'display_buttons_raw[5]'))))
        self._main_modes.add_mode(u'user', (enable_lower_fw_functions, disable_upper_fw_functions, self._translating_background))
        self._main_modes.selected_mode = u'instrument'
        self._main_modes.set_enabled(True)
        self.__on_main_modes_changed.subject = self._main_modes

    @listens(u'selected_mode')
    def __on_main_modes_changed(self, mode):
        self._button_labels.show_button_labels_for_mode(mode)
        self._elements.track_name_display.clear_send_cache()
        self._elements.device_name_display.clear_send_cache()

    @listens(u'is_view_visible', u'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible(u'Session'):
            self._record_modes.selected_mode = u'session'
        else:
            self._record_modes.selected_mode = u'arrange'
