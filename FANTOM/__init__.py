<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from ableton.v3.control_surface.components import DEFAULT_DRUM_TRANSLATION_CHANNEL
from ableton.v3.control_surface.legacy_bank_definitions import best_of_banks
from universal import UniversalControlSurface, UniversalControlSurfaceSpecification, create_skin
from . import sysex
from .colors import Rgb, Skin
from .elements import NUM_SCENES, NUM_TRACKS, Elements
from .mappings import create_mappings
from .mixer import MixerComponent
from .session import SessionComponent
from .transport import TransportComponent
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/__init__.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 811 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .fantom import FANTOM
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1410,
                          product_ids=[
                         544, 643],
                          model_name=[
                         'FANTOM-6 7 8', 'FANTOM-06 07 08']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC]),
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return FANTOM(c_instance=c_instance)


class Specification(UniversalControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = NUM_TRACKS
    num_scenes = NUM_SCENES
    include_returns = True
    feedback_channels = [DEFAULT_DRUM_TRANSLATION_CHANNEL]
    playing_feedback_velocity = Rgb.GREEN.midi_value
    recording_feedback_velocity = Rgb.RED.midi_value
    custom_identity_response = sysex.REFRESH_REQUEST
    identity_request = sysex.INITIATE_CONNECTION
    identity_request_delay = 10.0
    goodbye_messages = (sysex.TERMINATE_CONNECTION,)
    create_mappings_function = create_mappings
    parameter_bank_definitions = best_of_banks()
    component_map = {'Mixer':MixerComponent, 
     'Session':SessionComponent, 
     'Transport':TransportComponent}


class FANTOM(UniversalControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(a, specification=Specification, **k)

    def setup(self):
        super().setup()
        self.set_can_update_controlled_track(True)