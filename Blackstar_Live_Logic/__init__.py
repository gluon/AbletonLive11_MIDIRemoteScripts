from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .blackstar_live_logic import Blackstar_Live_Logic

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=10196,
                          product_ids=[
                         4097],
                          model_name=[
                         'Live Logic MIDI Controller']), 
     
     PORTS_KEY: [
                 inport(props=[SCRIPT, REMOTE, NOTES_CC]),
                 outport(props=[SCRIPT, REMOTE, NOTES_CC])]}


def create_instance(c_instance):
    return Blackstar_Live_Logic(c_instance=c_instance)