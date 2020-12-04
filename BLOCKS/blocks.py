#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/BLOCKS/blocks.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import range
from past.utils import old_div
from functools import partial
import Live
from ableton.v2.base import clamp, listens, liveobj_valid, nop
from ableton.v2.control_surface import ControlSurface, Layer, MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, PercussionInstrumentFinder
from ableton.v2.control_surface.components import DrumGroupComponent, SessionComponent, SessionNavigationComponent, SessionRingComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement, EncoderElement, SysexElement
from ableton.v2.control_surface.midi import CC_STATUS
from ableton.v2.control_surface.mode import LayerMode
from .button import ButtonElement
from .colors import LIVE_COLORS_TO_MIDI_VALUES, RGB_COLOR_TABLE, Rgb
from .mode import ModesComponent
from .element_translator import ElementTranslator
from .skin import skin
from .target_track_provider import TargetTrackProvider
NUM_TRACKS = 4
NUM_SCENES = 4
MODE_MSG_CHANNEL = 15
MODE_NAMES_TO_IDS = {u'session': 60,
 u'melodic': 61,
 u'drum': 62,
 u'disabled': 63}
MELODIC_FEEDBACK_CHANNEL = 3
DRUM_FEEDBACK_CHANNEL = 4
NON_FEEDBACK_CHANNEL = 0
FEEDBACK_CHANNELS = [MELODIC_FEEDBACK_CHANNEL, DRUM_FEEDBACK_CHANNEL]
TEMPO_MIN = 20.0
TEMPO_MAX = 250.0
PB_VALUE_RANGE_MAX = 16383
SYSEX_HEADER = (240, 0, 33, 16)

def is_playable(track):
    return liveobj_valid(track) and track.has_midi_input and not track.is_frozen


