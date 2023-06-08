from __future__ import absolute_import, print_function, unicode_literals
import Live
import _Generic.GenericScript as GenericScript
from .config import *

def create_instance(c_instance):
    return GenericScript(c_instance, Live.MidiMap.MapMode.absolute, Live.MidiMap.MapMode.absolute, DEVICE_CONTROLS, TRANSPORT_CONTROLS, VOLUME_CONTROLS, TRACKARM_CONTROLS, BANK_CONTROLS, CONTROLLER_DESCRIPTIONS, MIXER_OPTIONS)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2372,
                          product_ids=[261],
                          model_name='padKONTROL'), 
     
     PORTS_KEY: [
                 inport(props=[PLAIN_OLD_MIDI]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 inport(props=[]),
                 outport(props=[PLAIN_OLD_MIDI]),
                 outport(props=[SCRIPT])]}