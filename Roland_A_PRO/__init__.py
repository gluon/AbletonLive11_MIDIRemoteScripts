# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_A_PRO\__init__.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 840 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .Roland_A_PRO import Roland_A_PRO

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1410,
                          product_ids=[271],
                          model_name='A-PRO'), 
     
     PORTS_KEY: [
                 inport(props=[]),
                 inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[]),
                 outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Roland_A_PRO(c_instance)