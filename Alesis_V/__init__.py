from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .Alesis_V import Alesis_V

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=5042,
                          product_ids=[
                         134, 135, 136],
                          model_name=[
                         'V25', 'V49', 'V61']), 
     
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Alesis_V(c_instance)