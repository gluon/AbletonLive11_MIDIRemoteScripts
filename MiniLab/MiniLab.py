# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab\MiniLab.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6981 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.ButtonMatrixElement as ButtonMatrixElement
import _Framework.DeviceComponent as DeviceComponent
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
import _Framework.Layer as Layer
import _Arturia.ArturiaControlSurface as ArturiaControlSurface
import _Arturia.MixerComponent as MixerComponent
import _Arturia.SessionComponent as SessionComponent
HARDWARE_ENCODER_IDS = (48, 1, 2, 9, 11, 12, 13, 14, 51, 3, 4, 10, 5, 6, 7, 8)
HARDWARE_BUTTON_IDS = list(range(112, 128))
PAD_IDENTIFIER_OFFSET = 36

class MiniLab(ArturiaControlSurface):
    session_component_type = SessionComponent
    encoder_msg_channel = 0
    encoder_msg_ids = (7, 74, 71, 76, 77, 93, 73, 75, 114, 18, 19, 16, 17, 91, 79,
                       72)
    pad_channel = 9

    def __init__(self, *a, **k):
        (super(MiniLab, self).__init__)(*a, **k)
        with self.component_guard():
            self._create_controls()
            self._create_device()
            self._create_session()
            self._create_mixer()

    def _create_controls(self):
        self._device_controls = ButtonMatrixElement(rows=[[EncoderElement(MIDI_CC_TYPE, (self.encoder_msg_channel), identifier, (Live.MidiMap.MapMode.relative_smooth_two_compliment), name=('Encoder_%d_%d' % (column_index, row_index))) for column_index, identifier in enumerate(row)] for row_index, row in enumerate((
         self.encoder_msg_ids[:4], self.encoder_msg_ids[8:12]))])
        self._horizontal_scroll_encoder = EncoderElement(MIDI_CC_TYPE,
          (self.encoder_msg_channel),
          (self.encoder_msg_ids[7]),
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Horizontal_Scroll_Encoder')
        self._vertical_scroll_encoder = EncoderElement(MIDI_CC_TYPE,
          (self.encoder_msg_channel),
          (self.encoder_msg_ids[15]),
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Vertical_Scroll_Encoder')
        self._volume_encoder = EncoderElement(MIDI_CC_TYPE,
          (self.encoder_msg_channel),
          (self.encoder_msg_ids[13]),
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Volume_Encoder')
        self._pan_encoder = EncoderElement(MIDI_CC_TYPE,
          (self.encoder_msg_channel),
          (self.encoder_msg_ids[12]),
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Pan_Encoder')
        self._send_a_encoder = EncoderElement(MIDI_CC_TYPE,
          (self.encoder_msg_channel),
          (self.encoder_msg_ids[4]),
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Send_A_Encoder')
        self._send_b_encoder = EncoderElement(MIDI_CC_TYPE,
          (self.encoder_msg_channel),
          (self.encoder_msg_ids[5]),
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Send_B_Encoder')
        self._send_encoders = ButtonMatrixElement(rows=[
         [
          self._send_a_encoder, self._send_b_encoder]])
        self._return_a_encoder = EncoderElement(MIDI_CC_TYPE,
          (self.encoder_msg_channel),
          (self.encoder_msg_ids[6]),
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Return_A_Encoder')
        self._return_b_encoder = EncoderElement(MIDI_CC_TYPE,
          (self.encoder_msg_channel),
          (self.encoder_msg_ids[14]),
          (Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Return_B_Encoder')
        self._return_encoders = ButtonMatrixElement(rows=[
         [
          self._return_a_encoder, self._return_b_encoder]])
        self._pads = ButtonMatrixElement(rows=[[ButtonElement(True, MIDI_NOTE_TYPE, (self.pad_channel), (col + 36 + 8 * row), name=('Pad_%d_%d' % (col, row))) for col in range(8)] for row in range(2)])

    def _create_device(self):
        self._device = DeviceComponent(name='Device',
          is_enabled=False,
          layer=Layer(parameter_controls=(self._device_controls)),
          device_selection_follows_track_selection=True)
        self._device.set_enabled(True)
        self.set_device_component(self._device)

    def _create_session(self):
        self._session = self.session_component_type(num_tracks=(self._pads.width()),
          num_scenes=(self._pads.height()),
          name='Session',
          is_enabled=False,
          layer=Layer(clip_launch_buttons=(self._pads),
          scene_select_control=(self._vertical_scroll_encoder)))
        self._session.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(name='Mixer',
          is_enabled=False,
          num_returns=2,
          layer=Layer(track_select_encoder=(self._horizontal_scroll_encoder),
          selected_track_volume_control=(self._volume_encoder),
          selected_track_pan_control=(self._pan_encoder),
          selected_track_send_controls=(self._send_encoders),
          return_volume_controls=(self._return_encoders)))
        self._mixer.set_enabled(True)

    def _collect_setup_messages(self):
        for cc_id, encoder_id in zip(self.encoder_msg_ids, HARDWARE_ENCODER_IDS):
            self._setup_hardware_encoder(encoder_id,
              cc_id, channel=(self.encoder_msg_channel))

        for index, pad_id in enumerate(HARDWARE_BUTTON_IDS):
            self._setup_hardware_button(pad_id, index + PAD_IDENTIFIER_OFFSET, self.pad_channel)