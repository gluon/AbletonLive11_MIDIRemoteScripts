#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .sl_mkiii import SLMkIII

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[257], model_name=[u'Novation SL MkIII']),
     PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 inport(props=[NOTES_CC, REMOTE]),
                 outport(props=[]),
                 outport(props=[SCRIPT]),
                 outport(props=[]),
                 outport(props=[])]}


def create_instance(c_instance):
    return SLMkIII(c_instance=c_instance)
