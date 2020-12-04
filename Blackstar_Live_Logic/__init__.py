#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Blackstar_Live_Logic/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import controller_id, CONTROLLER_ID_KEY, inport, NOTES_CC, outport, PORTS_KEY, REMOTE, SCRIPT
from .blackstar_live_logic import Blackstar_Live_Logic

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=10196, product_ids=[4097], model_name=[u'Live Logic MIDI Controller']),
     PORTS_KEY: [inport(props=[SCRIPT, REMOTE, NOTES_CC]), outport(props=[SCRIPT, REMOTE, NOTES_CC])]}


def create_instance(c_instance):
    return Blackstar_Live_Logic(c_instance=c_instance)
