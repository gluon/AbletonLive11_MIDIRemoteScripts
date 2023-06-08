from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from .KeyPad import KeyPad

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=9901,
                          product_ids=[28149],
                          model_name='Reloop KeyPad'), 
     
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), outport(props=[NOTES_CC, SCRIPT])]}


def create_instance(c_instance):
    return KeyPad(c_instance)