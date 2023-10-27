# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\__init__.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 957 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .sl_mkiii import SLMkIII

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661,
                          product_ids=[257],
                          model_name=['Novation SL MkIII']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 inport(props=[NOTES_CC, REMOTE]),
                 outport(props=[]),
                 outport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[]),
                 outport(props=[])]}


def create_instance(c_instance):
    return SLMkIII(c_instance=c_instance)