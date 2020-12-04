#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_MK3/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from .launchkey_mk3 import Launchkey_MK3
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[308,
                         309,
                         310,
                         311], model_name=[u'Launchkey MK3 25',
                         u'Launchkey MK3 37',
                         u'Launchkey MK3 49',
                         u'Launchkey MK3 61']),
     PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[SYNC, REMOTE]),
                 outport(props=[NOTES_CC, SCRIPT])]}


def create_instance(c_instance):
    return Launchkey_MK3(c_instance=c_instance)
