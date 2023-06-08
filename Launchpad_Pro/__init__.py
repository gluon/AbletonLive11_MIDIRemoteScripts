from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from .Launchpad_Pro import Launchpad_Pro

def create_instance(c_instance):
    return Launchpad_Pro(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661,
                          product_ids=[81],
                          model_name='Launchpad Pro'), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 inport(props=[]),
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE]),
                 outport(props=[])]}