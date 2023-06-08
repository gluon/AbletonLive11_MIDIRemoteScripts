from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import listens, nop
from ableton.v2.control_surface import Layer, SessionRingSelectionLinking
from ableton.v2.control_surface.components import AutoArmComponent, BackgroundComponent, UndoRedoComponent
from ableton.v2.control_surface.mode import AddLayerMode, LayerMode
from novation import sysex
from novation.instrument_control import InstrumentControlMixin
from novation.launchkey_drum_group import DrumGroupComponent
from novation.launchkey_elements import SESSION_HEIGHT
from novation.mode import ModesComponent
from novation.novation_base import NovationBase
from novation.quantization import QuantizationComponent
from novation.view_control import NotifyingViewControlComponent
from . import midi
from .channel_strip import ChannelStripComponent
from .clip_actions import ClipActionsComponent
from .device import DeviceComponent
from .elements import Elements
from .mixer import MixerComponent
from .notification import NotificationComponent
from .skin import skin
from .transport import TransportComponent
DRUM_FEEDBACK_CHANNEL = 1

class Launchkey_MK3(InstrumentControlMixin, NovationBase):
    element_class = Elements
    session_height = SESSION_HEIGHT
    mixer_class = MixerComponent
    channel_strip_class = ChannelStripComponent
    skin = skin
    suppress_layout_switch = False

    def __init__(self, *a, **k):
        self._is_small_model = False
        self._is_88_key_model = False
        self._last_pad_layout_byte = midi.PAD_SESSION_LAYOUT
        self._last_pot_layout_byte = None
        self._last_fader_layout_byte = midi.VOLUME_LAYOUT
        (super(Launchkey_MK3, self).__init__)(*a, **k)

    def disconnect(self):
        self._elements.pad_layout_switch.send_value(midi.PAD_DRUM_LAYOUT)
        self._auto_arm.set_enabled(False)
        super(Launchkey_MK3, self).disconnect()

    def on_identified(self, midi_bytes):
        if self._last_pot_layout_byte is None:
            self._last_pot_layout_byte = midi.VOLUME_LAYOUT if self._is_small_model else midi.PAN_LAYOUT
            self._pot_modes.selected_mode = 'volume' if self._is_small_model else 'pan'
        self._elements.incontrol_mode_switch.send_value(midi.INCONTROL_ONLINE_VALUE)
        self._elements.pad_layout_switch.send_value(self._last_pad_layout_byte)
        self._elements.pot_layout_switch.send_value(self._last_pot_layout_byte)
        if not self._is_small_model:
            self._elements.fader_layout_switch.send_value(self._last_fader_layout_byte)
        self._target_track_changed()
        self._drum_group_changed()
        self._auto_arm.set_enabled(True)
        self.set_feedback_channels([DRUM_FEEDBACK_CHANNEL])
        super(Launchkey_MK3, self).on_identified(midi_bytes)

    def port_settings_changed(self):
        self._auto_arm.set_enabled(False)
        super(Launchkey_MK3, self).port_settings_changed()

    def _create_components(self):
        super(Launchkey_MK3, self)._create_components()
        self.register_slot(self._elements.incontrol_mode_switch, nop, 'value')
        self._create_auto_arm()
        self._create_background()
        self._create_notification()
        self._create_view_control()
        self._create_transport()
        self._create_undo()
        self._create_quantization()
        self._create_device()
        self._create_drum_group()
        self._pot_modes = self._create_pot_or_fader_modes('pot')
        self._create_stop_solo_mute_modes()
        self._create_pad_modes()
        self._create_recording_modes()
        if not self._is_small_model:
            self._fader_modes = self._create_pot_or_fader_modes('fader')
            self._setup_master_fader()
            self._create_fader_button_modes()

    def _setup_master_fader(self):
        strip = self._mixer.master_strip()
        strip.set_volume_control(self._elements.master_fader)
        strip.volume_display.set_control_element(self._elements.master_fader_parameter_value_display)
        self._elements.master_fader_parameter_name_display.display_message('Master Volume')

    def _create_session_navigation_layer(self):
        return Layer(up_button='up_button', down_button='down_button')

    def _create_session_layer(self):
        return super(Launchkey_MK3, self)._create_session_layer() + Layer(scene_launch_buttons='scene_launch_buttons')

    def _create_auto_arm(self):
        self._auto_arm = AutoArmComponent(name='Auto_Arm', is_enabled=False)

    def _create_background(self):
        self._background = BackgroundComponent(name='Background',
          is_enabled=False,
          add_nop_listeners=True,
          layer=Layer(secondary_up_button='secondary_up_button',
          secondary_down_button='secondary_down_button',
          device_select_button='device_select_button',
          unused_matrix=(self._elements.device_select_matrix.submatrix[:, 1:]),
          pot_parameter_name_displays='pot_parameter_name_displays',
          pot_parameter_value_displays='pot_parameter_value_displays',
          fader_parameter_name_displays='fader_parameter_name_displays',
          fader_parameter_value_displays='fader_parameter_value_displays'))
        self._background.set_enabled(True)

    def _create_notification(self):
        self._notification_component = NotificationComponent(name='Notifications',
          is_enabled=False,
          layer=Layer(display_lines='notification_display'))
        self._notification_component.set_enabled(True)

    def _create_view_control(self):
        self._view_control = NotifyingViewControlComponent(name='Track_Scroller',
          is_enabled=False,
          track_provider=(self._session_ring),
          layer=Layer(prev_track_button='left_button',
          next_track_button='right_button'))
        self._view_control.set_enabled(True)
        self._session_ring_selection_linking = self.register_disconnectable(SessionRingSelectionLinking(session_ring=(self._session_ring),
          selection_changed_notifier=(self._view_control)))

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(play_button='play_button',
          continue_playing_button='play_button_with_shift',
          alt_stop_button='stop_button',
          loop_button='loop_button',
          metronome_button='click_button',
          capture_midi_button='capture_midi_button'))
        self._transport.set_enabled(True)

    def _create_recording_modes(self):
        super(Launchkey_MK3, self)._create_recording_modes()
        self._recording_modes.add_mode('arrange', AddLayerMode(self._transport, Layer(record_button='record_button')))
        self._Launchkey_MK3__on_main_view_changed.subject = self.application.view
        self._select_recording_mode()

    def _create_undo(self):
        self._undo = UndoRedoComponent(name='Undo',
          is_enabled=False,
          layer=Layer(undo_button='undo_button'))
        self._undo.set_enabled(True)

    def _create_quantization(self):
        self._quantization = QuantizationComponent(name='Quantization')
        self._clip_actions = ClipActionsComponent(name='Clip_Actions',
          quantization_component=(self._quantization),
          is_enabled=False,
          layer=Layer(quantize_button='quantize_button'))
        self._clip_actions.set_enabled(True)

    def _create_device(self):
        self._device = DeviceComponent(name='Device',
          is_enabled=False,
          show_notification=(self._notification_component.show_notification),
          device_bank_registry=(self._device_bank_registry),
          toggle_lock=(self.toggle_lock),
          use_parameter_banks=True,
          layer=Layer(device_lock_button='device_lock_button'))
        self._device.set_enabled(True)

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(name='Drum_Group',
          is_enabled=False,
          translation_channel=DRUM_FEEDBACK_CHANNEL,
          layer=Layer(matrix='drum_pads',
          scroll_page_up_button='up_button',
          scroll_page_down_button='down_button'))

    def _create_pot_or_fader_modes(self, modes_type_name):
        modes = ModesComponent(name=('{}_Modes'.format(modes_type_name.title())),
          is_enabled=False,
          layer=Layer(mode_selection_control=('{}_layout_switch'.format(modes_type_name))))
        elements_name = '{}s'.format(modes_type_name)
        name_displays_element_name = '{}_parameter_name_displays'.format(modes_type_name)
        value_displays_element_name = '{}_parameter_value_displays'.format(modes_type_name)

        def add_pot_or_fader_mixer_mode(parameter_name):
            modes.add_mode(parameter_name, (
             partial(getattr(self._mixer, 'set_{}_parameter_name'.format(modes_type_name)), parameter_name.replace('_', ' ').title()),
             AddLayerMode(self._mixer, Layer(**{'{}_controls'.format(parameter_name): elements_name, 
              '{}_parameter_name_displays'.format(modes_type_name): name_displays_element_name, 
              
              '{}_displays'.format(parameter_name): value_displays_element_name}))))

        modes.add_mode('dummy', None)
        add_pot_or_fader_mixer_mode('volume')
        modes.add_mode('device', AddLayerMode(self._device, Layer(parameter_controls=elements_name,
          parameter_name_displays=name_displays_element_name,
          parameter_value_displays=value_displays_element_name)))
        if modes_type_name == 'pot':
            add_pot_or_fader_mixer_mode('pan')
        else:
            modes.add_mode('pan', None)
        add_pot_or_fader_mixer_mode('send_a')
        add_pot_or_fader_mixer_mode('send_b')
        for i in range(4):
            modes.add_mode('custom{}'.format(i), None)

        modes.selected_mode = 'pan' if modes_type_name == 'pot' else 'volume'
        modes.set_enabled(True)
        self.register_slot(modes, getattr(self, '_on_{}_mode_byte_changed'.format(modes_type_name)), 'mode_byte')
        return modes

    def _create_fader_button_modes(self):
        self._fader_button_modes = ModesComponent(name='Fader_Modes',
          is_enabled=False,
          support_momentary_mode_cycling=False,
          layer=Layer(cycle_mode_button='fader_button_modes_button'))
        self._fader_button_modes.add_mode('arm',
          (AddLayerMode(self._mixer, Layer(arm_buttons='fader_buttons'))),
          cycle_mode_button_color='DefaultButton.Off')
        self._fader_button_modes.add_mode('track_select',
          (AddLayerMode(self._mixer, Layer(track_select_buttons='fader_buttons'))),
          cycle_mode_button_color='DefaultButton.On')
        self._fader_button_modes.selected_mode = 'arm'
        self._fader_button_modes.set_enabled(True)

    def _create_stop_solo_mute_modes(self):
        self._stop_solo_mute_modes = ModesComponent(name='Stop_Solo_Mute_Modes',
          is_enabled=False,
          support_momentary_mode_cycling=False)
        lower_matrix_row = self._elements.clip_launch_matrix.submatrix[:, 1:]
        self._stop_solo_mute_modes.add_mode('launch',
          None, cycle_mode_button_color='Mode.Launch.On')
        self._stop_solo_mute_modes.add_mode('stop',
          (AddLayerMode(self._session, Layer(stop_track_clip_buttons=lower_matrix_row))),
          cycle_mode_button_color='Session.StopClip')
        self._stop_solo_mute_modes.add_mode('solo',
          (AddLayerMode(self._mixer, Layer(solo_buttons=lower_matrix_row))),
          cycle_mode_button_color='Mixer.SoloOn')
        self._stop_solo_mute_modes.add_mode('mute',
          (AddLayerMode(self._mixer, Layer(mute_buttons=lower_matrix_row))),
          cycle_mode_button_color='Mixer.MuteOff')
        self._stop_solo_mute_modes.selected_mode = 'launch'
        self._stop_solo_mute_modes.set_enabled(True)
        self._Launchkey_MK3__on_stop_solo_mute_mode_changed.subject = self._stop_solo_mute_modes

    def _create_pad_modes(self):
        self._pad_modes = ModesComponent(name='Pad_Modes',
          is_enabled=False,
          layer=Layer(mode_selection_control='pad_layout_switch'))
        suppress_scene_launch_buttons = AddLayerMode((self._background),
          layer=Layer(scene_launch_buttons='scene_launch_buttons'))
        suppress_all_buttons_around_pads = AddLayerMode((self._background),
          layer=Layer(scene_launch_buttons='scene_launch_buttons',
          up_button='up_button',
          down_button='down_button'))
        self._pad_modes.add_mode('dummy', suppress_all_buttons_around_pads)
        self._pad_modes.add_mode('drum', (suppress_scene_launch_buttons, self._drum_group))
        self._pad_modes.add_mode('session', LayerMode((self._stop_solo_mute_modes),
          layer=Layer(cycle_mode_button=(self._elements.scene_launch_buttons_raw[1]))))
        for i in range(6):
            self._pad_modes.add_mode('custom{}'.format(i), suppress_all_buttons_around_pads)

        upper_matrix_row = self._elements.device_select_matrix.submatrix[:, :1]
        self._pad_modes.add_mode('device_select', (
         suppress_scene_launch_buttons,
         self._device.show_device_name_and_bank,
         AddLayerMode((self._device),
           layer=Layer(bank_select_buttons=upper_matrix_row,
           prev_button='up_button',
           next_button='down_button'))))
        self._pad_modes.selected_mode = 'session'
        self._pad_modes.set_enabled(True)
        self._Launchkey_MK3__on_pad_mode_changed.subject = self._pad_modes
        self._Launchkey_MK3__on_pad_mode_byte_changed.subject = self._pad_modes

    def _select_recording_mode(self):
        if self.application.view.is_view_visible('Session'):
            self._recording_modes.selected_mode = 'track' if self._pad_modes.selected_mode == 'drum' else 'session'
        else:
            self._recording_modes.selected_mode = 'arrange'

    @listens('is_view_visible', 'Session')
    def __on_main_view_changed(self):
        self._select_recording_mode()

    @listens('selected_mode')
    def __on_pad_mode_changed(self, _):
        self._select_recording_mode()
        self._update_controlled_track()

    @listens('selected_mode')
    def __on_stop_solo_mute_mode_changed(self, mode):
        if mode:
            self._notification_component.show_notification('Lower Pad Mode', mode.title())

    @listens('mode_byte')
    def __on_pad_mode_byte_changed(self, mode_byte):
        self._last_pad_layout_byte = mode_byte

    def _on_pot_mode_byte_changed(self, mode_byte):
        self._last_pot_layout_byte = mode_byte

    def _on_fader_mode_byte_changed(self, mode_byte):
        self._last_fader_layout_byte = mode_byte

    def _drum_group_changed(self):
        self._drum_group.set_drum_group_device(self._drum_group_finder.drum_group)

    def _target_track_changed(self):
        super(Launchkey_MK3, self)._target_track_changed()
        self._notification_component.show_notification('Track', self._target_track.target_track.name)

    def _is_instrument_mode(self):
        return self._pad_modes.selected_mode == 'drum'

    def _extract_product_id_bytes(self, midi_bytes):
        id_bytes = super(Launchkey_MK3, self)._extract_product_id_bytes(midi_bytes)
        model_id_byte = id_bytes[3]
        self._elements.init_display_elements(model_id_byte == midi.LK_MK3_88_ID_BYTE)
        if id_bytes[:3] == sysex.NOVATION_MANUFACTURER_ID:
            if model_id_byte in midi.MODEL_ID_BYTES:
                if id_bytes[4:] == midi.MODEL_ID_BYTE_SUFFIX:
                    self._is_small_model = model_id_byte in midi.SMALL_MODEL_ID_BYTES
                    self._product_id_bytes = sysex.NOVATION_MANUFACTURER_ID + id_bytes[3:]
        return id_bytes