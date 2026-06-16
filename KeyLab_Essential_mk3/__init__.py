# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential_mk3\__init__.py
# Compiled at: 2023-09-13 04:24:51
# Size of source mod 2**32: 2979 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.base import listens
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from ableton.v3.control_surface.components import DeviceComponent
from MiniLab_3 import DrumGroupComponent
from .colors import Rgb, Skin
from .device_bank_toggle import DeviceBankToggleComponent
from .display import display_specification
from .elements import Elements
from .mappings import create_mappings
from .midi import CONNECTION_MESSAGE, DAW_PROGRAM_BYTE, DISCONNECTION_MESSAGE, REQUEST_PROGRAM_MESSAGE
from .mixer import MixerComponent

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=7285,
                          product_ids=[
                         588, 652, 716],
                          model_name=[
                         'KeyLab 3 Essential']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT]),
                 inport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[NOTES_CC])]}


def create_instance(c_instance):
    return KeyLab_Essential_mk3(c_instance=c_instance)


class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = 4
    num_scenes = 2
    link_session_ring_to_track_selection = True
    link_session_ring_to_scene_selection = True
    identity_response_id_bytes = (0, 32, 107, 2, 0, 5)
    create_mappings_function = create_mappings
    hello_messages = (CONNECTION_MESSAGE, REQUEST_PROGRAM_MESSAGE)
    goodbye_messages = (DISCONNECTION_MESSAGE,)
    component_map = {'Device':partial(DeviceComponent,
       bank_size=16,
       bank_navigation_component_type=DeviceBankToggleComponent), 
     'Drum_Group':DrumGroupComponent, 
     'Mixer':MixerComponent}
    display_specification = display_specification


class KeyLab_Essential_mk3(ControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(Specification, *a, **k)

    def setup(self):
        super().setup()
        self._KeyLab_Essential_mk3__on_firmware_program_changed.subject = self.elements.program_command

    @listens('value')
    def __on_firmware_program_changed(self, value):
        if value[0] == DAW_PROGRAM_BYTE:
            for encoder in self.elements.continuous_controls_raw:
                encoder.realign_value()

            self.elements.encoder_9.realign_value()