class Blocks(ControlSurface):

    def __init__(self, *a, **k):
        super(Blocks, self).__init__(*a, **k)
        with self.component_guard():
            self._create_controls()
            self._create_session()
            self._create_navigation()
            self._create_drums()
            self._create_drum_finder()
            self._create_modes()
        self.set_feedback_channels(FEEDBACK_CHANNELS)
        self.__on_target_track_changed.subject = self._target_track_provider
        self.__on_armed_tracks_changed.subject = self._target_track_provider
        self.__on_percussion_instrument_found.subject = self._percussion_instrument_finder
        self.__on_percussion_instrument_found()
        self.__on_tempo_changed_in_live.subject = self.song
        self.__on_tempo_changed_in_live()
        self.__on_session_record_changed.subject = self.song
        self._set_feedback_velocity()

    def _create_controls(self):
        self._pads_raw = [ ButtonElement(True, MIDI_NOTE_TYPE, 0, identifier, name=u'Pad_{}'.format(identifier), skin=skin) for identifier in range(100) ]
        self._session_matrix = ButtonMatrixElement(rows=[ [ self._pads_raw[offset + col] for col in range(NUM_TRACKS) ] for offset in range(80, 49, -10) ], name=u'Session_Matrix')
        self._scene_launch_button_matrix = ButtonMatrixElement(rows=[[ self._pads_raw[identifier] for identifier in range(89, 58, -10) ]], name=u'Scene_Launch_Button_Matrix')
        self._stop_all_clips_button = ButtonElement(True, MIDI_NOTE_TYPE, 0, 127, skin=skin, name=u'Stop_All_Clips_Button')
        self._nav_down_button = self._pads_raw[90]
        self._nav_up_button = self._pads_raw[91]
        self._nav_left_button = self._pads_raw[92]
        self._nav_right_button = self._pads_raw[93]
        self._mode_cycle_button = ButtonElement(True, MIDI_CC_TYPE, 0, 127, skin=skin, name=u'Mode_Button')
        self._drum_pads = ButtonMatrixElement(rows=[ [ self._pads_raw[offset + col] for col in range(4) ] for offset in range(48, 35, -4) ], name=u'Drum_Pads')
        self._tempo_encoder = EncoderElement(MIDI_PB_TYPE, 0, 0, Live.MidiMap.MapMode.absolute, send_should_depend_on_forwarding=False, name=u'Tempo_Encoder')
        self._tempo_encoder.reset = nop
        self._sysex_element = SysexElement(sysex_identifier=SYSEX_HEADER, name=u'Sysex_Element')
        self._sysex_element.add_value_listener(nop)
        self._surface_update_message_element = ButtonElement(True, MIDI_CC_TYPE, 0, 64, name=u'Surface_Update_Message_Element')
        self.__on_surface_update_message_received.subject = self._surface_update_message_element

    def _create_session(self):
        self._session_ring = SessionRingComponent(num_tracks=NUM_TRACKS, num_scenes=NUM_SCENES, is_enabled=False, name=u'Session_Ring')
        self._session = SessionComponent(session_ring=self._session_ring, name=u'Session')
        self._session.set_rgb_mode(LIVE_COLORS_TO_MIDI_VALUES, RGB_COLOR_TABLE)

    def _create_navigation(self):
        self._session_navigation = SessionNavigationComponent(session_ring=self._session_ring, name=u'Session_Navigation')

    def _create_drums(self):
        self._drum_group = DrumGroupComponent(name=u'Drum_Group', translation_channel=DRUM_FEEDBACK_CHANNEL)

    def _create_drum_finder(self):
        self._target_track_provider = TargetTrackProvider()
        self._percussion_instrument_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=self._target_track_provider.target_track))

    def _create_modes(self):
        self._note_modes = ModesComponent(name=u'Note_Modes', is_enabled=False)
        self._melodic_pad_translator = ElementTranslator(self._pads_raw, MELODIC_FEEDBACK_CHANNEL, NON_FEEDBACK_CHANNEL)
        self._note_modes.add_mode(u'drum', [partial(self._send_mode_message, u'drum'), LayerMode(self._drum_group, Layer(matrix=self._drum_pads))])
        self._note_modes.add_mode(u'melodic', [partial(self._send_mode_message, u'melodic'), self._melodic_pad_translator])
        self._note_modes.add_mode(u'disabled', [partial(self._send_mode_message, u'disabled')])
        self._modes = ModesComponent(name=u'Modes')
        self._modes.add_mode(u'session', [partial(self._send_mode_message, u'session'),
         partial(self._clear_send_cache, self._pads_raw),
         LayerMode(self._session, Layer(clip_launch_buttons=self._session_matrix, scene_launch_buttons=self._scene_launch_button_matrix, stop_all_clips_button=self._stop_all_clips_button)),
         LayerMode(self._session_navigation, Layer(down_button=self._nav_down_button, up_button=self._nav_up_button, left_button=self._nav_left_button, right_button=self._nav_right_button))])
        self._modes.add_mode(u'note', [self._note_modes, self._select_note_mode])
        self._modes.cycle_mode_button.set_control_element(self._mode_cycle_button)
        self._modes.selected_mode = u'session'

    @listens(u'target_track')
    def __on_target_track_changed(self):
        self._percussion_instrument_finder.device_parent = self._target_track_provider.target_track
        self._select_note_mode()

    @listens(u'instrument')
    def __on_percussion_instrument_found(self):
        self._drum_group.set_drum_group_device(self._percussion_instrument_finder.drum_group)
        self._select_note_mode()

    @listens(u'armed_tracks')
    def __on_armed_tracks_changed(self):
        self._set_feedback_velocity()

    @listens(u'tempo')
    def __on_tempo_changed_in_live(self):
        normalized_tempo = old_div(clamp(self.song.tempo, TEMPO_MIN, TEMPO_MAX) - TEMPO_MIN, TEMPO_MAX - TEMPO_MIN)
        value_to_send = clamp(int(normalized_tempo * PB_VALUE_RANGE_MAX), 0, PB_VALUE_RANGE_MAX)
        self._tempo_encoder.send_value(value_to_send)

    @listens(u'session_record')
    def __on_session_record_changed(self):
        self._set_feedback_velocity()

    @listens(u'value')
    def __on_surface_update_message_received(self, value):
        if value:
            self._clear_send_cache(self.controls)
            self.update()
            self.__on_tempo_changed_in_live()

    def _set_feedback_velocity(self):
        target_track = self._target_track_provider.target_track
        if self.song.session_record and liveobj_valid(target_track) and target_track.arm:
            feedback_velocity = Rgb.RED.midi_value
        else:
            feedback_velocity = Rgb.GREEN.midi_value
        self._c_instance.set_feedback_velocity(int(feedback_velocity))

    def _select_note_mode(self):
        track = self._target_track_provider.target_track
        drum_device = self._percussion_instrument_finder.drum_group
        if not is_playable(track):
            self._note_modes.selected_mode = u'disabled'
        elif drum_device:
            self._note_modes.selected_mode = u'drum'
        else:
            self._note_modes.selected_mode = u'melodic'
        if self._note_modes.selected_mode == u'disabled':
            self.release_controlled_track()
        else:
            self.set_controlled_track(track)

    def _send_mode_message(self, mode):
        self._send_midi((CC_STATUS + MODE_MSG_CHANNEL, MODE_NAMES_TO_IDS[mode], 127))

    def _clear_send_cache(self, controls):
        for control in controls:
            control.clear_send_cache()

    def port_settings_changed(self):
        super(Blocks, self).port_settings_changed()
        self.set_feedback_channels(FEEDBACK_CHANNELS)
