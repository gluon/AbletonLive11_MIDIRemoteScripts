# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Blackstar_Live_Logic/__init__.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 815 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .blackstar_live_logic import Blackstar_Live_Logic

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=10196,
                          product_ids=[
                         4097],
                          model_name=[
                         'Live Logic MIDI Controller']), 
     
     PORTS_KEY: [
                 inport(props=[SCRIPT, REMOTE, NOTES_CC]),
                 outport(props=[SCRIPT, REMOTE, NOTES_CC])]}


def create_instance(c_instance):
    return Blackstar_Live_Logic(c_instance=c_instance)