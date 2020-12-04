#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Code_Series/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .code import Code

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[12548, 12549, 12550], model_name=[u'Code 25', u'Code 49', u'Code 61']),
     PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 inport(props=[]),
                 outport(props=[]),
                 outport(props=[]),
                 outport(props=[SCRIPT]),
                 outport(props=[])]}


def create_instance(c_instance):
    return Code(c_instance=c_instance)
