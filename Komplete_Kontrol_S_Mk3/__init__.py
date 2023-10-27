# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk3\__init__.py
# Compiled at: 2023-09-22 09:34:38
# Size of source mod 2**32: 3113 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from ableton.v3.control_surface.midi import CC_STATUS
from .display import display_specification
from .elements import Elements
from .focus_follow import FocusFollowComponent
from .launch_and_stop import LaunchAndStopComponent
from .mappings import create_mappings
from .midi import MIDI_CHANNEL
from .session_navigation import SessionNavigationComponent
from .skin import Skin
from .view_control import ViewControlComponent

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6092,
                          product_ids=[8448],
                          model_name=['KONTROL S49 MK3']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC, SCRIPT])]}


def create_instance(c_instance):
    return Komplete_Kontrol_S_Mk3(c_instance=c_instance, specification=Specification)


class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin)
    create_mappings_function = create_mappings
    display_specification = display_specification
    include_returns = True
    include_master = True
    snap_track_offset = True
    include_auto_arming = True
    identity_request = (MIDI_CHANNEL + CC_STATUS, 1, 0)
    custom_identity_response = (MIDI_CHANNEL + CC_STATUS, 1)
    goodbye_messages = ((MIDI_CHANNEL + CC_STATUS, 2, 0),)
    send_goodbye_messages_last = False
    component_map = {'Focus_Follow':FocusFollowComponent, 
     'Launch_And_Stop':LaunchAndStopComponent, 
     'Session_Navigation':partial(SessionNavigationComponent, snap_track_offset=True), 
     'View_Control':ViewControlComponent}


class Komplete_Kontrol_S_Mk3(ControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self.set_can_auto_arm(True)

    def port_settings_changed(self):
        super().port_settings_changed()
        self._set_mixer_enabled_state(False)

    def on_identified(self, response_bytes):
        self._set_mixer_enabled_state(True)
        super().on_identified(response_bytes)

    def _set_mixer_enabled_state(self, enabled):
        with self.component_guard():
            self.component_map['Mixer'].set_enabled(enabled)