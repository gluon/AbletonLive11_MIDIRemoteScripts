#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_Mini_MK3/launchkey_mini_mk3.py
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
        super(Launchkey_Mini_MK3, self).__init__(*a, **k)

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
        self.register_slot(self._elements.incontrol_mode_switch, nop, u'value')
        self._background = BackgroundComponent(name=u'Background', add_nop_listeners=True)
        self._create_auto_arm()
        self._create_view_control()
        self._create_transport()
        self._create_recording_modes()
        self._create_device()
        self._create_drum_group()
        self._create_pot_modes()
        self._create_stop_solo_mute_modes()
        self._create_pad_modes()

    def _create_session_layer(self):
        return super(Launchkey_Mini_MK3, self)._create_session_layer() + Layer(scene_launch_buttons=u'scene_launch_buttons')

    def _create_session_navigation_layer(self):
        return Layer(up_button=u'scene_launch_button_with_shift', down_button=u'stop_solo_mute_button_with_shift')

    def _create_auto_arm(self):
        self._auto_arm = AutoArmComponent(name=u'Auto_Arm', is_enabled=False)

    def _create_view_control(self):
        self._view_control = NotifyingViewControlComponent(name=u'Track_Scroller', is_enabled=False, track_provider=self._session_ring, layer=Layer(prev_track_button=u'left_button', next_track_button=u'right_button'))
        self._view_control.set_enabled(True)
        self._session_ring_selection_linking = self.register_disconnectable(SessionRingSelectionLinking(session_ring=self._session_ring, selection_changed_notifier=self._view_control))

    def _create_transport(self):
        self._transport = TransportComponent(name=u'Transport', is_enabled=False, layer=Layer(play_button=u'play_button', continue_playing_button=u'play_button_with_shift', capture_midi_button=u'record_button_with_shift'))
        self._transport.set_enabled(True)

    def _create_device(self):
        self._device = SimpleDeviceParameterComponent(name=u'Device', is_enabled=False, layer=Layer(parameter_controls=u'pots'))

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(name=u'Drum_Group', is_enabled=False, translation_channel=DRUM_FEEDBACK_CHANNEL, layer=Layer(matrix=u'drum_pads', scroll_page_up_button=u'scene_launch_button_with_shift', scroll_page_down_button=u'stop_solo_mute_button_with_shift'))

    def _create_pot_modes(self):
        self._pot_modes = ModesComponent(name=u'Pot_Modes', is_enabled=False, layer=Layer(mode_selection_control=u'pot_layout_switch'))
        self._pot_modes.add_mode(u'custom', None)
        self._pot_modes.add_mode(u'volume', AddLayerMode(self._mixer, Layer(volume_controls=u'pots')))
        self._pot_modes.add_mode(u'device', self._device)
        self._pot_modes.add_mode(u'pan', AddLayerMode(self._mixer, Layer(pan_controls=u'pots')))
        self._pot_modes.add_mode(u'send_a', AddLayerMode(self._mixer, Layer(send_a_controls=u'pots')))
        self._pot_modes.add_mode(u'send_b', AddLayerMode(self._mixer, Layer(send_b_controls=u'pots')))
        self._pot_modes.selected_mode = u'volume'
        self._pot_modes.set_enabled(True)
        self.__on_pot_mode_byte_changed.subject = self._pot_modes

    def _create_stop_solo_mute_modes(self):
        self._stop_solo_mute_modes = ModesComponent(name=u'Stop_Solo_Mute_Modes', is_enabled=False, support_momentary_mode_cycling=False)
        bottom_row = self._elements.clip_launch_matrix.submatrix[:, 1:]
        self._stop_solo_mute_modes.add_mode(u'launch', None, cycle_mode_button_color=u'Mode.Launch.On')
        self._stop_solo_mute_modes.add_mode(u'stop', AddLayerMode(self._session, Layer(stop_track_clip_buttons=bottom_row)), cycle_mode_button_color=u'Session.StopClip')
        self._stop_solo_mute_modes.add_mode(u'solo', AddLayerMode(self._mixer, Layer(solo_buttons=bottom_row)), cycle_mode_button_color=u'Mixer.SoloOn')
        self._stop_solo_mute_modes.add_mode(u'mute', AddLayerMode(self._mixer, Layer(mute_buttons=bottom_row)), cycle_mode_button_color=u'Mixer.MuteOff')
        self._stop_solo_mute_modes.selected_mode = u'launch'
        self._stop_solo_mute_modes.set_enabled(True)

    def _create_pad_modes(self):
        self._pad_modes = ModesComponent(name=u'Pad_Modes', is_enabled=False, layer=Layer(mode_selection_control=u'pad_layout_switch'))
        bg_mode = AddLayerMode(self._background, layer=Layer(scene_launch_buttons=u'scene_launch_buttons'))
        self._pad_modes.add_mode(u'custom', bg_mode)
        self._pad_modes.add_mode(u'drum', (bg_mode, self._drum_group))
        self._pad_modes.add_mode(u'session', LayerMode(self._stop_solo_mute_modes, layer=Layer(cycle_mode_button=self._elements.scene_launch_buttons_raw[1])))
        self._pad_modes.selected_mode = u'session'
        self._pad_modes.set_enabled(True)
        self.__on_pad_mode_changed.subject = self._pad_modes
        self.__on_pad_mode_byte_changed.subject = self._pad_modes

    @listens(u'selected_mode')
    def __on_pad_mode_changed(self, mode):
        self._recording_modes.selected_mode = u'track' if mode == u'drum' else u'session'
        self._update_controlled_track()

    @listens(u'mode_byte')
    def __on_pad_mode_byte_changed(self, mode_byte):
        self._last_pad_layout_byte = mode_byte

    @listens(u'mode_byte')
    def __on_pot_mode_byte_changed(self, mode_byte):
        self._last_pot_layout_byte = mode_byte

    def _drum_group_changed(self):
        self._drum_group.set_drum_group_device(self._drum_group_finder.drum_group)

    def _is_instrument_mode(self):
        return self._pad_modes.selected_mode == u'drum'
