# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Faderport_16_XT\__init__.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 810 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from MackieControlXT import MackieControlXT

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479,
                          product_ids=[516],
                          model_name=['PreSonus FP16']), 
     
     PORTS_KEY: [
                 inport(props=[]),
                 inport(props=[SCRIPT, REMOTE]),
                 outport(props=[]),
                 outport(props=[SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return MackieControlXT(c_instance)