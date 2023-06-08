from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, inject, listens
from ableton.v2.control_surface import IdentifiableControlSurface, Layer
from ableton.v2.control_surface.components import BackgroundComponent, MixerComponent, SessionRecordingComponent, SessionRingComponent, SimpleTrackAssigner, TransportComponent, UndoRedoComponent
from ableton.v2.control_surface.mode import AddLayerMode, EnablingMode, ImmediateBehaviour, ModesComponent
from novation.simple_device import SimpleDeviceParameterComponent
from . import midi
from .channel_strip import ChannelStripComponent
from .elements import Elements
from .mode import ReenterBehaviour
from .session import SessionComponent
from .session_navigation import SessionNavigationComponent

class Oxygen_Pro(IdentifiableControlSurface):
    session_height = 2
    session_width = 8
    live_mode_byte = midi.LIVE_MODE_BYTE
    pad_ids = ((40, 41, 42, 43, 48, 49, 50, 51), (36, 37, 38, 39, 44, 45, 46, 47))
    device_parameter_component = SimpleDeviceParameterComponent
    has_session_component = True

    def __init__(self, *a, **k):
        (super(Oxygen_Pro, self).__init__)(a, product_id_bytes=midi.M_AUDIO_MANUFACTURER_ID + (0, ), **k)
        self._last_selected_knob_mode = 'device'
        with self.component_guard():
            self._elements = Elements(self.session_height, self.session_width, self.pad_ids)
            with inject(element_container=(const(self._elements))).everywhere():
                self._create_background()
                self._create_transport()
                self._create_undo_redo()
                self._create_session()
                self._create_mixer()
                self._create_device_parameters()
                self._create_record_modes()
                self._create_button_modes()
                self._create_knob_modes()
                self._create_takeover_modes()
        self._Oxygen_Pro__on_main_view_changed.subject = self.application.view

    def on_identified(self, response_bytes):
        self._elements.firmware_mode_switch.send_value(self.live_mode_byte)
        self._elements.control_mode_switch.send_value(midi.RECORD_MODE_BYTE)
        self._elements.control_mode_switch.send_value(midi.DEVICE_MODE_BYTE)
        self._elements.led_control_switch.send_value(midi.LED_ENABLE_BYTE)
        self._elements.led_mode_switch.send_value(midi.SOFTWARE_CONTROL_BYTE)
        self._button_modes.selected_mode = 'arm'
        self._knob_modes.selected_mode = 'device'
        if self.has_session_component:
            self._session_ring.set_enabled(True)
        super(Oxygen_Pro, self).on_identified(response_bytes)

    def port_settings_changed(self):
        if self.has_session_component:
            self._session_ring.set_enabled(False)
        super(Oxygen_Pro, self).port_settings_changed()

    def _create_background(self):
        self._background = BackgroundComponent(name='Background',
          is_enabled=False,
          add_nop_listeners=True,
          layer=Layer(shift_button='shift_button'))
        self._background.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(loop_button='loop_button',
          stop_button='stop_button',
          play_button='play_button',
          metronome_button='metronome_button',
          seek_forward_button='fastforward_button',
          seek_backward_button='rewind_button'))
        self._transport.set_enabled(True)

    def _create_undo_redo(self):
        self._undo_redo = UndoRedoComponent(name='Undo_Redo',
          is_enabled=False,
          layer=Layer(undo_button='back_button'))
        self._undo_redo.set_enabled(True)

    def _create_session(self):
        self._session_ring = SessionRingComponent(name='Session_Ring',
          is_enabled=False,
          num_tracks=(self.session_width),
          num_scenes=(self.session_height))
        if self.has_session_component:
            self._session = SessionComponent(name='Session',
              is_enabled=False,
              session_ring=(self._session_ring),
              layer=Layer(clip_launch_buttons='pads',
              scene_launch_buttons='scene_launch_buttons',
              selected_scene_launch_button='encoder_push_button',
              scene_encoder='encoder_with_encoder_push'))
            self._session.set_enabled(True)
        self._session_navigation = SessionNavigationComponent(name='Session_Navigation',
          is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(left_button='bank_left_button',
          right_button='bank_right_button',
          scene_encoder='encoder'))
        self._session_navigation.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(name='Mixer',
          is_enabled=False,
          auto_name=True,
          channel_strip_component_type=ChannelStripComponent,
          tracks_provider=(self._session_ring),
          track_assigner=(SimpleTrackAssigner()),
          layer=Layer(volume_controls='faders'))
        self._mixer.master_strip().set_volume_control(self._elements.master_fader)
        self._mixer.set_enabled(True)

    def _create_device_parameters(self):
        self._device_parameters = self.device_parameter_component(name='Device_Parameters',
          is_enabled=False,
          layer=Layer(parameter_controls='knobs'))

    def _create_record_modes(self):
        self._session_record = SessionRecordingComponent(name='Session_Record',
          is_enabled=False,
          layer=Layer(record_button='record_button'))
        self._record_modes = ModesComponent(name='Record_Modes')
        self._record_modes.add_mode('session', EnablingMode(self._session_record))
        self._record_modes.add_mode('arrange', AddLayerMode((self._transport), layer=Layer(record_button='record_button')))
        self._Oxygen_Pro__on_main_view_changed()

    def _create_button_modes(self):
        self._button_modes = ModesComponent(name='Button_Modes',
          is_enabled=False,
          layer=Layer(off_button='off_mode_button',
          arm_button='arm_mode_button',
          track_select_button='track_select_mode_button',
          mute_button='mute_mode_button',
          solo_button='solo_mode_button'))
        self._button_modes.add_mode('off', None, behaviour=(ImmediateBehaviour()))
        self._button_modes.add_mode('arm',
          AddLayerMode((self._mixer), layer=Layer(arm_buttons='fader_buttons')),
          behaviour=(ImmediateBehaviour()))
        self._button_modes.add_mode('track_select',
          AddLayerMode((self._mixer), layer=Layer(track_select_buttons='fader_buttons')),
          behaviour=(ImmediateBehaviour()))
        self._button_modes.add_mode('mute',
          AddLayerMode((self._mixer), layer=Layer(mute_buttons='fader_buttons')),
          behaviour=(ImmediateBehaviour()))
        self._button_modes.add_mode('solo',
          AddLayerMode((self._mixer), layer=Layer(solo_buttons='fader_buttons')),
          behaviour=(ImmediateBehaviour()))
        self._button_modes.selected_mode = 'arm'
        self._button_modes.set_enabled(True)

    def _create_knob_modes(self):
        self._knob_modes = ModesComponent(name='Knob_Modes',
          is_enabled=False,
          layer=Layer(volume_button='volume_mode_button',
          pan_button='pan_mode_button',
          sends_button='sends_mode_button',
          device_button='device_mode_button'))
        self._knob_modes.add_mode('volume',
          AddLayerMode((self._mixer), layer=Layer(volume_controls='knobs')),
          behaviour=(ImmediateBehaviour()))
        self._knob_modes.add_mode('pan',
          AddLayerMode((self._mixer), layer=Layer(pan_controls='knobs')),
          behaviour=(ImmediateBehaviour()))
        self._knob_modes.add_mode('sends',
          AddLayerMode((self._mixer), layer=Layer(send_controls='knobs')),
          behaviour=ReenterBehaviour(on_reenter=(self._on_reenter_sends_mode)))
        self._knob_modes.add_mode('device',
          (self._device_parameters), behaviour=(self._get_device_mode_behaviour()))
        self._knob_modes.add_mode('takeover', None)
        self._knob_modes.selected_mode = 'device'
        self._Oxygen_Pro__on_knob_mode_changed.subject = self._knob_modes
        self._knob_modes.set_enabled(True)

    def _get_device_mode_behaviour(self):
        return ImmediateBehaviour()

    def _on_reenter_sends_mode(self):
        new_send_index = 1 if self._mixer.send_index == 0 else 0
        if new_send_index in range(self._mixer.num_sends):
            self._mixer.send_index = new_send_index

    def _create_takeover_modes(self):
        self._takeover_modes = ModesComponent(name='Takeover_Modes',
          is_enabled=False,
          layer=Layer(daw_button='daw_mode_button', preset_button='preset_mode_button'))
        self._takeover_modes.add_mode('daw', self._select_knob_mode)
        self._takeover_modes.add_mode('preset', (
         self._select_knob_mode,
         AddLayerMode((self._background),
           layer=Layer(faders='faders', knobs='knobs'))))
        self._takeover_modes.selected_mode = 'daw'
        self._takeover_modes.set_enabled(True)

    def _select_knob_mode(self):
        if self._takeover_modes.selected_mode == 'daw':
            self._knob_modes.selected_mode = self._last_selected_knob_mode
        else:
            self._knob_modes.selected_mode = 'takeover'

    @listens('selected_mode')
    def __on_knob_mode_changed(self, mode):
        if mode != 'takeover':
            self._last_selected_knob_mode = mode

    @listens('is_view_visible', 'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible('Session'):
            self._record_modes.selected_mode = 'session'
        else:
            self._record_modes.selected_mode = 'arrange'