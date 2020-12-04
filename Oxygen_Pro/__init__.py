#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Oxygen_Pro/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from .oxygen_pro import Oxygen_Pro

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[56, 57, 58], model_name=[u'Oxygen Pro 25', u'Oxygen Pro 49', u'Oxygen Pro 61']),
     PORTS_KEY: [inport(props=[]),
                 inport(props=[]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Oxygen_Pro(c_instance=c_instance)
