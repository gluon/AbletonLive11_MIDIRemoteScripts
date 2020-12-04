#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/BeatStep/BeatStep.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import object
from itertools import chain
import Live
from _Arturia.ArturiaControlSurface import ArturiaControlSurface
from _Arturia.SessionComponent import SessionComponent
from _Arturia.MixerComponent import MixerComponent
from _Framework.Layer import Layer
from _Framework.Skin import Skin
from _Framework.DeviceComponent import DeviceComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ButtonElement import ButtonElement, Color
from _Framework.EncoderElement import EncoderElement
HARDWARE_ENCODER_IDS = list(range(32, 48))
HARDWARE_STOP_BUTTON_ID = 89
HARDWARE_PLAY_BUTTON_ID = 88
HARDWARE_PAD_IDS = list(range(112, 128))
ENCODER_MSG_IDS = (10, 74, 71, 76, 77, 93, 73, 75, 114, 18, 19, 16, 17, 91, 79, 72)
PAD_MSG_IDS = (list(range(44, 52)), list(range(36, 44)))
PAD_CHANNEL = 9

class Colors(object):

    class Session(object):
        ClipStarted = Color(0)
        ClipStopped = Color(0)
        ClipRecording = Color(0)
        ClipTriggeredPlay = Color(0)
        ClipTriggeredRecord = Color(0)
        RecordButton = Color(0)
        ClipEmpty = Color(0)


class BeatStep(ArturiaControlSurface):

    def __init__(self, *a, **k):
        super(BeatStep, self).__init__(*a, **k)
        self._skin = Skin(Colors)
        with self.component_guard():
            self._create_controls()
            self._create_device()
            self._create_session()
            self._create_mixer()
            self._create_transport()

    def _create_controls(self):
        self._device_encoders = ButtonMatrixElement(rows=[ [ EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Encoder_%d_%d' % (column_index, row_index)) for column_index, identifier in enumerate(row) ] for row_index, row in enumerate((ENCODER_MSG_IDS[:4], ENCODER_MSG_IDS[8:12])) ])
        self._horizontal_scroll_encoder = EncoderElement(MIDI_CC_TYPE, 0, 75, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Horizontal_Scroll_Encoder')
        self._vertical_scroll_encoder = EncoderElement(MIDI_CC_TYPE, 0, 72, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Vertical_Scroll_Encoder')
        self._volume_encoder = EncoderElement(MIDI_CC_TYPE, 0, 91, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Volume_Encoder')
        self._pan_encoder = EncoderElement(MIDI_CC_TYPE, 0, 17, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Pan_Encoder')
        self._send_a_encoder = EncoderElement(MIDI_CC_TYPE, 0, 77, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Send_A_Encoder')
        self._send_b_encoder = EncoderElement(MIDI_CC_TYPE, 0, 93, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Send_B_Encoder')
        self._send_encoders = ButtonMatrixElement(rows=[[self._send_a_encoder, self._send_b_encoder]])
        self._return_a_encoder = EncoderElement(MIDI_CC_TYPE, 0, 73, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Return_A_Encoder')
        self._return_b_encoder = EncoderElement(MIDI_CC_TYPE, 0, 79, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Return_B_Encoder')
        self._return_encoders = ButtonMatrixElement(rows=[[self._return_a_encoder, self._return_b_encoder]])
        self._pads = ButtonMatrixElement(rows=[ [ ButtonElement(True, MIDI_NOTE_TYPE, PAD_CHANNEL, identifier, name=u'Pad_%d_%d' % (col_index, row_index), skin=self._skin) for col_index, identifier in enumerate(row) ] for row_index, row in enumerate(PAD_MSG_IDS) ])
        self._stop_button = ButtonElement(True, MIDI_CC_TYPE, 0, 1, name=u'Stop_Button')
        self._play_button = ButtonElement(True, MIDI_CC_TYPE, 0, 2, name=u'Play_Button')

    def _create_device(self):
        self._device = DeviceComponent(name=u'Device', is_enabled=False, layer=Layer(parameter_controls=self._device_encoders), device_selection_follows_track_selection=True)
        self._device.set_enabled(True)
        self.set_device_component(self._device)

    def _create_session(self):
        self._session = SessionComponent(name=u'Session', is_enabled=False, num_tracks=self._pads.width(), num_scenes=self._pads.height(), enable_skinning=True, layer=Layer(clip_launch_buttons=self._pads, scene_select_control=self._vertical_scroll_encoder))
        self._session.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(name=u'Mixer', is_enabled=False, num_returns=2, layer=Layer(track_select_encoder=self._horizontal_scroll_encoder, selected_track_volume_control=self._volume_encoder, selected_track_pan_control=self._pan_encoder, selected_track_send_controls=self._send_encoders, return_volume_controls=self._return_encoders))
        self._mixer.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name=u'Transport', is_enabled=False, layer=Layer(stop_button=self._stop_button, play_button=self._play_button))
        self._transport.set_enabled(True)

    def _collect_setup_messages(self):
        for identifier, hardware_id in zip(ENCODER_MSG_IDS, HARDWARE_ENCODER_IDS):
            self._setup_hardware_encoder(hardware_id, identifier)

        self._setup_hardware_button(HARDWARE_STOP_BUTTON_ID, 1, msg_type=u'cc')
        self._setup_hardware_button(HARDWARE_PLAY_BUTTON_ID, 2, msg_type=u'cc')
        for hardware_id, identifier in zip(HARDWARE_PAD_IDS, chain(*PAD_MSG_IDS)):
            self._setup_hardware_button(hardware_id, identifier, PAD_CHANNEL, msg_type=u'note')
