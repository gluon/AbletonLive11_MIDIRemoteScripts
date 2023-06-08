<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/__init__.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 736 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.base import liveobj_valid
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from ableton.v3.control_surface.components import ArmedTargetTrackComponent, TranslatingBackgroundComponent
from universal import UniversalControlSurface, UniversalControlSurfaceSpecification, create_skin
from . import midi
from .colors import Rgb
from .drum_group import DrumGroupComponent
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .keyboard import KeyboardComponent
from .mappings import create_mappings
from .skin import Skin

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479,
                          product_ids=[518],
                          model_name=['ATOM']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
<<<<<<< HEAD
    return ATOM(c_instance=c_instance)


class Specification(UniversalControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    target_track_component_type = ArmedTargetTrackComponent
    num_tracks = SESSION_WIDTH
    num_scenes = SESSION_HEIGHT
    identity_request = midi.NATIVE_MODE_ON_MESSAGE
    custom_identity_response = (191, 127, 127)
    goodbye_messages = (midi.NATIVE_MODE_OFF_MESSAGE,)
    create_mappings_function = create_mappings
    component_map = {'Drum_Group':partial(DrumGroupComponent, translation_channel=midi.DRUM_CHANNEL), 
     'Keyboard':partial(KeyboardComponent, midi.KEYBOARD_CHANNEL), 
     'Translating_Background':partial(TranslatingBackgroundComponent,
       translation_channel=midi.USER_CHANNEL)}


class ATOM(UniversalControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(a, specification=Specification, **k)

    def port_settings_changed(self):
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)
        super().port_settings_changed()

    def drum_group_changed(self, drum_group):
        self.component_map['Note_Modes'].selected_mode = 'drum' if liveobj_valid(drum_group) else 'keyboard'
=======
    return ATOM(c_instance=c_instance)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
