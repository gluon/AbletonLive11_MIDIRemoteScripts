#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_Essential/keylab_essential.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from ableton.v2.base import const, inject, listens
from ableton.v2.control_surface import ControlSurface, Layer, MIDI_CC_TYPE, MIDI_PB_TYPE
from ableton.v2.control_surface.components import MixerComponent, SessionNavigationComponent, SessionRingComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement, EncoderElement, SliderElement, SysexElement
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent
from . import sysex
from .arrangement import ArrangementComponent
from .channel_strip import ChannelStripComponent
from .control_element_utils import create_button, create_pad_led, create_ringed_encoder
from .hardware_settings import HardwareSettingsComponent
from .skin_default import default_skin
from .transport import TransportComponent
from .session import SessionComponent
from .undo import UndoComponent
from .view_control import ViewControlComponent

class KeyLabEssential(ControlSurface):
    mixer_component_type = MixerComponent
    session_component_type = SessionComponent
    view_control_component_type = ViewControlComponent
    hardware_settings_component_type = HardwareSettingsComponent
    channel_strip_component_type = ChannelStripComponent

    def __init__(self, *a, **k):
        super(KeyLabEssential, self).__init__(*a, **k)
        with self.component_guard():
            with inject(skin=const(default_skin)).everywhere():
                self._create_controls()
            self._create_hardware_settings()
        self._on_focused_view_changed.subject = self.application.view
        self._hardware_settings.set_hardware_live_mode_enabled(True)
        self._on_memory_preset_changed_on_hardware.subject = self._hardware_settings
        self._hardware_settings.select_memory_preset(sysex.DAW_MEMORY_PRESET_INDEX)
        with self.component_guard():
            self._create_transport()
            self._create_undo()
            self._create_session()
            self._create_navigation()
            self._create_mixer()
            self._create_view_control()
            self._create_arrangement()
            self._create_jogwheel_modes()

    def port_settings_changed(self):
        super(KeyLabEssential, self).port_settings_changed()
        self._hardware_settings.set_hardware_live_mode_enabled(True)

    def _create_controls(self):
        self._hardware_live_mode_switch = SysexElement(send_message_generator=lambda b: sysex.LIVE_MODE_MESSAGE_HEADER + (b, sysex.END_BYTE), default_value=sysex.OFF_VALUE, name=u'Hardware_Live_Mode_Switch')
        self._memory_preset_switch = SysexElement(send_message_generator=lambda b: sysex.MEMORY_PRESET_SWITCH_MESSAGE_HEADER + (b, sysex.END_BYTE), sysex_identifier=sysex.MEMORY_PRESET_SWITCH_MESSAGE_HEADER, name=u'Memory_Preset_Switch')
        self._memory_preset_select_mode_switch = SysexElement(sysex_identifier=sysex.MEMORY_PRESET_SELECT_MODE_MESSAGE_HEADER, name=u'Memory_Preset_Select_Mode')
        self._play_button = create_button(94, u'Play_Button')
        self._stop_button = create_button(93, u'Stop_Button')
        self._punch_in_button = create_button(87, u'Punch_In_Button')
        self._punch_out_button = create_button(88, u'Punch_Out_Button')
        self._metronome_button = create_button(89, u'Metronome_Button')
        self._loop_button = create_button(86, u'Loop_Button')
        self._rwd_button = create_button(91, u'Rewind_Button')
        self._ff_button = create_button(92, u'Fast_Forward_Button')
        self._record_button = create_button(95, u'Record_Button')
        self._undo_button = create_button(81, u'Undo_Button')
        self._bank_left_button = create_button(46, u'Bank_Left_Button')
        self._bank_right_button = create_button(47, u'Bank_Right_Button')
        self._left_button = create_button(48, u'Left_Button')
        self._right_button = create_button(49, u'Right_Button')
        self._left_arrow_button = create_button(98, u'Left_Arrow_Button')
        self._right_arrow_button = create_button(99, u'Right_Arrow_Button')
        self._marker_button = create_button(84, u'Marker_Button')
        self._pads = ButtonMatrixElement(rows=[[ create_button(col + 36, u'Pad_%d' % (col,), channel=10) for col in range(8) ]], name=u'Pad_Matrix')
        self._pad_leds = ButtonMatrixElement(rows=[[ create_pad_led(column + 112, u'Pad_LED_%d' % (column,)) for column in range(8) ]], name=u'Pad_LED_Matrix')
        self._faders = ButtonMatrixElement(rows=[[ SliderElement(msg_type=MIDI_PB_TYPE, channel=index, identifier=None, name=u'Fader_%d' % (index,)) for index in range(8) ]], name=u'Faders')
        self._master_fader = SliderElement(MIDI_PB_TYPE, 8, identifier=None, name=u'Master_Fader')
        self._encoders = ButtonMatrixElement(rows=[[ create_ringed_encoder(index + 16, index + 48, u'Encoder_%d' % (index,)) for index in range(8) ]])
        self._jogwheel = EncoderElement(MIDI_CC_TYPE, 0, 60, Live.MidiMap.MapMode.relative_smooth_signed_bit, name=u'Jogwheel')

    def _create_hardware_settings(self):
        self._hardware_settings = self.hardware_settings_component_type(is_enabled=False, layer=Layer(hardware_live_mode_switch=self._hardware_live_mode_switch, memory_preset_switch=self._memory_preset_switch, memory_preset_select_mode_switch=self._memory_preset_select_mode_switch), name=u'Hardware_Settings')
        self._hardware_settings.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(is_enabled=False, layer=Layer(play_button=self._play_button, stop_button=self._stop_button, punch_in_button=self._punch_in_button, punch_out_button=self._punch_out_button, loop_button=self._loop_button, metronome_button=self._metronome_button, record_button=self._record_button))
        self._transport.set_seek_buttons(self._ff_button, self._rwd_button)
        self._transport.set_enabled(True)

    def _create_undo(self):
        self._undo = UndoComponent(is_enabled=False, layer=Layer(undo_button=self._undo_button))
        self._undo.set_enabled(True)

    def _create_session(self):
        self._session_ring = SessionRingComponent(num_tracks=self._pads.width(), num_scenes=self._pads.height(), name=u'Session_Ring')
        self._session_ring.set_enabled(False)
        self._session = self.session_component_type(session_ring=self._session_ring, name=u'Session', is_enabled=False, layer=Layer(clip_launch_buttons=self._pads, clip_slot_leds=self._pad_leds))
        self._session.set_enabled(True)

    def _create_navigation(self):
        self._session_navigation = SessionNavigationComponent(session_ring=self._session_ring, is_enabled=False, layer=Layer(page_left_button=self._bank_left_button, page_right_button=self._bank_right_button, left_button=self._left_button, right_button=self._right_button), name=u'Session_Navigation')
        self._session_navigation.set_enabled(True)

    def _create_mixer(self):
        self._mixer = self.mixer_component_type(tracks_provider=self._session_ring, channel_strip_component_type=self.channel_strip_component_type, is_enabled=False, layer=Layer(volume_controls=self._faders, pan_controls=self._encoders))
        self._mixer.master_strip().set_volume_control(self._master_fader)
        self._mixer.set_enabled(True)

    def _create_view_control(self):
        self._view_control = self.view_control_component_type(is_enabled=False, layer=Layer(prev_track_button=self._left_arrow_button, next_track_button=self._right_arrow_button, scene_scroll_encoder=self._jogwheel), name=u'View_Control')
        self._view_control.set_enabled(True)

    def _create_arrangement(self):
        self._arrangement = ArrangementComponent(is_enabled=False, layer=Layer(set_or_delete_cue_button=self._marker_button), name=u'Arrangement')
        self._arrangement.set_enabled(True)

    def _create_jogwheel_modes(self):
        self._jogwheel_modes = ModesComponent()
        self._jogwheel_modes.add_mode(u'Session', AddLayerMode(self._view_control, Layer(scene_scroll_encoder=self._jogwheel)))
        self._jogwheel_modes.add_mode(u'Arranger', AddLayerMode(self._arrangement, Layer(jump_encoder=self._jogwheel)))
        self._on_focused_view_changed()

    @listens(u'focused_document_view')
    def _on_focused_view_changed(self):
        view = self.application.view.focused_document_view
        if self._jogwheel_modes:
            self._jogwheel_modes.selected_mode = view

    @listens(u'daw_preset')
    def _on_memory_preset_changed_on_hardware(self, is_daw_preset_on):
        self._session.set_allow_update(is_daw_preset_on)
        if is_daw_preset_on:
            for control in self.controls:
                control.clear_send_cache()

        self._session.set_enabled(is_daw_preset_on)
