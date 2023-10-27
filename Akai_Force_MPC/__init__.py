# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\__init__.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 697 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SUGGESTED_PORT_NAMES_KEY, inport, outport
from .akai_force_mpc import Akai_Force_MPC

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: ['Akai Network - DAW Control'], 
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return Akai_Force_MPC(c_instance)