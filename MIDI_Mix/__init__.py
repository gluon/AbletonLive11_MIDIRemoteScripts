# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MIDI_Mix\__init__.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 638 bytes
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.Capabilities as caps
from .MIDI_Mix import MIDI_Mix

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=2536,
                               product_ids=[49],
                               model_name='MIDI Mix'), 
     
     caps.PORTS_KEY: [
                      caps.inport(props=[caps.NOTES_CC, caps.SCRIPT]),
                      caps.outport(props=[caps.NOTES_CC, caps.SCRIPT])]}


def create_instance(c_instance):
    return MIDI_Mix(c_instance)