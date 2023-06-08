from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, nop
from ableton.v2.control_surface import Layer, SessionRingSelectionLinking
from ableton.v2.control_surface.components import AutoArmComponent, BackgroundComponent
from ableton.v2.control_surface.mode import AddLayerMode, LayerMode
from novation import sysex
from novation.instrument_control import InstrumentControlMixin
from novation.launchkey_drum_group import DrumGroupComponent
from novation.launchkey_elements import SESSION_HEIGHT
from novation.mode import ModesComponent
from novation.novation_base import NovationBase
from novation.simple_device import SimpleDeviceParameterComponent
from novation.transport import TransportComponent
from novation.view_control import NotifyingViewControlComponent
from . import midi
from . import sysex_ids as ids
from .elements import Elements
from .skin import skin
DRUM_FEEDBACK_CHANNEL = 1

class Launchkey_Mini_MK3(InstrumentControlMixin, NovationBase):
    model_family_code = ids.LK_MINI_MK3_FAMILY_CODE
    element_class = Elements
    session_height = SESSION_HEIGHT
    skin = skin
    suppress_layout_switch = False

    def __init__(self, *a, **k):
        self._last_pad_layout_byte = midi.PAD_SESSION_LAYOUT
        self._last_pot_layout_byte = midi.POT_VOLUME_LAYOUT
        (super(Launchkey_Mini_MK3, self).__init__)(*a, **k)

    def disconnect(self):
        self._elements.pad_layout_switch.send_value(midi.PAD_DRUM_LAYOUT)
        self._auto_arm.set_enabled(False)
        super(Launchkey_Mini_MK3, self).disconnect()

    def on_identified(self, midi_bytes):
        self._elements.incontrol_mode_switch.send_value(midi.INCONTROL_ONLINE_VALUE)
        self._elements.pad_layout_switch.send_value(self._last_pad_layout_byte)
        self._elements.pot_layout_switch.send_value(self._last_pot_layout_byte)
        self._target_track_changed()
        self._drum_group_changed()
        self._auto_arm.set_enabled(True)
        self.set_feedback_channels([DRUM_FEEDBACK_CHANNEL])
        super(Launchkey_Mini_MK3, self).on_identified(midi_bytes)

    def port_settings_changed(self):
        self._auto_arm.set_enabled(False)
        super(Launchkey_Mini_MK3, self).port_settings_changed()

    def _create_components(self):
        super(Launchkey_Mini_MK3, self)._create_components()
        self.register_slot(self._elements.incontrol_mode_switch, nop, 'value')
        self._background = BackgroundComponent(name='Background', add_nop_listeners=True)
        self._create_auto_arm()
        self._create_view_control()
        self._create_transport()
        self._create_device()
        self._create_drum_group()
        self._create_pot_modes()
        self._create_stop_solo_mute_modes()
        self._create_pad_modes()
        self._create_recording_modes()

    def _create_session_layer(self):
        return super(Launchkey_Mini_MK3, self)._create_session_layer() + Layer(scene_launch_buttons='scene_launch_buttons')

    def _create_session_navigation_layer(self):
        return Layer(up_button='scene_launch_button_with_shift',
          down_button='stop_solo_mute_button_with_shift')

    def _create_auto_arm(self):
        self._auto_arm = AutoArmComponent(name='Auto_Arm', is_enabled=False)

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
          capture_midi_button='record_button_with_shift'))
        self._transport.set_enabled(True)

    def _create_recording_modes(self):
        super(Launchkey_Mini_MK3, self)._create_recording_modes()
        self._recording_modes.add_mode('arrange', AddLayerMode(self._transport, Layer(record_button='record_button')))
        self._Launchkey_Mini_MK3__on_main_view_changed.subject = self.application.view
        self._select_recording_mode()

    def _create_device(self):
        self._device = SimpleDeviceParameterComponent(name='Device',
          is_enabled=False,
          layer=Layer(parameter_controls='pots'))

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(name='Drum_Group',
          is_enabled=False,
          translation_channel=DRUM_FEEDBACK_CHANNEL,
          layer=Layer(matrix='drum_pads',
          scroll_page_up_button='scene_launch_button_with_shift',
          scroll_page_down_button='stop_solo_mute_button_with_shift'))

    def _create_pot_modes(self):
        self._pot_modes = ModesComponent(name='Pot_Modes',
          is_enabled=False,
          layer=Layer(mode_selection_control='pot_layout_switch'))
        self._pot_modes.add_mode('custom', None)
        self._pot_modes.add_mode('volume', AddLayerMode(self._mixer, Layer(volume_controls='pots')))
        self._pot_modes.add_mode('device', self._device)
        self._pot_modes.add_mode('pan', AddLayerMode(self._mixer, Layer(pan_controls='pots')))
        self._pot_modes.add_mode('send_a', AddLayerMode(self._mixer, Layer(send_a_controls='pots')))
        self._pot_modes.add_mode('send_b', AddLayerMode(self._mixer, Layer(send_b_controls='pots')))
        self._pot_modes.selected_mode = 'volume'
        self._pot_modes.set_enabled(True)
        self._Launchkey_Mini_MK3__on_pot_mode_byte_changed.subject = self._pot_modes

    def _create_stop_solo_mute_modes(self):
        self._stop_solo_mute_modes = ModesComponent(name='Stop_Solo_Mute_Modes',
          is_enabled=False,
          support_momentary_mode_cycling=False)
        bottom_row = self._elements.clip_launch_matrix.submatrix[:, 1:]
        self._stop_solo_mute_modes.add_mode('launch',
          None, cycle_mode_button_color='Mode.Launch.On')
        self._stop_solo_mute_modes.add_mode('stop',
          (AddLayerMode(self._session, Layer(stop_track_clip_buttons=bottom_row))),
          cycle_mode_button_color='Session.StopClip')
        self._stop_solo_mute_modes.add_mode('solo',
          (AddLayerMode(self._mixer, Layer(solo_buttons=bottom_row))),
          cycle_mode_button_color='Mixer.SoloOn')
        self._stop_solo_mute_modes.add_mode('mute',
          (AddLayerMode(self._mixer, Layer(mute_buttons=bottom_row))),
          cycle_mode_button_color='Mixer.MuteOff')
        self._stop_solo_mute_modes.selected_mode = 'launch'
        self._stop_solo_mute_modes.set_enabled(True)

    def _create_pad_modes(self):
        self._pad_modes = ModesComponent(name='Pad_Modes',
          is_enabled=False,
          layer=Layer(mode_selection_control='pad_layout_switch'))
        bg_mode = AddLayerMode((self._background),
          layer=Layer(scene_launch_buttons='scene_launch_buttons'))
        self._pad_modes.add_mode('custom', bg_mode)
        self._pad_modes.add_mode('drum', (bg_mode, self._drum_group))
        self._pad_modes.add_mode('session', LayerMode((self._stop_solo_mute_modes),
          layer=Layer(cycle_mode_button=(self._elements.scene_launch_buttons_raw[1]))))
        self._pad_modes.selected_mode = 'session'
        self._pad_modes.set_enabled(True)
        self._Launchkey_Mini_MK3__on_pad_mode_changed.subject = self._pad_modes
        self._Launchkey_Mini_MK3__on_pad_mode_byte_changed.subject = self._pad_modes

    def _select_recording_mode(self):
        if self.application.view.is_view_visible('Session'):
            self._recording_modes.selected_mode = 'track' if self._pad_modes.selected_mode == 'drum' else 'session'
        else:
            self._recording_modes.selected_mode = 'arrange'

    @listens('is_view_visible', 'Session')
    def __on_main_view_changed(self):
        self._select_recording_mode()

    @listens('selected_mode')
    def __on_pad_mode_changed(self, mode):
        self._select_recording_mode()
        self._update_controlled_track()

    @listens('mode_byte')
    def __on_pad_mode_byte_changed(self, mode_byte):
        self._last_pad_layout_byte = mode_byte

    @listens('mode_byte')
    def __on_pot_mode_byte_changed(self, mode_byte):
        self._last_pot_layout_byte = mode_byte

    def _drum_group_changed(self):
        self._drum_group.set_drum_group_device(self._drum_group_finder.drum_group)

    def _is_instrument_mode(self):
        return self._pad_modes.selected_mode == 'drum'