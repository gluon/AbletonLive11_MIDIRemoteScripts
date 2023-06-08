from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .oxygen_5th_gen import Oxygen_5th_Gen

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891,
                          product_ids=[
                         1, 2, 3],
                          model_name=[
                         'Oxygen 25 MKV', 'Oxygen 49 MKV', 'Oxygen 61 MKV']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[]),
                 outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Oxygen_5th_Gen(c_instance=c_instance)