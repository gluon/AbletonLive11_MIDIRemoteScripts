# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Novation_Impulse\__init__.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1200 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .Novation_Impulse import Novation_Impulse

def create_instance(c_instance):
    return Novation_Impulse(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661,
                          product_ids=[25],
                          model_name='Impulse 25'), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE, SCRIPT]),
                 inport(props=[NOTES_CC, REMOTE]),
                 outport(props=[NOTES_CC, REMOTE, SCRIPT])]}