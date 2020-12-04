#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_mkII/keylab_mkii.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.base import listens
from ableton.v2.control_surface import Layer
from ableton.v2.control_surface.components import SessionRecordingComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement, PhysicalDisplayElement, SysexElement
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent
from KeyLab_Essential import sysex
from KeyLab_Essential.control_element_utils import create_button, create_pad_led
from KeyLab_Essential.keylab_essential import KeyLabEssential
from .channel_strip import ChannelStripComponent
from .hardware_settings import HardwareSettingsComponent
from .mixer import MixerComponent
from .session import SessionComponent
from .view_control import ViewControlComponent
PAD_IDS = ((36, 37, 38, 39, 44, 45, 46, 47), (40, 41, 42, 43, 48, 49, 50, 51))
PAD_LED_IDS = ((112, 113, 114, 115, 120, 121, 122, 123), (116, 117, 118, 119, 124, 125, 126, 127))
DISPLAY_LINE_WIDTH = 16

class KeyLabMkII(KeyLabEssential):
    mixer_component_type = MixerComponent
    session_component_type = SessionComponent
    view_control_component_type = ViewControlComponent
    hardware_settings_component_type = HardwareSettingsComponent
    channel_strip_component_type = ChannelStripComponent

    def __init__(self, *a, **k):
        super(KeyLabMkII, self).__init__(*a, **k)
        with self.component_guard():
            self._create_session_recording()

    def _create_controls(self):
        super(KeyLabMkII, self)._create_controls()

        def make_button_row(index_offset, name):
            return ButtonMatrixElement(rows=[[ create_button(index + index_offset, name=u'{}_{}'.format(name, index)) for index in range(8) ]], name=u'{}s'.format(name))

        self._select_buttons = make_button_row(24, u'Select_Button')
        self._solo_buttons = make_button_row(8, u'Solo_Button')
        self._mute_buttons = make_button_row(16, u'Mute_Button')
        self._record_arm_buttons = make_button_row(0, u'Record_Arm_Buttons')
        self._automation_button = create_button(56, name=u'Automation_Button')
        self._re_enable_automation_button = create_button(57, name=u'Re_Enable_Automation_Button')
        self._view_button = create_button(74, name=u'View_Button')
        self._pads = ButtonMatrixElement(rows=[ [ create_button(identifier, channel=9, name=u'Pad_{}_{}'.format(col_index, row_index)) for col_index, identifier in enumerate(row) ] for row_index, row in enumerate(PAD_IDS) ])
        self._pad_leds = ButtonMatrixElement(rows=[ [ create_pad_led(identifier, u'Pad_LED_{}_{}'.format(col_index, row_index)) for col_index, identifier in enumerate(row) ] for row_index, row in enumerate(PAD_LED_IDS) ], name=u'Pad_LED_Matrix')
        self._display = PhysicalDisplayElement(DISPLAY_LINE_WIDTH, name=u'Display')
        self._display.set_message_parts(sysex.LCD_SET_STRING_MESSAGE_HEADER + (sysex.LCD_LINE_1_ITEM_ID,), (sysex.NULL, sysex.LCD_LINE_2_ITEM_ID) + (ord(u' '),) * DISPLAY_LINE_WIDTH + (sysex.NULL, sysex.END_BYTE))
        self._mixer_mode_cycle_button = create_button(51, name=u'Mixer_Mode_Cycle_Button')
        self._vegas_mode_switch = SysexElement(send_message_generator=lambda b: sysex.VEGAS_MODE_MESSAGE_HEADER + (b, sysex.END_BYTE), name=u'Vegas_Mode_Switch')

    def _create_mixer(self):
        super(KeyLabMkII, self)._create_mixer()
        self._mixer.layer += Layer(track_select_buttons=self._select_buttons, solo_buttons=self._solo_buttons, mute_buttons=self._mute_buttons, arm_buttons=self._record_arm_buttons, selected_track_name_display=self._display)
        self._mixer_modes = ModesComponent(name=u'Mixer_Modes')
        self._mixer_modes.add_mode(u'volume_mode', AddLayerMode(self._mixer, Layer(volume_controls=self._faders)))
        self._mixer_modes.add_mode(u'sends_a_mode', AddLayerMode(self._mixer, Layer(send_controls=self._faders)))
        self._mixer_modes.layer = Layer(cycle_mode_button=self._mixer_mode_cycle_button)
        self._mixer_modes.selected_mode = u'volume_mode'

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(name=u'Session_Recording', is_enabled=False, layer=Layer(automation_button=self._automation_button, re_enable_automation_button=self._re_enable_automation_button))
        self._session_recording.set_enabled(True)

    def _create_view_control(self):
        super(KeyLabMkII, self)._create_view_control()
        self._view_control.layer += Layer(document_view_toggle_button=self._view_button)

    def _create_hardware_settings(self):
        super(KeyLabMkII, self)._create_hardware_settings()
        self._hardware_settings.layer += Layer(vegas_mode_switch=self._vegas_mode_switch)
