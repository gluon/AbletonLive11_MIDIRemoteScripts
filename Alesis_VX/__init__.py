from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .Alesis_VX import Alesis_VX

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=5042,
                          product_ids=[4176],
                          model_name='VX49'), 
     
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Alesis_VX(c_instance)