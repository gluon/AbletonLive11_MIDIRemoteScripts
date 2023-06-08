from __future__ import absolute_import, print_function, unicode_literals
import Live
import _Generic.GenericScript as GenericScript
from .config import *

def create_instance(c_instance):
    return GenericScript(c_instance, Live.MidiMap.MapMode.absolute, Live.MidiMap.MapMode.absolute, DEVICE_CONTROLS, TRANSPORT_CONTROLS, VOLUME_CONTROLS, TRACKARM_CONTROLS, BANK_CONTROLS, CONTROLLER_DESCRIPTIONS)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891,
                          product_ids=[8200],
                          model_name='Ozone'), 
     
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), outport(props=[SCRIPT])]}