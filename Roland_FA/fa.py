# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_FA\fa.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 5903 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from functools import partial
from ableton.v2.base import const, inject
from ableton.v2.control_surface import MIDI_NOTE_TYPE, Layer, SimpleControlSurface
from ableton.v2.control_surface.components import DrumGroupComponent, MixerComponent, SessionRecordingComponent, SessionRingComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement
from ableton.v2.control_surface.mode import LayerMode, ModesComponent
from .control_element_utils import make_button, make_encoder
from .navigation import SessionNavigationComponent
from .skin import make_default_skin
from .transport import TransportComponent

class FA(SimpleControlSurface):

    def __init__(self, *a, **k):
        (super(FA, self).__init__)(*a, **k)
        with self.component_guard():
            with inject(skin=(const(make_default_skin()))).everywhere():
                self._create_controls()
            self._create_transport()
            self._create_session_recording()
            self._create_mixer()
            self._create_navigation()
            self._create_modes()
            self._create_drums()

    def _create_controls(self):
        self._jump_to_start_button = make_button(21, 'Jump_To_Start_Button')
        self._rwd_button = make_button(22, 'RWD_Button')
        self._ff_button = make_button(23, 'FF_Button')
        self._stop_button = make_button(25, 'Stop_Button')
        self._play_button = make_button(26, 'Play_Button')
        self._record_button = make_button(28, 'Record_Button')
        self._encoders = ButtonMatrixElement(rows=[
         [make_encoder(index + 70, 'Encoder_%d' % (index,)) for index in range(6)]],
          name='Encoders')
        self._volume_mode_button = make_button(16, 'Volume_Mode_Button')
        self._pan_mode_button = make_button(17, 'Pan_Mode_Button')
        self._send_a_mode_button = make_button(18, 'Send_A_Mode_Button')
        self._send_b_mode_button = make_button(19, 'Send_B_Mode_Button')
        self._s1_button = make_button(14, 'S1_Button')
        self._s2_button = make_button(15, 'S2_Button')
        self._pads = ButtonMatrixElement(rows=[[make_button((col_index + offset), ('Pad_%d_%d' % (col_index, row_index)), msg_type=MIDI_NOTE_TYPE) for col_index in range(4)] for row_index, offset in enumerate(range(72, 59, -4))],
          name='Pads')

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(play_button=(self._play_button),
          stop_button=(self._stop_button),
          seek_backward_button=(self._rwd_button),
          seek_forward_button=(self._ff_button),
          jump_to_start_button=(self._jump_to_start_button)))
        self._transport.set_enabled(True)

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(name='Session_Recording',
          is_enabled=False,
          layer=Layer(record_button=(self._record_button)))
        self._session_recording.set_enabled(True)

    def _create_mixer(self):
        self._session_ring = SessionRingComponent(num_tracks=(self._encoders.width()),
          num_scenes=0,
          is_enabled=False,
          name='Session_Ring')
        self._mixer = MixerComponent(tracks_provider=(self._session_ring), name='Mixer')

    def _create_navigation(self):
        self._navigation = SessionNavigationComponent(session_ring=(self._session_ring),
          name='Navigation',
          is_enabled=False,
          layer=Layer(page_left_button=(self._s1_button),
          page_right_button=(self._s2_button)))
        self._navigation.set_enabled(True)

    def _create_modes(self):
        self._modes = ModesComponent(name='Encoder_Modes')
        self._modes.add_mode('volume_mode', LayerMode(self._mixer, Layer(volume_controls=(self._encoders))))
        self._modes.add_mode('pan_mode', LayerMode(self._mixer, Layer(pan_controls=(self._encoders))))
        self._modes.add_mode('send_a_mode', [
         LayerMode(self._mixer, Layer(send_controls=(self._encoders))),
         partial(self._set_send_index, 0)])
        self._modes.add_mode('send_b_mode', [
         LayerMode(self._mixer, Layer(send_controls=(self._encoders))),
         partial(self._set_send_index, 1)])
        self._modes.layer = Layer(volume_mode_button=(self._volume_mode_button),
          pan_mode_button=(self._pan_mode_button),
          send_a_mode_button=(self._send_a_mode_button),
          send_b_mode_button=(self._send_b_mode_button))
        self._modes.selected_mode = 'volume_mode'

    def _set_send_index(self, index):
        self._mixer.send_index = index if index < self._mixer.num_sends else None

    def _create_drums(self):
        self._drums = DrumGroupComponent(name='Drum_Group',
          is_enabled=False,
          translation_channel=0,
          layer=Layer(matrix=(self._pads)))
        self._drums.set_enabled(True)