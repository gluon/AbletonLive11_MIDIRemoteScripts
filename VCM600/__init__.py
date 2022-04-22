# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/VCM600/__init__.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 949 bytes
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