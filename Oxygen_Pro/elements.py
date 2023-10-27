# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_Pro\elements.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 6258 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement, SysexElement
from . import midi
from .skin import skin
MIDI_CHANNEL = 0

def create_button(identifier, name, msg_type=MIDI_CC_TYPE, channel=MIDI_CHANNEL, is_momentary=True, **k):
    return ButtonElement(
 is_momentary, msg_type, channel, identifier, name=name, skin=skin, **k)


def create_encoder(identifier, name, map_mode=Live.MidiMap.MapMode.absolute, **k):
    return EncoderElement(
 MIDI_CC_TYPE, MIDI_CHANNEL, identifier, map_mode, name=name, **k)


class Elements(object):

    def __init__(self, session_height, session_width, pad_ids, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.encoder_push_button = create_button(102,
          'Encoder_Push_Button', resource_type=PrioritizedResource)
        self.off_mode_button = create_button(57, 'Off_Mode_Button', channel=15)
        self.arm_mode_button = create_button(58, 'Arm_Mode_Button', channel=15)
        self.track_select_mode_button = create_button(59,
          'Track_Select_Mode_Button', channel=15)
        self.mute_mode_button = create_button(60, 'Mute_Mode_Button', channel=15)
        self.solo_mode_button = create_button(61, 'Solo_Mode_Button', channel=15)
        self.volume_mode_button = create_button(83, 'Volume_Mode_Button', channel=15)
        self.pan_mode_button = create_button(85, 'Pan_Mode_Button', channel=15)
        self.device_mode_button = create_button(86, 'Device_Mode_Button', channel=15)
        self.sends_mode_button = create_button(87, 'Sends_Mode_Button', channel=15)
        self.back_button = create_button(104, 'Back_Button')
        self.shift_button = create_button(105, 'Shift_Button', channel=12)
        self.metronome_button = create_button(106, 'Metronome_Button')
        self.bank_left_button = create_button(110, 'Bank_Left_Button')
        self.bank_right_button = create_button(111, 'Bank_Right_Button')
        self.preset_mode_button = create_button(112, 'Preset_Mode_Button')
        self.daw_mode_button = create_button(113, 'DAW_Mode_Button')
        self.loop_button = create_button(114, 'Loop_Button')
        self.rewind_button = create_button(115, 'Rewind_Button')
        self.fastforward_button = create_button(116, 'Fastforward_Button')
        self.stop_button = create_button(117, 'Stop_Button')
        self.play_button = create_button(118, 'Play_Button')
        self.record_button = create_button(119, 'Record_Button')
        self.fader_buttons = ButtonMatrixElement(rows=[
         [create_button((index + 32), ('Fader_Button_{}'.format(index)), is_momentary=False) for index in range(session_width)]],
          name='Fader_Buttons')
        self.scene_launch_buttons = ButtonMatrixElement(rows=[
         [create_button(index + 107, 'Scene_Launch_Button_{}'.format(index)) for index in range(session_height)]],
          name='Scene_Launch_Buttons')
        self.pads = ButtonMatrixElement(rows=[[create_button(ident, ('{}_Pad_{}'.format(row_index, col_index)), msg_type=MIDI_NOTE_TYPE) for col_index, ident in enumerate(pad_ids[row_index])] for row_index in range(session_height)],
          name='Pads')
        self.encoder = create_encoder(103,
          'Encoder', map_mode=(Live.MidiMap.MapMode.relative_signed_bit))
        self.encoder_with_encoder_push = self.with_modifier(self.encoder, 'encoder_push')
        self.master_fader = create_encoder(41, 'Master_Fader')
        self.faders = ButtonMatrixElement(rows=[
         [create_encoder(index + 12, 'Fader_{}'.format(index)) for index in range(session_width)]],
          name='Faders')
        self.knobs = ButtonMatrixElement(rows=[
         [create_encoder(index + 22, 'Knob_{}'.format(index)) for index in range(session_width)]],
          name='Knobs')
        self.firmware_mode_switch = SysexElement(name='Firmware_Mode_Switch',
          send_message_generator=(lambda v: midi.SYSEX_HEADER + midi.FIRMWARE_MODE_BYTES + (v, midi.SYSEX_END_BYTE)
))
        self.control_mode_switch = SysexElement(name='Control_Mode_Switch',
          send_message_generator=(lambda v: midi.SYSEX_HEADER + midi.CONTROL_MODE_BYTES + (v, midi.SYSEX_END_BYTE)
))
        self.led_control_switch = SysexElement(name='LED_Control_Switch',
          send_message_generator=(lambda v: midi.SYSEX_HEADER + midi.LED_CONTROL_BYTES + (v, midi.SYSEX_END_BYTE)
))
        self.led_mode_switch = SysexElement(name='LED_Mode_Switch',
          send_message_generator=(lambda v: midi.SYSEX_HEADER + midi.LED_MODE_BYTES + (v, midi.SYSEX_END_BYTE)
),
          default_value=(midi.FIRMWARE_CONTROL_BYTE))

    def with_modifier(self, control, modifier_name):
        return ComboElement(control=control,
          modifier=(getattr(self, '{}_button'.format(modifier_name))),
          name=('{}_With_{}'.format(control.name, modifier_name.upper())))