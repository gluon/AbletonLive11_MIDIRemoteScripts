from __future__ import absolute_import, print_function, unicode_literals
import _Framework.Capabilities as caps
from .VCM600 import VCM600

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=6817,
                               product_ids=[64],
                               model_name=['VCM-600']), 
     
     caps.PORTS_KEY: [
                      caps.inport(props=[caps.SCRIPT]),
                      caps.outport(props=[caps.SCRIPT])]}


def create_instance(c_instance):
    return VCM600(c_instance)