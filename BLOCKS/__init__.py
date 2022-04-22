# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/BLOCKS/__init__.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 717 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface as caps
from .blocks import Blocks

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=10996,
                               product_ids=[
                              2304],
                               model_name=[
                              'Lightpad BLOCK', 'BLOCKS']), 
     
     caps.PORTS_KEY: [
                      caps.inport(props=[caps.NOTES_CC, caps.SCRIPT]),
                      caps.outport(props=[caps.NOTES_CC, caps.SCRIPT])], 
     
     caps.TYPE_KEY: 'blocks'}


def create_instance(c_instance):
    return Blocks(c_instance=c_instance)