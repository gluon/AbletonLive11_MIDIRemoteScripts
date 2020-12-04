#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/VCM600/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.Capabilities as caps
from .VCM600 import VCM600

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=6817, product_ids=[64], model_name=[u'VCM-600']),
     caps.PORTS_KEY: [caps.inport(props=[caps.SCRIPT]), caps.outport(props=[caps.SCRIPT])]}


def create_instance(c_instance):
    u""" Creates and returns the ADA1 script """
    return VCM600(c_instance)
