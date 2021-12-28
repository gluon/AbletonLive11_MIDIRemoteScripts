#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/novation_base.py
from __future__ import absolute_import, print_function, unicode_literals
from contextlib import contextmanager
from ableton.v2.base import const, inject, nop
from ableton.v2.control_surface import IdentifiableControlSurface, Layer
from ableton.v2.control_surface.components import SessionComponent, SessionRecordingComponent, SessionRingComponent, SimpleTrackAssigner
from ableton.v2.control_surface.mode import ModesComponent
from . import sysex
from .channel_strip import ChannelStripComponent
from .colors import CLIP_COLOR_TABLE, RGB_COLOR_TABLE
from .launchpad_elements import LaunchpadElements, SESSION_HEIGHT, SESSION_WIDTH
from .mixer import MixerComponent
from .session_navigation import SessionNavigationComponent
from .skin import skin
from .track_recording import TrackRecordingComponent

class NovationBase(IdentifiableControlSurface):
    model_family_code = (0, 0)
    element_class = LaunchpadElements
    session_class = SessionComponent
    mixer_class = MixerComponent
    session_recording_class = SessionRecordingComponent
    track_recording_class = TrackRecordingComponent
    channel_strip_class = ChannelStripComponent
    session_height = SESSION_HEIGHT
    skin = skin
    suppress_layout_switch = True

    def __init__(self, *a, **k):
        super(NovationBase, self).__init__(product_id_bytes=(sysex.NOVATION_MANUFACTURER_ID + self.model_family_code + sysex.DEVICE_FAMILY_MEMBER_CODE), *a, **k)
        self._element_injector = inject(element_container=const(None)).everywhere()
        with self.component_guard():
            with inject(skin=const(self.skin)).everywhere():
                self._elements = self.element_class()
        self._element_injector = inject(element_container=const(self._elements)).everywhere()
        if self.suppress_layout_switch:
            self.register_slot(self._elements.layout_switch, nop, u'value')
        with self.component_guard():
            self._create_components()

    def on_identified(self, midi_bytes):
        self._session_ring.set_enabled(True)
        super(NovationBase, self).on_identified(midi_bytes)

    def port_settings_changed(self):
        self._session_ring.set_enabled(False)
        super(NovationBase, self).port_settings_changed()

    @contextmanager
    def _component_guard(self):
        with super(NovationBase, self)._component_guard():
            with self._element_injector:
                yield

    def _create_components(self):
        self._create_session()
        self._create_mixer()

    def _create_session(self):
        self._session_ring = SessionRingComponent(name=u'Session_Ring', is_enabled=False, num_tracks=SESSION_WIDTH, num_scenes=self.session_height)
        self._session = self.session_class(name=u'Session', is_enabled=False, session_ring=self._session_ring, layer=self._create_session_layer())
        self._session.set_rgb_mode(CLIP_COLOR_TABLE, RGB_COLOR_TABLE)
        self._session.set_enabled(True)
        self._session_navigation = SessionNavigationComponent(name=u'Session_Navigation', is_enabled=False, session_ring=self._session_ring, layer=self._create_session_navigation_layer())
        self._session_navigation.set_enabled(True)

    def _create_session_layer(self):
        return Layer(clip_launch_buttons=u'clip_launch_matrix')

    def _create_session_navigation_layer(self):
        return Layer(up_button=u'up_button', down_button=u'down_button', left_button=u'left_button', right_button=u'right_button')

    def _create_mixer(self):
        self._mixer = self.mixer_class(name=u'Mixer', auto_name=True, tracks_provider=self._session_ring, track_assigner=SimpleTrackAssigner(), invert_mute_feedback=True, channel_strip_component_type=self.channel_strip_class)

    def _create_session_recording(self):
        self._session_recording = self.session_recording_class(self._target_track, name=u'Session_Recording', is_enabled=False, layer=Layer(record_button=u'record_button'))

    def _create_track_recording(self):
        self._track_recording = self.track_recording_class(self._target_track, name=u'Track_Recording', is_enabled=False, layer=Layer(record_button=u'record_button'))

    def _create_recording_modes(self):
        self._create_session_recording()
        self._create_track_recording()
        self._recording_modes = ModesComponent(name=u'Recording_Modes')
        self._recording_modes.add_mode(u'session', self._session_recording)
        self._recording_modes.add_mode(u'track', self._track_recording)
        self._recording_modes.selected_mode = u'session'
