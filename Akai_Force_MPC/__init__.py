from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SUGGESTED_PORT_NAMES_KEY, inport, outport
from .akai_force_mpc import Akai_Force_MPC

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: ['Akai Network - DAW Control'], 
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return Akai_Force_MPC(c_instance)