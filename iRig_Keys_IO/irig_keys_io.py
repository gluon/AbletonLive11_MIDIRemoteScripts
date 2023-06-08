from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, Layer, SimpleControlSurface
from ableton.v2.control_surface.components import TransportComponent
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement
from .mixer import MixerComponent
from .session_recording import SessionRecordingComponent
from .session_ring import SelectedTrackFollowingSessionRingComponent
from .skin import skin
PAD_IDS = (36, 38, 40, 42, 46, 43, 47, 49)
PAD_CHANNEL = 9

class IRigKeysIO(SimpleControlSurface):

    def __init__(self, *a, **k):
        (super(IRigKeysIO, self).__init__)(*a, **k)
        with self.component_guard():
            self._create_controls()
            self._create_mixer()
            self._create_transport()

    def _create_controls(self):
        self._encoders = ButtonMatrixElement(rows=[
         [EncoderElement(MIDI_CC_TYPE, 0, identifier, map_mode=(Live.MidiMap.MapMode.absolute), name=('Volume_Encoder_{}'.format(index))) for index, identifier in enumerate(range(12, 20))]],
          name='Volume_Encoders')
        self._data_encoder = EncoderElement(MIDI_CC_TYPE,
          0,
          22,
          map_mode=(Live.MidiMap.MapMode.relative_smooth_two_compliment),
          name='Data_Encoder')
        self._data_encoder_button = ButtonElement(True,
          MIDI_CC_TYPE, 0, 23, name='Data_Encoder_Button', skin=skin)
        self._play_button = ButtonElement(False,
          MIDI_CC_TYPE, 0, 118, name='Play_Button', skin=skin)
        self._record_button = ButtonElement(False,
          MIDI_CC_TYPE, 0, 119, name='Record_Button', skin=skin)
        self._record_stop_button = ButtonElement(False,
          MIDI_CC_TYPE, 0, 116, name='Record_Stop_Button', skin=skin)
        self._stop_button = ButtonElement(False,
          MIDI_CC_TYPE, 0, 117, name='Stop_Button', skin=skin)
        self._pads = ButtonMatrixElement(rows=[
         [ButtonElement(True, MIDI_NOTE_TYPE, PAD_CHANNEL, identifier, name=('Pad_{}'.format(index)), skin=skin) for index, identifier in enumerate(PAD_IDS)]])

    def _create_mixer(self):
        self._session_ring = SelectedTrackFollowingSessionRingComponent(is_enabled=False,
          num_tracks=(self._encoders.width()),
          num_scenes=(self._encoders.height()),
          name='Session_Ring')
        self._mixer = MixerComponent(tracks_provider=(self._session_ring), name='Mixer')
        self._mixer.layer = Layer(volume_controls=(self._encoders),
          track_scroll_encoder=(self._data_encoder),
          selected_track_arm_button=(self._data_encoder_button),
          mute_buttons=(self._pads))

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport')
        self._transport.layer = Layer(play_button=(self._play_button),
          stop_button=(self._stop_button))
        self._session_recording = SessionRecordingComponent(name='Session_Recording')
        self._session_recording.layer = Layer(record_button=(self._record_button),
          record_stop_button=(self._record_stop_button))