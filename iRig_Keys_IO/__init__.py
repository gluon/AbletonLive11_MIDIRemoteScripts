from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .irig_keys_io import IRigKeysIO

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6499,
                          product_ids=[
                         46, 45],
                          model_name=[
                         'iRig Keys IO 25', 'iRig Keys IO 49']), 
     
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return IRigKeysIO(c_instance=c_instance)