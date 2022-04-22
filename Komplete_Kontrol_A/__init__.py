# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Komplete_Kontrol_A/__init__.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 484 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import SUGGESTED_PORT_NAMES_KEY
from .komplete_kontrol_a import Komplete_Kontrol_A

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: ['Komplete Kontrol A DAW', 'Komplete Kontrol M DAW']}


def create_instance(c_instance):
    return Komplete_Kontrol_A(c_instance=c_instance)