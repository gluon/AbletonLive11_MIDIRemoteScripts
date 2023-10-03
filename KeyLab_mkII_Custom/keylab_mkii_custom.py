<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_mkII/keylab_mkii.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 8529 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from functools import partial
from ableton.v2.base import listens
from ableton.v2.control_surface import MIDI_NOTE_TYPE, Layer
from ableton.v2.control_surface.components import SessionRecordingComponent
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, PhysicalDisplayElement, SysexElement
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent
from novation.simple_device import SimpleDeviceParameterComponent
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
<<<<<<< HEAD
ENCODER_MODE_TO_COLOR = {
  'pan_mode': (127, 127, 127),
  'sends_a_mode': (0, 127, 0),
  'sends_b_mode': (0, 100, 0),
  'device_mode': (0, 0, 100)}
=======
ENCODER_MODE_TO_COLOR = {'pan_mode':(127, 127, 127), 
 'sends_a_mode':(0, 127, 0), 
 'sends_b_mode':(0, 100, 0), 
 'device_mode':(0, 0, 100)}
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
DISPLAY_LINE_WIDTH = 16

class InputOnlyButton(ButtonElement):

    def send_value(self, value, force=False, channel=None):
        pass


class KeyLabMkIICustom(KeyLabEssential):
    mixer_component_type = MixerComponent
    session_component_type = SessionComponent
    view_control_component_type = ViewControlComponent
    hardware_settings_component_type = HardwareSettingsComponent
    channel_strip_component_type = ChannelStripComponent

    def __init__(self, *a, **k):
        (super(KeyLabMkIICustom, self).__init__)(*a, **k)
        with self.component_guard():
            self._create_device_parameters()
            self._create_encoder_modes()
            self._create_session_recording()

    def can_lock_to_devices(self):
        return True

    def _create_controls(self):
        super(KeyLabMkIICustom, self)._create_controls()

        def make_button_row(index_offset, name):
            return ButtonMatrixElement(rows=[
             [create_button((index + index_offset), name=('{}_{}'.format(name, index))) for index in range(8)]],
              name=('{}s'.format(name)))

        self._select_buttons = make_button_row(24, 'Select_Button')
        self._solo_buttons = make_button_row(8, 'Solo_Button')
        self._mute_buttons = make_button_row(16, 'Mute_Button')
        self._record_arm_buttons = make_button_row(0, 'Record_Arm_Buttons')
        self._automation_button = create_button(56, name='Automation_Button')
        self._re_enable_automation_button = create_button(57,
          name='Re_Enable_Automation_Button')
        self._view_button = create_button(74, name='View_Button')
        self._pads = ButtonMatrixElement(rows=[[InputOnlyButton(True, MIDI_NOTE_TYPE, 9, identifier, name=('Pad_{}_{}'.format(col_index, row_index))) for col_index, identifier in enumerate(row)] for row_index, row in enumerate(PAD_IDS)])
        self._pad_leds = ButtonMatrixElement(rows=[[create_pad_led(identifier, 'Pad_LED_{}_{}'.format(col_index, row_index)) for col_index, identifier in enumerate(row)] for row_index, row in enumerate(PAD_LED_IDS)],
          name='Pad_LED_Matrix')
        self._display = PhysicalDisplayElement(DISPLAY_LINE_WIDTH, name='Display')
        self._display.set_message_parts(sysex.LCD_SET_STRING_MESSAGE_HEADER + (sysex.LCD_LINE_1_ITEM_ID,), (
         sysex.NULL, sysex.LCD_LINE_2_ITEM_ID) + (ord(' '),) * DISPLAY_LINE_WIDTH + (sysex.NULL, sysex.END_BYTE))
        self._encoder_mode_cycle_button = InputOnlyButton(True,
          MIDI_NOTE_TYPE,
          0,
          51,
          name='Mixer_Mode_Cycle_Button')
        self._vegas_mode_switch = SysexElement(send_message_generator=(lambda b: sysex.VEGAS_MODE_MESSAGE_HEADER + (
<<<<<<< HEAD
         b, sysex.END_BYTE)
),
=======
         b, sysex.END_BYTE)),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
          name='Vegas_Mode_Switch')
        self._encoder_mode_led = create_pad_led(42, name='Encoder_Mode_Led')

    def _create_mixer(self):
        super(KeyLabMkIICustom, self)._create_mixer()
        self._mixer.layer += Layer(track_select_buttons=(self._select_buttons),
          solo_buttons=(self._solo_buttons),
          mute_buttons=(self._mute_buttons),
          arm_buttons=(self._record_arm_buttons),
          selected_track_name_display=(self._display),
          volume_controls=(self._faders))

    def _create_encoder_modes(self):
        self._encoder_modes = ModesComponent(name='Mixer_Modes')
        self._encoder_modes.add_mode('pan_mode', (
         AddLayerMode(self._mixer, Layer(pan_controls=(self._encoders))),
         partial(self._encoder_mode_led.send_value, ENCODER_MODE_TO_COLOR['pan_mode'])))
        self._encoder_modes.add_mode('sends_a_mode', (
         AddLayerMode(self._mixer, Layer(send_a_controls=(self._encoders))),
         partial(self._encoder_mode_led.send_value, ENCODER_MODE_TO_COLOR['sends_a_mode'])))
        self._encoder_modes.add_mode('sends_b_mode', (
         AddLayerMode(self._mixer, Layer(send_b_controls=(self._encoders))),
         partial(self._encoder_mode_led.send_value, ENCODER_MODE_TO_COLOR['sends_b_mode'])))
        self._encoder_modes.layer = Layer(cycle_mode_button=(self._encoder_mode_cycle_button))
        self._encoder_modes.add_mode('device_mode', (
         self._device_parameters,
         partial(self._encoder_mode_led.send_value, ENCODER_MODE_TO_COLOR['device_mode'])))
        self._encoder_modes.selected_mode = 'pan_mode'

    def _create_device_parameters(self):
        self._device_parameters = SimpleDeviceParameterComponent(name='Device_Parameters',
          is_enabled=False,
          device_bank_registry=(self._device_bank_registry),
          layer=Layer(parameter_controls=(self._encoders)))

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(name='Session_Recording',
          is_enabled=False,
          layer=Layer(automation_button=(self._automation_button),
          re_enable_automation_button=(self._re_enable_automation_button)))
        self._session_recording.set_enabled(True)

    def _create_view_control(self):
        super(KeyLabMkIICustom, self)._create_view_control()
        self._view_control.layer += Layer(document_view_toggle_button=(self._view_button))

    def _create_hardware_settings(self):
        super(KeyLabMkIICustom, self)._create_hardware_settings()
        self._hardware_settings.layer += Layer(vegas_mode_switch=(self._vegas_mode_switch))

    @listens('daw_preset')
    def _on_memory_preset_changed_on_hardware(self, is_daw_preset_on):
        super(KeyLabMkIICustom, self)._on_memory_preset_changed_on_hardware(is_daw_preset_on)
        if is_daw_preset_on:
            self._encoder_mode_led.send_value(ENCODER_MODE_TO_COLOR[self._encoder_modes.selected_mode])