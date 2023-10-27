# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Alesis_VI\__init__.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 743 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .Alesis_VI import Alesis_VI

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=5042,
                          product_ids=[
                         131, 132, 133],
                          model_name=[
                         'VI25', 'VI49', 'VI61']), 
     
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Alesis_VI(c_instance)