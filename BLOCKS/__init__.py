# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\BLOCKS\__init__.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 743 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import capabilities as caps
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