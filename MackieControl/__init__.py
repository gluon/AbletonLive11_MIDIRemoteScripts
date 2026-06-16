# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\__init__.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1319 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .MackieControl import MackieControl

def create_instance(c_instance):
    return MackieControl(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2675,
                          product_ids=[6],
                          model_name='MCU Pro USB v3.1'), 
     
     PORTS_KEY: [
                 inport(props=[SCRIPT, REMOTE]),
                 inport(props=[]),
                 inport(props=[]),
                 inport(props=[]),
                 outport(props=[SCRIPT, REMOTE]),
                 outport(props=[]),
                 outport(props=[]),
                 outport(props=[])]}