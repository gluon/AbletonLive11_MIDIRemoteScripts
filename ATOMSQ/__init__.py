# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\__init__.py
# Compiled at: 2023-09-13 04:24:51
# Size of source mod 2**32: 3295 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.base import listens
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from ableton.v3.control_surface.components import TranslatingBackgroundComponent
from ableton.v3.control_surface.legacy_bank_definitions import banked
from . import midi
from .colors import Rgb
from .display import display_specification
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .launch_and_stop import LaunchAndStopComponent
from .mappings import create_mappings
from .skin import Skin

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479,
                          product_ids=[522],
                          model_name=['ATM SQ']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return ATOMSQ(c_instance=c_instance)


class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    display_specification = display_specification
    num_tracks = SESSION_WIDTH
    num_scenes = SESSION_HEIGHT
    link_session_ring_to_track_selection = True
    identity_response_id_bytes = midi.PRODUCT_ID_BYTES
    hello_messages = (midi.NATIVE_MODE_ON_MESSAGE,)
    goodbye_messages = (midi.NATIVE_MODE_OFF_MESSAGE,)
    create_mappings_function = create_mappings
    quantized_parameter_sensitivity = 0.3
    parameter_bank_definitions = banked()
    component_map = {'Launch_And_Stop':LaunchAndStopComponent, 
     'Translating_Background':partial(TranslatingBackgroundComponent,
       translation_channel=midi.USER_MODE_START_CHANNEL)}


class ATOMSQ(ControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(a, specification=Specification, **k)

    def setup(self):
        super().setup()
        self._ATOMSQ__on_main_modes_changed.subject = self.component_map['Main_Modes']
        self._update_firmware()

    def on_identified(self, response_bytes):
        self.schedule_message(1, self._update_firmware)
        super().on_identified(response_bytes)

    @listens('selected_mode')
    def __on_main_modes_changed(self, _):
        self._update_firmware()
        self.elements.track_name_display_command.clear_send_cache()
        self.elements.track_name_display.reset()
        self.elements.device_name_display_command.clear_send_cache()
        self.elements.device_name_display.reset()

    def _update_firmware(self):
        mode = self.component_map['Main_Modes'].selected_mode
        self.elements.lower_firmware_toggle_switch.send_value(bool(mode != 'song'))
        self.elements.upper_firmware_toggle_switch.send_value(bool(mode == 'instrument'))