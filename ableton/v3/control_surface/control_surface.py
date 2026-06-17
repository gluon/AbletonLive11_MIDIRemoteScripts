# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\control_surface.py
# Compiled at: 2023-09-22 09:34:38
# Size of source mod 2**32: 20938 bytes
from __future__ import absolute_import, print_function, unicode_literals
from contextlib import contextmanager, nullcontext
from ableton.v2.control_surface import SimpleControlSurface
from ..base import const, find_if, inject, lazy_attribute, listens
from ..live import is_song_recording, is_track_armed, liveobj_valid
from . import CompoundElement, DeviceBankRegistry, NotifyingControlElement
from .components import BackgroundComponent, DrumGroupComponent, SessionComponent, SlicedSimplerComponent, ViewControlComponent
from .consts import M4L_PRIORITY
from .control_surface_mapping import ControlSurfaceMappingMixin
from .display import Display, Renderable
from display.view.util import suppress_notifications
from .identification import IdentificationComponent
from .instrument_finder import InstrumentFinderComponent
from .layer import Layer
from .session_ring_selection_linking import SessionRingSelectionLinking

def create_control_surface(name=None, specification=None, c_instance=None):
    return type(name, (ControlSurface,), {})(specification, c_instance=c_instance)


class ControlSurface(SimpleControlSurface, ControlSurfaceMappingMixin):

    def __init__(self, specification=None, *a, **k):
        (super().__init__)(a, specification=specification, **k)
        is_identifiable = specification.identity_response_id_bytes is not None or specification.custom_identity_response is not None
        self.specification = specification
        self.device_provider = None
        self.device_bank_registry = None
        self.display = None
        self.instrument_finder = None
        self.session_ring_selection_linking = None
        self._can_update_controlled_track = False
        self._can_enable_auto_arm = False
        self._deferring_render_and_update_display = nullcontext
        self._drum_group_component = None
        self._sliced_simpler_component = None
        self._control_surface_injector.update(react=(const(self.react)),
          notifications=(const(specification.display_specification.notifications)),
          suppress_notifications=(lambda: self._suppress_notifications
))
        with inject(skin=(const(specification.control_surface_skin))).everywhere():
            with self._control_surface_injector:
                self.elements = self._create_elements(specification)
                self._element_injector = inject(element_container=(const(self.elements))).everywhere()
        with self.component_guard():
            self._on_entering_component_guard()
            self._background = self._create_background(specification.background_priority)
            self._identification = self._create_identification(specification) if is_identifiable else None
            self._target_track = specification.target_track_component_type()
            self._ControlSurface__on_target_track_changed.subject = self._target_track
            self._create_feedback_related_listeners()
            with self._create_extended_injector():
                if is_identifiable:
                    self._auto_arm = specification.auto_arm_component_type(is_enabled=False) if specification.include_auto_arming else None
                    self.setup()
                    if self._drum_group_component or self._sliced_simpler_component:
                        self._ControlSurface__on_instrument_changed()
                    if specification.display_specification.protocol:
                        self.display = self.register_disconnectable(Display(specification.display_specification, self.renderable_components, self.elements))
                        self._deferring_render_and_update_display = self.display.deferring_render_and_update_display
        self._can_enable_session_ring = is_identifiable and find_if(lambda x: isinstance(x, SessionComponent)
, self._components) is not None

    def disconnect(self):
        if self.specification.send_goodbye_messages_last:
            super().disconnect()
            self._send_specification_messages(messages_name='goodbye_messages')
        else:
            self._send_specification_messages(messages_name='goodbye_messages')
            super().disconnect()
        self.specification = None
        self.elements = None
        self.device_provider = None
        self.device_bank_registry = None
        self.instrument_finder = None
        self.session_ring_selection_linking = None
        self._drum_group_component = None
        self._sliced_simpler_component = None

    @property
    def renderable_components(self):
        return tuple((comp for comp in self._components if isinstance(comp, Renderable)))

    @property
    def controls(self):
        return [control for control in self._controls if not control.is_private]

    def port_settings_changed(self):
        if self._identification:
            self._identification.request_identity()
        else:
            self._send_specification_messages()
            self.refresh_state()

    def on_identified(self, response_bytes):
        self._send_specification_messages()
        self.refresh_state()

    def refresh_state(self):
        super().refresh_state()
        if self.specification.feedback_channels is not None:
            self._c_instance.set_feedback_channels(self.specification.feedback_channels)
        self._ControlSurface__on_target_track_changed()
        self._update_feedback_velocity()

    def can_lock_to_devices(self):
        return self.device_provider is not None

    def lock_to_device(self, device):
        with self.component_guard():
            self.device_provider.lock_to_device(device)

    def unlock_from_device(self, _):
        with self.component_guard():
            self.device_provider.unlock_from_device()

    def restore_bank(self, bank_index):
        device = self.device_provider.device
        if self.device_provider.is_locked_to_device:
            if liveobj_valid(device):
                with self.component_guard():
                    self.device_bank_registry.set_device_bank(device, bank_index)

    def target_track_changed(self, target_track):
        pass

    def drum_group_changed(self, drum_group):
        pass

    def sliced_simpler_changed(self, sliced_simpler):
        pass

    def set_can_update_controlled_track(self, can_update):
        self._can_update_controlled_track = can_update
        self._update_controlled_track()

    def set_can_auto_arm(self, can_auto_arm):
        self._can_enable_auto_arm = can_auto_arm
        self._update_auto_arm()

    def update(self):
        super().update()
        if self.display:
            self.display.clear_content_cache()

    def update_display(self):
        super().update_display()
        self._render_and_update_display()

    def react(self, event):
        if self.display:
            self.display.react(event)

    @staticmethod
    def mxd_grab_control_priority():
        return M4L_PRIORITY

    def _render_and_update_display(self):
        if self.display:
            with self._control_surface_injector:
                self.display.render_and_update_display()

    def _suppress_notifications(self):
        if self.display:
            suppress_notifications(self.display.state)

    @staticmethod
    def _should_include_element_in_background(element):
        return True

    def _get_additional_dependencies(self):
        pass

    def _on_entering_component_guard(self):
        pass

    def _send_specification_messages(self, messages_name='hello_messages'):
        for msg in getattr(self.specification, messages_name) or []:
            self._send_midi(msg)

    @contextmanager
    def _component_guard(self):
        with super()._component_guard():
            with self._element_injector:
                with self._deferring_render_and_update_display():
                    yield

    @staticmethod
    def _create_elements(specification):
        return specification.elements_type()

    def _create_background(self, priority):
        layer_dict = {c.name: c for c in  if self._should_include_element_in_background(c)}
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

    def _create_instrument_finder(self):
        if self.instrument_finder is None:
            self.instrument_finder = InstrumentFinderComponent()
            self._ControlSurface__on_instrument_changed.subject = self.instrument_finder
        return self.instrument_finder

    @lazy_attribute
    def _create_session_ring(self):
        self._session_ring = self.specification.session_ring_component_type(is_enabled=False,
          num_tracks=(self.specification.num_tracks),
          num_scenes=(self.specification.num_scenes),
          include_returns=(self.specification.include_returns),
          include_master=(self.specification.include_master),
          right_align_non_player_tracks=(self.specification.right_align_non_player_tracks),
          snap_track_offset=(self.specification.snap_track_offset))
        return self._session_ring

    @lazy_attribute
    def _create_device_provider(self):
        self.device_provider = self.register_disconnectable(self.specification.device_provider_type(song=(self.song)))
        self.device_provider.update_device_selection()
        return self.device_provider

    @lazy_attribute
    def _create_device_bank_registry(self):
        self.device_bank_registry = self.register_disconnectable(DeviceBankRegistry())
        return self.device_bank_registry

    def _create_extended_injector(self):
        inject_dict = {'full_velocity':const(self._c_instance.full_velocity), 
         'target_track':const(self._target_track), 
         'session_ring':lambda: self._create_session_ring
, 
         'device_provider':lambda: self._create_device_provider
, 
         'device_bank_registry':lambda: self._create_device_bank_registry
, 
         'toggle_lock':const(self._c_instance.toggle_lock), 
         'playhead':const(self._c_instance.playhead)}
        inject_dict.update(self._get_additional_dependencies() or {})
        return inject(**inject_dict).everywhere()

    def _create_feedback_related_listeners(self):
        self.register_slot(self.song, self._update_feedback_velocity, 'session_record')
        self.register_slot(self.song, self._update_feedback_velocity, 'record_mode')

    def _register_component(self, component):
        super()._register_component(component)
        if isinstance(component, DrumGroupComponent):
            self._drum_group_component = component
            self._create_instrument_finder()
        if isinstance(component, SlicedSimplerComponent):
            self._sliced_simpler_component = component
            self._create_instrument_finder()
        if isinstance(component, ViewControlComponent):
            link_to_tracks = self.specification.link_session_ring_to_track_selection
            link_to_scenes = self.specification.link_session_ring_to_scene_selection
            if link_to_tracks or link_to_scenes:
                self.session_ring_selection_linking = self.register_disconnectable(SessionRingSelectionLinking(selection_changed_notifier=component,
                  link_to_track_selection=link_to_tracks,
                  link_to_scene_selection=link_to_scenes))

    def _update_feedback_velocity(self):
        track = self._target_track.target_track
        if is_song_recording() and is_track_armed(track):
            feedback_velocity = self.specification.recording_feedback_velocity
        else:
            feedback_velocity = self.specification.playing_feedback_velocity
        self._c_instance.set_feedback_velocity(int(feedback_velocity))
        self._c_instance.playhead.velocity = int(feedback_velocity)

    def _update_controlled_track(self):
        if self._can_update_controlled_track:
            self.set_controlled_track(self._target_track.target_track)
        else:
            self.release_controlled_track()

    def _update_auto_arm(self):
        if self._auto_arm:
            self._auto_arm.set_enabled(self._identification.is_identified and self._can_enable_auto_arm)

    def _update_instrument_components(self):
        self._update_controlled_track()
        if self._drum_group_component:
            drum_group = self.instrument_finder.drum_group
            self._drum_group_component.set_drum_group_device(drum_group)
            self.drum_group_changed(drum_group)
        if self._sliced_simpler_component:
            sliced_simpler = self.instrument_finder.sliced_simpler
            self._sliced_simpler_component.set_simpler_device(sliced_simpler)
            self.sliced_simpler_changed(sliced_simpler)

    @listens('target_track')
    def __on_target_track_changed(self):
        track = self._target_track.target_track
        self._ControlSurface__on_track_arm_changed.subject = track
        self._ControlSurface__on_track_implicit_arm_changed.subject = track
        self._update_controlled_track()
        self.target_track_changed(track)

    @listens('arm')
    def __on_track_arm_changed(self):
        self._update_feedback_velocity()

    @listens('implicit_arm')
    def __on_track_implicit_arm_changed(self):
        self._update_feedback_velocity()

    @listens('instrument')
    def __on_instrument_changed(self):
        self._update_instrument_components()

    @listens('is_identified')
    def __on_is_identified_changed(self, is_identified):
        if is_identified:
            self.on_identified(self._identification.received_response_bytes)
        if self._can_enable_session_ring:
            self._session_ring.set_enabled(is_identified)
        self._update_auto_arm()