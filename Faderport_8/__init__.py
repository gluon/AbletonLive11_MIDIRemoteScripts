from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from MackieControl import MackieControl

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479,
                          product_ids=[515],
                          model_name=['PreSonus FP8']), 
     
     PORTS_KEY: [inport(props=[SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return MackieControl(c_instance)