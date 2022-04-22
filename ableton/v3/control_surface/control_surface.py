# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/control_surface.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 15686 bytes
from __future__ import absolute_import, print_function, unicode_literals
from abc import abstractmethod
from types import SimpleNamespace
from ableton.v2.control_surface import SimpleControlSurface
from ..base import const, find_if, inject, is_song_recording, lazy_attribute, listens, liveobj_valid, nop, track_can_record
from . import DEFAULT_PRIORITY, BasicColors, DeviceBankRegistry, DeviceProvider, Layer, PercussionInstrumentFinder, midi
from .components import BackgroundComponent, DrumGroupComponent, SessionComponent, SessionRingComponent, TargetTrackComponent
from .default_skin import default_skin
from .identification import IdentificationComponent
LOW_PRIORITY = DEFAULT_PRIORITY - 1
HIGH_PRIORITY = DEFAULT_PRIORITY + 1
M4L_PRIORITY = HIGH_PRIORITY + 1

class ControlSurfaceSpecification(SimpleNamespace):
    elements_type = None
    control_surface_skin = default_skin
    num_tracks = 8
    num_scenes = 1
    include_returns = False
    session_ring_component_type = SessionRingComponent
    target_track_component_type = TargetTrackComponent
    feedback_channels = None
    playing_feedback_velocity = BasicColors.ON.midi_value
    recording_feedback_velocity = BasicColors.ON.midi_value
    device_provider_type = DeviceProvider
    background_priority = LOW_PRIORITY
    identity_response_id_bytes = None
    custom_identity_response = None
    identity_request_delay = 0.0
    identity_request = midi.SYSEX_IDENTITY_REQUEST_MESSAGE


