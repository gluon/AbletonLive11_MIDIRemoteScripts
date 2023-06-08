from __future__ import absolute_import, print_function, unicode_literals
from types import SimpleNamespace
from . import BasicColors, DeviceProvider, midi
from .components import AutoArmComponent, SessionRingComponent, TargetTrackComponent
from .consts import LOW_PRIORITY
from .default_skin import default_skin

class ControlSurfaceSpecification(SimpleNamespace):
    elements_type = None
    control_surface_skin = default_skin
    num_tracks = 8
    num_scenes = 1
    include_returns = False
    include_master = False
    right_align_non_player_tracks = False
    include_auto_arming = False
    link_session_ring_to_track_selection = False
    link_session_ring_to_scene_selection = False
    session_ring_component_type = SessionRingComponent
    target_track_component_type = TargetTrackComponent
    auto_arm_component_type = AutoArmComponent
    device_provider_type = DeviceProvider
    feedback_channels = None
    playing_feedback_velocity = BasicColors.ON.midi_value
    recording_feedback_velocity = BasicColors.ON.midi_value
    background_priority = LOW_PRIORITY
    identity_response_id_bytes = None
    custom_identity_response = None
    identity_request = midi.SYSEX_IDENTITY_REQUEST_MESSAGE
    identity_request_delay = 0.0
    hello_messages = None
    goodbye_messages = None
    display_specification = None