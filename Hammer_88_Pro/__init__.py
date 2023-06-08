from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .hammer_88_pro import Hammer_88_Pro

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891,
                          product_ids=[60],
                          model_name=['Hammer 88 Pro']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[]),
                 outport(props=[]),
                 outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Hammer_88_Pro(c_instance=c_instance)