class ControlSurface(SimpleControlSurface):

    def __init__(self, specification=None, entering_component_guard_hook=None, get_additional_dependencies_hook=None, *a, **k):
        (super().__init__)(*a, **k)
        entering_component_guard_hook = entering_component_guard_hook or nop
        dependency_hook = lambda: {}
        get_additional_dependencies_hook = get_additional_dependencies_hook or dependency_hook
        is_identifiable = specification.identity_response_id_bytes is not None or specification.custom_identity_response is not None
        self._specification = specification
        self._device_provider = None
        self._device_bank_registry = None
        self._drum_group_finder = None
        self._can_update_controlled_track = False
        with inject(skin=(const(specification.control_surface_skin))).everywhere():
            with self._control_surface_injector:
                self._elements = self._create_elements(specification)
        with self.component_guard():
            entering_component_guard_hook()
            self._background = self._create_background(specification.background_priority)
            self._identification = self._create_identification(specification) if is_identifiable else None
            self._target_track = specification.target_track_component_type()
            self._ControlSurface__on_target_track_changed.subject = self._target_track
            self._create_feedback_related_listeners()
            with self._create_extended_injector(get_additional_dependencies_hook):
                self._create_control_surface()
        self._can_enable_session_ring = is_identifiable and find_if(lambda x: isinstance(x, SessionComponent), self._components) is not None

    def disconnect(self):
        super().disconnect()
        self._specification = None
        self._elements = None
        self._device_provider = None
        self._device_bank_registry = None
        self._drum_group_finder = None

    @abstractmethod
    def _create_control_surface(self):
        pass

    @property
    def device_provider(self):
        return self._device_provider

    @property
    def device_bank_registry(self):
        return self._device_bank_registry

    @property
    def drum_group_finder(self):
        return self._drum_group_finder

    def port_settings_changed(self):
        if self._identification:
            self._identification.request_identity()
        else:
            self.refresh_state()

    def on_identified(self, response_bytes):
        self.refresh_state()

    def refresh_state(self):
        super().refresh_state()
        if self._specification.feedback_channels is not None:
            self._c_instance.set_feedback_channels(self._specification.feedback_channels)
        self._ControlSurface__on_target_track_changed()
        self._update_feedback_velocity()

    def can_lock_to_devices(self):
        return self._device_provider is not None

    def lock_to_device(self, device):
        with self.component_guard():
            self._device_provider.lock_to_device(device)

    def unlock_from_device(self, _):
        with self.component_guard():
            self._device_provider.unlock_from_device()

    def restore_bank(self, bank_index):
        device = self._device_provider.device
        if self._device_provider.is_locked_to_device:
            if liveobj_valid(device):
                with self.component_guard():
                    self._device_bank_registry.set_device_bank(device, bank_index)

    def target_track_changed(self, track):
        pass

    def drum_group_changed(self, drum_group):
        pass

    def set_is_observing_instruments(self, is_observing):
        self._drum_group_finder.is_enabled = is_observing
        if is_observing:
            self.drum_group_changed(self._drum_group_finder.drum_group)

    def set_can_update_controlled_track(self, can_update):
        self._can_update_controlled_track = can_update
        self._update_controlled_track()

    def mxd_grab_control_priority(self):
        return M4L_PRIORITY

    def _create_elements(self, specification):
        return specification.elements_type()

    def _create_background(self, priority):
        layer_dict = {c.name:c for c in self.controls}
        layer_dict['priority'] = priority
        background = BackgroundComponent(is_enabled=False, layer=Layer(**layer_dict))
        background.set_enabled(True)
        return background

    def _create_identification(self, specification):
        identification = IdentificationComponent(identity_request=(specification.identity_request),
          identity_request_delay=(specification.identity_request_delay),
          identity_response_id_bytes=(specification.identity_response_id_bytes),
          custom_identity_response=(specification.custom_identity_response))
        self._ControlSurface__on_is_identified_changed.subject = identification
        return identification

    @lazy_attribute
    def _create_session_ring(self):
        self._session_ring = self._specification.session_ring_component_type(is_enabled=False,
          num_tracks=(self._specification.num_tracks),
          num_scenes=(self._specification.num_scenes),
          include_returns=(self._specification.include_returns))
        return self._session_ring

    @lazy_attribute
    def _create_device_provider(self):
        self._device_provider = self.register_disconnectable(self._specification.device_provider_type(song=(self.song)))
        self._device_provider.update_device_selection()
        return self._device_provider

    @lazy_attribute
    def _create_device_bank_registry(self):
        self._device_bank_registry = self.register_disconnectable(DeviceBankRegistry())
        return self._device_bank_registry

    def _create_extended_injector(self, get_additional_dependencies_hook):
        inject_dict = {'element_container':const(self._elements), 
         'full_velocity':const(self._c_instance.full_velocity), 
         'target_track':const(self._target_track), 
         'session_ring':lambda: self._create_session_ring, 
         'device_provider':lambda: self._create_device_provider, 
         'device_bank_registry':lambda: self._create_device_bank_registry, 
         'toggle_lock':const(self._c_instance.toggle_lock)}
        inject_dict.update(get_additional_dependencies_hook())
        return inject(**inject_dict).everywhere()

    def _create_feedback_related_listeners(self):
        self.register_slot(self.song, self._update_feedback_velocity, 'session_record')
        self.register_slot(self.song, self._update_feedback_velocity, 'record_mode')

    def _register_component(self, component):
        super()._register_component(component)
        if isinstance(component, DrumGroupComponent):
            self._drum_group_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=(self._target_track.target_track),
              is_enabled=False))
            self._ControlSurface__on_drum_group_changed.subject = self._drum_group_finder

    def _update_feedback_velocity(self):
        track = self._target_track.target_track
        if is_song_recording(self.song) and track_can_record(track):
            feedback_velocity = self._specification.recording_feedback_velocity
        else:
            feedback_velocity = self._specification.playing_feedback_velocity
        self._c_instance.set_feedback_velocity(int(feedback_velocity))

    def _update_controlled_track(self, *_):
        if self._can_update_controlled_track:
            self.set_controlled_track(self._target_track.target_track)
        else:
            self.release_controlled_track()

    @listens('target_track')
    def __on_target_track_changed(self):
        track = self._target_track.target_track
        self._ControlSurface__on_track_arm_changed.subject = track
        self._ControlSurface__on_track_implicit_arm_changed.subject = track
        if self._drum_group_finder:
            self._drum_group_finder.device_parent = track
        self._update_controlled_track()
        self.target_track_changed(track)

    @listens('arm')
    def __on_track_arm_changed(self):
        self._update_feedback_velocity()

    @listens('implicit_arm')
    def __on_track_implicit_arm_changed(self):
        self._update_feedback_velocity()

    @listens('instrument')
    def __on_drum_group_changed(self):
        self.drum_group_changed(self._drum_group_finder.drum_group)

    @listens('is_identified')
    def __on_is_identified_changed(self, is_identified):
        if is_identified:
            self.on_identified(self._identification.received_response_bytes)
        if self._can_enable_session_ring:
            self._session_ring.set_enabled(is_identified)