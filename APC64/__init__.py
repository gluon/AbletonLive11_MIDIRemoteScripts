# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\__init__.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 4283 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import const, listens, task
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, HIDDEN, NOTES_CC, PORTS_KEY, SCRIPT, SYNC, controller_id, inport, outport
from ableton.v3.control_surface.components import DEFAULT_DRUM_TRANSLATION_CHANNEL
from ableton.v3.live import liveobj_valid
from .colors import Rgb
from .device import DeviceComponent
from .display import display_specification
from .elements import Elements
from .global_quantization import GlobalQuantizationComponent
from .mappings import create_mappings
from .mixer import MixerComponent
from .recording import FixedLengthRecordingMethod
from .render_to_clip import RenderToClipComponent
from .session import SessionComponent
from .settings import SettingsComponent
from .skin import Skin
from .transport import TransportComponent

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536,
                          product_ids=[83],
                          model_name=['APC64']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, HIDDEN]),
                 outport(props=[NOTES_CC, SCRIPT, HIDDEN]),
                 outport(props=[SYNC])]}


def create_instance(c_instance):
    return APC64(c_instance=c_instance)


class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = 8
    num_scenes = 8
    include_returns = True
    include_master = True
    right_align_non_player_tracks = True
    include_auto_arming = True
    feedback_channels = [DEFAULT_DRUM_TRANSLATION_CHANNEL]
    playing_feedback_velocity = Rgb.GREEN.midi_value
    recording_feedback_velocity = Rgb.RED.midi_value
    identity_response_id_bytes = (71, 83, 0, 25)
    create_mappings_function = create_mappings
    recording_method_type = FixedLengthRecordingMethod
    component_map = {
      'Device': DeviceComponent,
      'Global_Quantization': GlobalQuantizationComponent,
      'Mixer': MixerComponent,
      'Render_To_Clip': RenderToClipComponent,
      'Session': SessionComponent,
      'Transport': TransportComponent}
    display_specification = display_specification


class APC64(ControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(Specification, *a, **k)

    def disconnect(self):
        self.elements.track_type_element.send_value(0)
        super().disconnect()

    def setup(self):
        super().setup()
        self._APC64__on_pad_mode_changed.subject = self.component_map['Pad_Modes']

    def drum_group_changed(self, drum_group):
        has_drum_group = liveobj_valid(drum_group)
        self.elements.track_type_element.send_value(bool(has_drum_group))
        if not has_drum_group:
            if self.component_map['Pad_Modes'].selected_mode == 'drum':
                self.component_map['Pad_Modes'].selected_mode = 'note'

    def _get_additional_dependencies(self):
        settings = SettingsComponent()
        self.component_map['Settings'] = settings
        return {'settings_component': const(settings)}

    @listens('selected_mode')
    def __on_pad_mode_changed(self, selected_mode):
        self.set_can_update_controlled_track(selected_mode == 'drum')
        if selected_mode in ('session', 'session_overview', 'drum'):
            self._tasks.add(task.run(self.refresh_state))
        self.set_can_auto_arm(selected_mode not in ('session', 'session_overview'))