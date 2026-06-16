# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk2\__init__.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 473 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import SUGGESTED_PORT_NAMES_KEY
from .komplete_kontrol_s_mk2 import Komplete_Kontrol_S_Mk2

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: ['Komplete Kontrol DAW - 1']}


def create_instance(c_instance):
    return Komplete_Kontrol_S_Mk2(c_instance=c_instance)