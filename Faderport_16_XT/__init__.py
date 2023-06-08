from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from MackieControlXT import MackieControlXT

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479,
                          product_ids=[516],
                          model_name=['PreSonus FP16']), 
     
     PORTS_KEY: [
                 inport(props=[]),
                 inport(props=[SCRIPT, REMOTE]),
                 outport(props=[]),
                 outport(props=[SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return MackieControlXT(c_instance)