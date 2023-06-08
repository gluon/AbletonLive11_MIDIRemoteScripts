from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from _Komplete_Kontrol.control_element_util import create_slider_element
from _Komplete_Kontrol.komplete_kontrol_base import NUM_TRACKS, ButtonMatrixElement, KompleteKontrolBase, Layer, create_button, create_encoder, create_sysex_element, sysex
from .channel_strip_component import ChannelStripComponent
from .meter_display_element import MeterDisplayElement
from .mixer_component import MixerComponent
from .session_ring_navigation_component import SessionRingNavigationComponent
from .view_control_component import ViewControlComponent

class Komplete_Kontrol_S_Mk2(KompleteKontrolBase):
    mixer_component_class = MixerComponent
    channel_strip_component_class = ChannelStripComponent
    is_s_mk2 = True

    def _create_controls(self):
        super(Komplete_Kontrol_S_Mk2, self)._create_controls()
        self._selected_track_mute_button = create_button(102, 'Selected_Track_Mute_Button')
        self._selected_track_solo_button = create_button(103, 'Selected_Track_Solo_Button')
        self._selected_track_type_button = create_button(104, 'Selected_Track_Type_Button')
        self._selected_track_muted_via_solo_button = create_button(105, 'Selected_Track_Muted_via_Solo_Button')
        self._track_encoder = create_encoder(48, 'Track_Encoder')
        self._bank_encoder = create_encoder(49, 'Bank_Encoder')
        self._scene_encoder = create_encoder(50, 'Scene_Encoder')
        self._selected_track_volume_encoder = create_encoder(100,
          'Selected_Track_Volume_Encoder', is_s_mk2=True)
        self._selected_track_pan_encoder = create_encoder(101,
          'Selected_Track_Pan_Encoder', is_s_mk2=True)
        self._selection_control = create_slider_element(66, 'Selection_Control')
        self._mute_control = create_slider_element(67, 'Mute_Control')
        self._solo_control = create_slider_element(68, 'Solo_Control')
        self._track_arm_displays = ButtonMatrixElement(rows=[
         [create_sysex_element(sysex.TRACK_ARM_DISPLAY_HEADER, index, 'Track_Arm_Display_{}'.format(index)) for index in range(NUM_TRACKS)]],
          name='Track_Arm_Displays')
        self._track_meter_display = MeterDisplayElement((sysex.TRACK_METER_DISPLAY_HEADER),
          NUM_TRACKS, name='Track_Meter_Display')

    def _create_components(self):
        super(Komplete_Kontrol_S_Mk2, self)._create_components()
        self._create_session_ring_navigation()
        self._create_view_control()

    def _create_session_ring_navigation(self):
        self._session_ring_navigation = SessionRingNavigationComponent((self._session_ring),
          name='Session_Ring_Navigation',
          is_enabled=False,
          layer=Layer(navigation_encoder=(self._bank_encoder)))

    def _create_view_control(self):
        self._view_control = ViewControlComponent(name='View_Control',
          is_enabled=False,
          layer=Layer(track_encoder=(self._track_encoder),
          scene_encoder=(self._scene_encoder)))

    def _create_mixer_component_layer(self):
        return super(Komplete_Kontrol_S_Mk2, self)._create_mixer_component_layer() + Layer(mute_button=(self._selected_track_mute_button),
          solo_button=(self._selected_track_solo_button),
          selected_track_volume_control=(self._selected_track_volume_encoder),
          selected_track_pan_control=(self._selected_track_pan_encoder),
          selected_track_type_display=(self._selected_track_type_button),
          selected_track_muted_via_solo_display=(self._selected_track_muted_via_solo_button),
          selection_control=(self._selection_control),
          mute_control=(self._mute_control),
          solo_control=(self._solo_control),
          track_meter_display=(self._track_meter_display),
          track_arm_displays=(self._track_arm_displays))